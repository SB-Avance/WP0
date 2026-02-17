"""
Webhook para recibir notificaciones de WhatsApp y almacenar mensajes en Dataverse
Implementa sistema de menú interactivo dinámico cargado desde cr321_grup
"""
from flask import Blueprint, request, jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from goot import save_incoming_message, get_token, DATAVERSE_URL, PHONE_NUMBER_ID, ACCESS_TOKEN
import requests
from datetime import datetime, timezone
import json

# Importar handler manager - agregar path al directorio raíz
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from handlers.handler_manager import get_handler_manager

bp_webhook = Blueprint('webhook', __name__)

# Estado de conversaciones (en memoria - considerar usar Redis para producción)
conversation_states = {}

# Cache del menú (se recarga periódicamente)
MENU_CACHE = {
    "menu": {},
    "last_update": None
}


def crear_contacto_automatico(telefono, nombre=None):
    """
    Crear o obtener contacto automáticamente desde mensaje de WhatsApp
    Retorna el ID del contacto (existente o creado)
    """
    token = get_token()
    if not token:
        print("[CONTACTO] No se pudo obtener token")
        return None
    
    headers = {
        'Authorization': f'Bearer {token}',
        'OData-MaxVersion': '4.0',
        'OData-Version': '4.0',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    try:
        # 1. Verificar si ya existe contacto con ese teléfono
        url_buscar = f"{DATAVERSE_URL}/api/data/v9.2/cr321_contactos"
        params = {
            "$filter": f"cr321_telefono eq '{telefono}'",
            "$select": "cr321_contactoid,cr321_fromnombre,cr321_telefono"
        }
        
        response = requests.get(url_buscar, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            contactos = response.json().get("value", [])
            if contactos:
                print(f"[CONTACTO] Contacto existente: {contactos[0]['cr321_contactoid']}")
                return contactos[0]['cr321_contactoid']
        
        # 2. Crear nuevo contacto
        nombre_limpio = nombre.strip() if nombre else f"Contacto {telefono}"
        
        url_crear = f"{DATAVERSE_URL}/api/data/v9.2/cr321_contactos"
        payload = {
            "cr321_fromnombre": nombre_limpio,
            "cr321_telefono": telefono,
            "cr321_descripcion": "Contacto creado automáticamente desde WhatsApp",
            "cr321_fechacreacion": datetime.now(timezone.utc).isoformat()
        }
        
        response = requests.post(url_crear, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 204:
            # Obtener ID del contacto creado
            contacto_url = response.headers.get('OData-EntityId')
            if contacto_url:
                contacto_id = contacto_url.split('(')[1].split(')')[0]
                print(f"[CONTACTO] Nuevo contacto creado: {contacto_id}")
                return contacto_id
            else:
                # Buscar el contacto recién creado
                response2 = requests.get(url_buscar, params=params, headers=headers, timeout=10)
                if response2.status_code == 200:
                    contactos = response2.json().get("value", [])
                    if contactos:
                        return contactos[0]['cr321_contactoid']
        else:
            print(f"[CONTACTO] Error al crear: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"[CONTACTO] Error: {e}")
        import traceback
        traceback.print_exc()
        return None


def load_menu_from_dataverse():
    """
    Carga el menú dinámicamente desde la tabla cr321_chatbot
    CADA FILA ACTIVA = UNA OPCIÓN DEL MENÚ
    - cr321_name = Nombre de la opción principal (1. Informacion, 2. Soporte, etc)
    - cr321_elemento1-5 = Sub-opciones de esa categoría
    Solo carga chatbots con cr321_active = true
    """
    token = get_token()
    if not token:
        print("[WEBHOOK] No se pudo obtener token para cargar menú")
        return get_default_menu()
    
    try:
        # Consultar TODOS los chatbots activos (cr321_active = true)
        url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_chatbots"
        url += "?$select=cr321_chatbotid,cr321_name,cr321_active,cr321_elemento1,cr321_elemento2,cr321_elemento3,cr321_grupoid,cr321_config"
        url += "&$filter=cr321_active eq true"
        url += "&$orderby=cr321_name asc"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            chatbots = data.get("value", [])
            
            if not chatbots:
                print("[WEBHOOK] No se encontraron chatbots activos, usando menú por defecto")
                return get_default_menu()
            
            # Construir menú dinámico: CADA CHATBOT = UNA OPCIÓN PRINCIPAL
            menu_opciones = {}
            
            print(f"[WEBHOOK] Construyendo menú desde {len(chatbots)} chatbots activos:")
            
            for idx, chatbot in enumerate(chatbots, 1):
                chatbot_name = chatbot.get("cr321_name", f"Opción {idx}")
                
                # ✅ VALIDACIÓN: Nombre de categoría no vacío
                if not chatbot_name or not chatbot_name.strip():
                    print(f"  [!] ADVERTENCIA: Chatbot {idx} sin nombre, omitiendo")
                    continue
                
                # Obtener elementos (sub-opciones) de este chatbot (solo 3 elementos disponibles)
                elementos = [
                    chatbot.get("cr321_elemento1"),
                    chatbot.get("cr321_elemento2"),
                    chatbot.get("cr321_elemento3")
                ]
                
                # Filtrar solo elementos no vacíos y limpiar espacios
                sub_opciones = [e.strip() for e in elementos if e and e.strip()]
                
                # ✅ VALIDACIÓN: Al menos 1 sub-opción requerida
                if not sub_opciones:
                    print(f"  [!] ADVERTENCIA: {chatbot_name} sin sub-opciones, omitiendo")
                    continue
                
                # ✅ VALIDACIÓN: Máximo 10 sub-opciones (límite de WhatsApp)
                if len(sub_opciones) > 10:
                    print(f"  [!] ADVERTENCIA: {chatbot_name} tiene {len(sub_opciones)} sub-opciones, usando solo las primeras 10")
                    sub_opciones = sub_opciones[:10]
                
                # 🆕 CARGAR CONFIGURACIÓN DE HANDLERS desde cr321_config (JSON)
                config_json = chatbot.get("cr321_config", "{}")
                handlers_config = {}
                
                try:
                    if config_json:
                        handlers_config = json.loads(config_json)
                        print(f"  📦 Config JSON cargada: {list(handlers_config.keys())}")
                except json.JSONDecodeError:
                    print(f"  ⚠️ Error parseando cr321_config para {chatbot_name}")
                    handlers_config = {}
                
                # Mapear nombre a tipo de flujo (usa el primer elemento o el nombre del chatbot)
                tipo = map_nombre_to_tipo(sub_opciones[0] if sub_opciones else chatbot_name)
                preguntas = get_preguntas_for_tipo(tipo)
                mensajes = get_mensajes_for_tipo(tipo)
                
                menu_opciones[str(idx)] = {
                    "nombre": chatbot_name,
                    "tipo": tipo,
                    "preguntas": preguntas,
                    "mensajes": mensajes,
                    "chatbot_id": chatbot.get("cr321_chatbotid"),
                    "chatbot_name": chatbot_name,
                    "sub_opciones": sub_opciones,  # ✨ NUEVO: Lista de sub-opciones
                    "grupo_id": chatbot.get("cr321_grupoid"),  # 🆕 GUID del grupo de Dataverse
                    "handlers_config": handlers_config  # 🆕 Configuración de handlers desde JSON
                }
                
                print(f"  [{idx}] {chatbot_name} - {len(sub_opciones)} sub-opciones")
                for sub_idx, sub_opcion in enumerate(sub_opciones, 1):
                    print(f"      {sub_idx}. {sub_opcion}")
            
            if not menu_opciones:
                print("[WEBHOOK] No se pudieron construir opciones de menú, usando menú por defecto")
                return get_default_menu()
            
            print(f"[WEBHOOK] Menú cargado exitosamente: {len(menu_opciones)} opciones principales")
            
            return menu_opciones
        else:
            print(f"[WEBHOOK] Error al cargar chatbots: {response.status_code}")
            return get_default_menu()
    
    except Exception as e:
        print(f"[WEBHOOK] Error al cargar menú desde chatbot: {e}")
        import traceback
        traceback.print_exc()
        return get_default_menu()


def get_default_menu():
    """Menú por defecto en caso de error al cargar desde Dataverse"""
    return {
        "1": {
            "nombre": "Solicitud Ticket",
            "tipo": "soporte",
            "preguntas": ["nombre", "empresa", "descripcion"],
            "mensajes": {
                "nombre": "Por favor, indique su nombre completo:",
                "empresa": "¿De qué empresa nos contacta?",
                "descripcion": "Describa su solicitud de soporte:"
            }
        },
        "2": {
            "nombre": "Cotizaciones",
            "tipo": "cotizacion",
            "preguntas": ["nombre", "empresa", "descripcion"],
            "mensajes": {
                "nombre": "Por favor, indique su nombre completo:",
                "empresa": "¿De qué empresa nos contacta?",
                "descripcion": "Describa el producto, marca y modelo si lo tiene:"
            }
        },
        "3": {
            "nombre": "Información",
            "tipo": "informacion",
            "preguntas": [],
            "respuesta": "Gracias por contactarnos. Visite nuestro sitio web para más información."
        },
        "4": {
            "nombre": "Solicitar atención de agente",
            "tipo": "atencion_agente",
            "preguntas": ["nombre"],
            "mensajes": {
                "nombre": "Por favor, indique su nombre para conectarlo con un agente:"
            }
        }
    }


def map_nombre_to_tipo(nombre):
    """Mapea nombre de grupo a tipo de flujo"""
    nombre_lower = nombre.lower()
    if "ticket" in nombre_lower or "soporte" in nombre_lower or "solicitud" in nombre_lower:
        return "soporte"
    elif "cotiz" in nombre_lower:
        return "cotizacion"
    elif "informacion" in nombre_lower or "info" in nombre_lower:
        return "informacion"
    elif "agente" in nombre_lower or "atencion" in nombre_lower or "atención" in nombre_lower:
        return "atencion_agente"
    else:
        return "general"


def get_preguntas_for_tipo(tipo):
    """Retorna preguntas según el tipo de flujo"""
    if tipo in ["soporte", "cotizacion"]:
        return ["nombre", "empresa", "descripcion"]
    elif tipo == "atencion_agente":
        return ["nombre"]
    else:
        return []


def get_mensajes_for_tipo(tipo):
    """Retorna mensajes según el tipo de flujo"""
    base_mensajes = {
        "nombre": "Por favor, indique su nombre completo:",
        "empresa": "¿De qué empresa nos contacta?",
    }
    
    if tipo == "soporte":
        base_mensajes["descripcion"] = "Describa su solicitud de soporte:"
    elif tipo == "cotizacion":
        base_mensajes["descripcion"] = "Describa el producto, marca y modelo si lo tiene:"
    elif tipo == "informacion":
        base_mensajes["respuesta"] = "Gracias por contactarnos. Visite nuestro sitio web para más información."
    elif tipo == "atencion_agente":
        # Solo nombre
        pass
    
    return base_mensajes


def get_current_menu():
    """Obtiene el menú actual (desde cache o recarga si es necesario)"""
    now = datetime.now(timezone.utc)
    
    # Recargar menú cada 5 minutos
    if (MENU_CACHE["last_update"] is None or 
        (now - MENU_CACHE["last_update"]).total_seconds() > 300):
        
        print("[MENU] Cargando menú desde Dataverse...")
        MENU_CACHE["menu"] = load_menu_from_dataverse()
        MENU_CACHE["last_update"] = now
        print(f"[MENU] Cache actualizado con {len(MENU_CACHE['menu'])} opciones")
    else:
        print(f"[MENU] Usando cache (último update hace {int((now - MENU_CACHE['last_update']).total_seconds())}s)")
    
    return MENU_CACHE["menu"]


def send_whatsapp_message(to_phone, message_text):
    """Enviar mensaje de WhatsApp"""
    try:
        url = f"https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages"
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": to_phone,
            "type": "text",
            "text": {"body": message_text}
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.status_code == 200
    except Exception as e:
        print(f"Error enviando mensaje WhatsApp: {e}")
        return False


def create_ticket_from_conversation(phone, conversation_data):
    """Crear ticket o cotización desde una conversación completada"""
    token = get_token()
    if not token:
        print("No se pudo obtener token para crear ticket/cotización")
        return False
    
    tipo = conversation_data.get("tipo", "soporte")
    nombre = conversation_data.get("nombre", "")
    empresa = conversation_data.get("empresa", "")
    descripcion = conversation_data.get("descripcion", "")
    
    # Si es cotización, crear en cr321_cotizacions
    if tipo == "cotizacion":
        return create_cotizacion_record(phone, nombre, empresa, descripcion, token)
    else:
        # Para soporte y otros, crear ticket normal
        return create_ticket_record(phone, nombre, empresa, descripcion, tipo, token)


def create_cotizacion_record(phone, nombre, empresa, descripcion, token):
    """Crear registro en tabla cr321_cotizacion"""
    try:
        url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_cotizacions"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        
        payload = {
            "cr321_nombre": f"Cotización de {nombre}",
            "cr321_cliente": f"{nombre} - {empresa}" if empresa else nombre,
            "cr321_descripcion": descripcion,
            "cr321_fecha": now
        }
        
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code in [200, 201, 204]:
            print(f"Cotización creada exitosamente para {nombre}")
            return True
        else:
            print(f"Error creando cotización: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Error en create_cotizacion_record: {e}")
        return False


def create_ticket_record(phone, nombre, empresa, descripcion, tipo, token):
    """Crear registro de ticket en cr321_ticket"""
    # Mapeo de tipos
    tipo_map = {
        "soporte": 462410000,
        "cotizacion": 462410001,
        "informacion": 462410002,
        "atencion_agente": 462410003
    }
    
    # Obtener siguiente ID de ticket
    try:
        search_url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_ticketses?$select=cr321_idticket&$orderby=cr321_idticket desc&$top=1"
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
        response = requests.get(search_url, headers=headers)
        
        next_id = 1
        if response.status_code == 200:
            data = response.json()
            tickets = data.get("value", [])
            if tickets:
                next_id = tickets[0].get("cr321_idticket", 0) + 1
        
        # Crear el ticket
        url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_ticketses"
        headers["Content-Type"] = "application/json"
        
        now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        
        payload = {
            "cr321_idticket": next_id,
            "cr321_fromnombre": nombre,
            "cr321_telefono": phone,
            "cr321_empresa": empresa,
            "cr321_descripcion": descripcion,
            "cr321_tipo": tipo_map.get(tipo, 462410000),
            "cr321_fechacreacion": now,
            "cr321_fechaactualizacion": now
        }
        
        # Nota: cr321_estadoId es lookup opcional, se puede asignar después manualmente
        # Si se requiere estado por defecto, buscar el GUID del estado "Nuevo" y usar:
        # payload["cr321_estadoId@odata.bind"] = f"/cr321_estados({estado_guid})"
        
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 204:
            print(f"Ticket #{next_id} creado exitosamente")
            return next_id
        else:
            print(f"Error creando ticket: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Error en create_ticket_record: {e}")
        return False


def get_menu_text():
    """Genera el texto del menú principal (solo categorías)"""
    menu_opciones = get_current_menu()
    print(f"[MENU_TEXT] Generando menú principal con {len(menu_opciones)} categorías")
    menu = "¡Bienvenido! Por favor seleccione una categoría:\n\n"
    
    for key, opcion in menu_opciones.items():
        menu += f"{key}. {opcion['nombre']}\n"
        print(f"[MENU_TEXT]   [{key}] {opcion['nombre']}")
    
    return menu


def get_submenu_text(opcion_id):
    """Genera el texto del submenú para una categoría específica"""
    menu_opciones = get_current_menu()
    
    if opcion_id not in menu_opciones:
        return get_menu_text()  # Si no existe, volver al menú principal
    
    opcion = menu_opciones[opcion_id]
    sub_opciones = opcion.get('sub_opciones', [])
    
    if not sub_opciones:
        return "Esta categoría no tiene opciones disponibles.\n\n" + get_menu_text()
    
    print(f"[SUBMENU_TEXT] Generando submenú para: {opcion['nombre']}")
    submenu = f"*{opcion['nombre']}*\n\nSeleccione una opción:\n\n"
    
    for idx, sub_opcion in enumerate(sub_opciones, 1):
        submenu += f"{idx}. {sub_opcion}\n"
        print(f"[SUBMENU_TEXT]   [{idx}] {sub_opcion}")
    
    submenu += "\n0. Volver al menú principal"
    
    return submenu


def procesar_seleccion_elemento(phone, message_text, state, menu_opciones, handler_manager):
    """Procesa la selección de un elemento del submenú"""
    categoria_id = state.get("categoria_id")
    
    if categoria_id not in menu_opciones:
        del conversation_states[phone]
        return get_menu_text()
    
    opcion = menu_opciones[categoria_id]
    sub_opciones = opcion.get('sub_opciones', [])
    handlers_config = opcion.get('handlers_config', {})
    
    # Si escribe "0", volver al menú principal
    if message_text.strip() == "0":
        del conversation_states[phone]
        return get_menu_text()
    
    # Intentar convertir a número (selección por índice)
    try:
        idx = int(message_text.strip())
        if 1 <= idx <= len(sub_opciones):
            elemento_seleccionado = sub_opciones[idx - 1]
            print(f"[SUBMENU] Elemento seleccionado por índice {idx}: {elemento_seleccionado}")
        else:
            return f"❌ Opción inválida. Por favor elige un número entre 1 y {len(sub_opciones)} (o 0 para menú principal).\n\n" + get_submenu_text(categoria_id)
    except ValueError:
        # No es número, intentar buscar por nombre exacto
        elemento_seleccionado = None
        for sub_opcion in sub_opciones:
            if message_text.strip().lower() == sub_opcion.lower():
                elemento_seleccionado = sub_opcion
                print(f"[SUBMENU] Elemento seleccionado por nombre: {elemento_seleccionado}")
                break
        
        if not elemento_seleccionado:
            return f"❌ Opción no encontrada. Por favor elige un número entre 1 y {len(sub_opciones)}.\n\n" + get_submenu_text(categoria_id)
    
    # Buscar handler para este elemento
    handler_code = handlers_config.get(elemento_seleccionado)
    
    if handler_code and handler_manager.handler_existe(handler_code):
        print(f"[HANDLER] Iniciando handler {handler_code} para '{elemento_seleccionado}'")
        
        # Obtener preguntas del handler
        preguntas = handler_manager.get_preguntas(handler_code)
        
        if preguntas:
            # Actualizar estado para conversación con handler
            conversation_states[phone] = {
                "modo": "conversacion_handler",
                "opcion": categoria_id,
                "sub_opcion": elemento_seleccionado,
                "handler_code": handler_code,
                "step": 0,
                "respuestas": {},
                "grupo_id": opcion.get("grupo_id")
            }
            
            return preguntas[0]
        else:
            # Handler sin preguntas, ejecutar inmediatamente
            mensaje = handler_manager.ejecutar_handler(
                codigo=handler_code,
                from_user=phone,
                respuestas={},
                grupo_id=opcion.get("grupo_id")
            )
            
            del conversation_states[phone]
            
            if mensaje:
                return f"{mensaje}\n\n{get_menu_text()}"
            else:
                return f"✅ {elemento_seleccionado}\n\nGracias por tu interés.\n\n{get_menu_text()}"
    else:
        # No tiene handler configurado, respuesta simple
        del conversation_states[phone]
        return f"✅ {elemento_seleccionado}\n\nGracias por tu interés.\n\n{get_menu_text()}"


def process_menu_response(phone, message_text):
    """Procesa la respuesta del usuario en el menú (con soporte para handlers)"""
    print(f"[MENU_RESPONSE] Procesando mensaje de {phone}: '{message_text}'")
    menu_opciones = get_current_menu()
    print(f"[MENU_RESPONSE] Menu opciones disponibles: {list(menu_opciones.keys())}")
    
    handler_manager = get_handler_manager()
    
    # Verificar si el usuario está respondiendo preguntas de un handler
    if phone in conversation_states:
        state = conversation_states[phone]
        
        # Si está en modo "esperando_categoria" o "esperando_elemento", manejar diferente
        if state.get("modo") == "esperando_elemento":
            return procesar_seleccion_elemento(phone, message_text, state, menu_opciones, handler_manager)
        
        # Si ya está en conversación con handler (respondiendo preguntas)
        opcion_id = state.get("opcion")
        
        if opcion_id not in menu_opciones:
            del conversation_states[phone]
            return get_menu_text()
        
        opcion = menu_opciones[opcion_id]
        
        # 🆕 SOPORTE PARA HANDLERS: Si hay handler_code, usar handler manager
        handler_code = state.get("handler_code")
        
        if handler_code:
            print(f"[HANDLER] Usando handler {handler_code} para conversación")
            
            # Obtener preguntas del handler
            preguntas = handler_manager.get_preguntas(handler_code)
            
            if not preguntas:
                # Si no hay preguntas o hay error, limpiar y mostrar menú
                del conversation_states[phone]
                return f"⚠️ Error con el handler {handler_code}.\n\n{get_menu_text()}"
            
            step = state.get("step", 0)
            
            # Si hay preguntas pendientes
            if step < len(preguntas):
                pregunta_actual = preguntas[step]
                
                # Guardar respuesta del usuario
                state["respuestas"][pregunta_actual] = message_text
                print(f"[HANDLER] Respuesta guardada: {pregunta_actual[:30]}... = {message_text[:30]}...")
                
                # Si es el último paso, ejecutar handler
                if step == len(preguntas) - 1:
                    print(f"[HANDLER] Última pregunta contestada, ejecutando handler {handler_code}")
                    
                    # Ejecutar handler con grupo_id de Dataverse
                    grupo_id = state.get("grupo_id")
                    mensaje_respuesta = handler_manager.ejecutar_handler(
                        codigo=handler_code,
                        from_user=phone,
                        respuestas=state["respuestas"],
                        grupo_id=grupo_id
                    )
                    
                    # Limpiar estado
                    del conversation_states[phone]
                    
                    if mensaje_respuesta:
                        return f"{mensaje_respuesta}\n\n{get_menu_text()}"
                    else:
                        return f"⚠️ Error al procesar su solicitud.\n\n{get_menu_text()}"
                
                else:
                    # Avanzar al siguiente paso
                    state["step"] = step + 1
                    siguiente_pregunta = preguntas[state["step"]]
                    return siguiente_pregunta
        
        else:
            # FLUJO LEGACY (sin handlers)
            preguntas = opcion.get("preguntas", [])
            step = state.get("step", 0)
            
            # Si hay preguntas pendientes
            if step < len(preguntas):
                pregunta_actual = preguntas[step]
                
                # Guardar respuesta anterior (si no es el primer paso)
                if step > 0:
                    pregunta_anterior = preguntas[step - 1]
                    state["data"][pregunta_anterior] = message_text
                
                # Si es el último paso, guardar y crear ticket
                if step == len(preguntas) - 1:
                    state["data"][pregunta_actual] = message_text
                    
                    # Crear ticket con los datos recopilados
                    ticket_data = {
                        "tipo": opcion.get("tipo"),
                        **state["data"]
                    }
                    ticket_id = create_ticket_from_conversation(phone, ticket_data)
                    
                    # Limpiar estado
                    del conversation_states[phone]
                    
                    if ticket_id:
                        return f"¡Gracias! Su solicitud ha sido registrada con el ticket #{ticket_id}. Nos pondremos en contacto pronto.\n\n{get_menu_text()}"
                    else:
                        return f"Lo sentimos, hubo un error al procesar su solicitud. Por favor intente nuevamente.\n\n{get_menu_text()}"
                else:
                    # Avanzar al siguiente paso
                    state["step"] = step + 1
                    siguiente_pregunta = preguntas[state["step"]]
                    return opcion["mensajes"].get(siguiente_pregunta, "Por favor proporcione la información:")
    
    # Si no hay conversación activa, verificar si es selección de categoría principal
    if message_text.strip() in menu_opciones:
        opcion_id = message_text.strip()
        opcion = menu_opciones[opcion_id]
        
        print(f"[MENU] Categoría seleccionada: {opcion['nombre']}")
        
        # Guardar estado "esperando elemento"
        conversation_states[phone] = {
            "modo": "esperando_elemento",
            "categoria_id": opcion_id,
            "categoria_nombre": opcion['nombre']
        }
        
        # Mostrar submenú con elementos de esta categoría
        return get_submenu_text(opcion_id)
    
    # Si escribe "0" o "menu", volver al menú principal
    if message_text.strip() in ["0", "menu", "menú", "inicio"]:
        if phone in conversation_states:
            del conversation_states[phone]
        return get_menu_text()
    
    # Si no es una opción válida, mostrar menú principal
    return get_menu_text()


@bp_webhook.route('/webhook', methods=['GET'])
def verify_webhook():
    """Verificación del webhook de WhatsApp"""
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    from goot import VERIFY_TOKEN
    
    if mode == 'subscribe' and token == VERIFY_TOKEN:
        print("Webhook verificado exitosamente")
        return challenge, 200
    else:
        return jsonify({'error': 'Token de verificación inválido'}), 403


@bp_webhook.route('/webhook', methods=['POST'])
def whatsapp_webhook():
    """Procesar mensajes entrantes de WhatsApp"""
    data = request.get_json()
    
    try:
        # Extraer información del mensaje
        if data and 'entry' in data:
            for entry in data['entry']:
                for change in entry.get('changes', []):
                    value = change.get('value', {})
                    messages = value.get('messages', [])
                    
                    for message in messages:
                        phone = message.get('from')
                        message_type = message.get('type')
                        
                        # Solo procesar mensajes de texto
                        if message_type == 'text':
                            text_body = message.get('text', {}).get('body', '')
                            
                            # Obtener nombre del perfil si está disponible
                            contacts = value.get('contacts', [])
                            nombre = None
                            if contacts:
                                nombre = contacts[0].get('profile', {}).get('name')
                            
                            # Procesar respuesta del menú
                            response_text = process_menu_response(phone, text_body)
                            
                            # Enviar respuesta
                            send_whatsapp_message(phone, response_text)
                            
                            # 🚀 NUEVO: Guardar mensaje con contacto asociado automáticamente
                            try:
                                from api.webhook_enhanced import procesar_mensaje_whatsapp_mejorado
                                
                                exito, contacto_id, _ = procesar_mensaje_whatsapp_mejorado(
                                    data,
                                    phone,
                                    text_body,
                                    nombre
                                )
                                
                                if exito:
                                    print(f"✅ Mensaje y contacto procesados correctamente: {contacto_id}")
                                else:
                                    print(f"⚠️ Error al procesar mensaje/contacto para {phone}")
                                    # Fallback al método antiguo
                                    save_incoming_message(data)
                                    crear_contacto_automatico(phone, nombre)
                            except Exception as e:
                                print(f"❌ Error en webhook mejorado: {e}")
                                print(f"⚠️ Usando método fallback...")
                                # Fallback al método antiguo si hay error
                                save_incoming_message(data)
                                try:
                                    contacto_id = crear_contacto_automatico(phone, nombre)
                                    if contacto_id:
                                        print(f"✅ Contacto procesado (fallback): {contacto_id}")
                                except Exception as e2:
                                    print(f"❌ Error en fallback: {e2}")
        
        return jsonify({'message': 'Mensaje procesado'}), 200
    
    except Exception as e:
        print(f"Error en webhook: {e}")
        return jsonify({'error': str(e)}), 500

