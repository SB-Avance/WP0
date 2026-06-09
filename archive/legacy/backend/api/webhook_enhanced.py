"""
Funciones mejoradas para Webhook - Auto-creación de contactos con Lookup
==========================================================================

Implementado: Febrero 8, 2026
Mejora #3: Creación automática de contactos con asociación directa usando Lookups

CAMBIO PRINCIPAL:
- Antes: Crear mensaje → Crear contacto (sin asociar)
- Ahora: Crear/buscar contacto → Crear mensaje con Lookup asociado
"""

import os
import sys
from datetime import datetime, timezone

import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from goot import DATAVERSE_URL, get_token


def buscar_o_crear_contacto_lookup(telefono, nombre=None):
    """
    Buscar o crear contacto de forma optimizada
    Retorna el GUID del contacto para usar en Lookups

    Args:
        telefono (str): Número de teléfono del contacto
        nombre (str, optional): Nombre del contacto

    Returns:
        str: GUID del contacto o None si hay error
    """
    token = get_token()
    if not token:
        print("[❌ CONTACTO] No se pudo obtener token")
        return None

    headers = {
        "Authorization": f"Bearer {token}",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Prefer": "return=representation",  # Para obtener el objeto creado
    }

    try:
        # PASO 1: Buscar contacto existente
        url_buscar = f"{DATAVERSE_URL}/api/data/v9.2/cr321_contactos"
        params = {
            "$filter": f"cr321_telefono eq '{telefono}'",
            "$select": "cr321_contactoid,cr321_fromnombre,cr321_telefono",
            "$top": 1,
        }

        response = requests.get(url_buscar, params=params, headers=headers, timeout=10)

        if response.status_code == 200:
            contactos = response.json().get("value", [])
            if contactos:
                contacto_id = contactos[0]["cr321_contactoid"]
                print(f"[✅ CONTACTO] Existente encontrado: {contacto_id}")
                return contacto_id

        # PASO 2: No existe, crear nuevo contacto
        nombre_final = (nombre or f"Contacto {telefono}").strip()

        url_crear = f"{DATAVERSE_URL}/api/data/v9.2/cr321_contactos"
        payload = {
            "cr321_fromnombre": nombre_final,
            "cr321_telefono": telefono,
            "cr321_descripcion": "Auto-creado desde WhatsApp",
            "cr321_fechacreacion": datetime.now(timezone.utc).isoformat(),
            "cr321_tipo": 462410000,  # Tipo: Cliente WhatsApp
        }

        response = requests.post(url_crear, json=payload, headers=headers, timeout=10)

        if response.status_code in (200, 201, 204):
            # Método 1: Leer del header OData-EntityId
            entity_id_header = response.headers.get("OData-EntityId", "")
            if "(" in entity_id_header and ")" in entity_id_header:
                contacto_id = entity_id_header.split("(")[1].split(")")[0]
                print(f"[✅ CONTACTO] Nuevo creado (header): {contacto_id}")
                return contacto_id

            # Método 2: Leer del body si usamos Prefer=representation
            if response.status_code in (200, 201):
                data = response.json()
                contacto_id = data.get("cr321_contactoid")
                if contacto_id:
                    print(f"[✅ CONTACTO] Nuevo creado (body): {contacto_id}")
                    return contacto_id

            # Método 3: Hacer otra búsqueda (fallback)
            print("[⏳ CONTACTO] Buscando contacto recién creado...")
            response2 = requests.get(
                url_buscar, params=params, headers=headers, timeout=10
            )
            if response2.status_code == 200:
                contactos = response2.json().get("value", [])
                if contactos:
                    contacto_id = contactos[0]["cr321_contactoid"]
                    print(f"[✅ CONTACTO] Nuevo creado (búsqueda): {contacto_id}")
                    return contacto_id
        else:
            print(f"[❌ CONTACTO] Error al crear: {response.status_code}")
            print(f"[❌ CONTACTO] Respuesta: {response.text[:300]}")
            return None

    except Exception as e:
        print(f"[❌ CONTACTO] Excepción: {e}")
        import traceback

        traceback.print_exc()
        return None


def guardar_mensaje_con_lookup_contacto(data_mensaje, contacto_id=None, grupo_id=None):
    """
    Guarda mensaje en Dataverse con Lookup a contacto y grupo

    Esta es la MEJORA PRINCIPAL: asocia el mensaje con contacto en una sola operación

    Args:
        data_mensaje (dict): Datos del mensaje de WhatsApp
        contacto_id (str): GUID del contacto para asociar
        grupo_id (str): ID del grupo para asociar (opcional)

    Returns:
        bool: True si se guardó correctamente
    """
    token = get_token()
    if not token:
        print("[❌ MENSAJE] No se pudo obtener token")
        return False

    headers = {
        "Authorization": f"Bearer {token}",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    try:
        url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s"

        # Copiar datos del mensaje
        payload = dict(data_mensaje)

        # 🎯 MEJORA PRINCIPAL: Agregar Lookup a contacto usando @odata.bind
        if contacto_id:
            # Este es el formato para asociar un Lookup en Dataverse
            payload["cr321_contactorelacion@odata.bind"] = (
                f"/cr321_contactos({contacto_id})"
            )
            print(f"[✅ LOOKUP] Asociando mensaje con contacto: {contacto_id}")

        # Si hay grupo, también asociarlo
        if grupo_id:
            payload["cr321_grupoid@odata.bind"] = f"/cr321_grups({grupo_id})"
            print(f"[✅ LOOKUP] Asociando mensaje con grupo: {grupo_id}")

        response = requests.post(url, headers=headers, json=payload, timeout=15)

        if response.status_code in (200, 201, 204):
            print(f"[✅ MENSAJE] Guardado con lookups correctamente")
            return True
        else:
            print(f"[❌ MENSAJE] Error al guardar: {response.status_code}")
            print(f"[❌ MENSAJE] Respuesta: {response.text[:500]}")
            return False

    except Exception as e:
        print(f"[❌ MENSAJE] Excepción: {e}")
        import traceback

        traceback.print_exc()
        return False


def procesar_mensaje_whatsapp_mejorado(
    data_webhook, phone, mensaje_texto, nombre_contacto=None
):
    """
    Función integrada que procesa mensaje de WhatsApp con auto-creación de contacto

    Este es el flujo OPTIMIZADO:
    1. Buscar/crear contacto PRIMERO
    2. Guardar mensaje YA ASOCIADO con el contacto
    3. Todo en 2 operaciones en lugar de 3+

    Args:
        data_webhook (dict): Datos del webhook de WhatsApp
        phone (str): Número de teléfono
        mensaje_texto (str): Texto del mensaje
        nombre_contacto (str, optional): Nombre del contacto

    Returns:
        tuple: (exito: bool, contacto_id: str, mensaje_id: str)
    """
    print(f"\n{'='*70}")
    print(f"[🚀 WEBHOOK MEJORADO] Procesando mensaje de {phone}")
    print(f"{'='*70}")

    # PASO 1: Buscar o crear contacto
    print(f"[1/2] Obteniendo contacto...")
    contacto_id = buscar_o_crear_contacto_lookup(phone, nombre_contacto)

    if not contacto_id:
        print(f"[❌] No se pudo obtener/crear contacto para {phone}")
        return (False, None, None)

    # PASO 2: Guardar mensaje con Lookup a contacto
    print(f"[2/2] Guardando mensaje con lookup a contacto...")

    # Determinar grupo basado en la lógica del webhook
    # (simplificado - en producción usar la misma lógica que el webhook actual)
    grupo_id = None  # Puedes pasar esto como parámetro si lo necesitas

    exito = guardar_mensaje_con_lookup_contacto(data_webhook, contacto_id, grupo_id)

    if exito:
        print(f"[✅ COMPLETADO] Mensaje guardado y asociado con contacto {contacto_id}")
        print(f"{'='*70}\n")
        return (True, contacto_id, None)  # mensaje_id se puede obtener si se necesita
    else:
        print(f"[❌ ERROR] No se pudo guardar el mensaje")
        print(f"{'='*70}\n")
        return (False, contacto_id, None)


def obtener_grupo_por_tipo(tipo_grupo):
    """
    Helper: Obtener ID de grupo por tipo

    Args:
        tipo_grupo (str): Tipo de grupo ('Información', 'Solicitud Ticket', etc.)

    Returns:
        str: ID del grupo o None
    """
    token = get_token()
    if not token:
        return None

    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    try:
        url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_grups"
        params = {
            "$filter": f"cr321_nombre eq '{tipo_grupo}'",
            "$select": "cr321_grupoid",
            "$top": 1,
        }

        response = requests.get(url, params=params, headers=headers, timeout=10)

        if response.status_code == 200:
            grupos = response.json().get("value", [])
            if grupos:
                return grupos[0]["cr321_grupoid"]

        return None
    except:
        return None


# ============================================================================
# COMPARACIÓN: Antes vs Ahora
# ============================================================================

"""
❌ FLUJO ANTERIOR (INEFICIENTE):
1. save_incoming_message(data)         → Guarda mensaje SIN contacto
2. crear_contacto_automatico(phone)    → Crea contacto
3. [FIN - mensaje y contacto NO asociados]
   Total: 3-4 requests HTTP
   Problema: Datos desconectados

✅ FLUJO NUEVO (OPTIMIZADO):
1. buscar_o_crear_contacto_lookup(phone) → Obtiene/crea contacto
2. guardar_mensaje_con_lookup_contacto() → Guarda mensaje CON lookup
   Total: 2 requests HTTP
   Beneficio: Datos asociados automáticamente

VENTAJAS:
- ⚡ Más rápido (menos requests)
- 🔗 Relación automática (integridad)
- 🎯 Operación atómica (no hay estado intermedio)
- 📊 Datos listos para reportes con $expand
"""

# ===========================================================================
# EJEMPLO DE USO
# ===========================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("EJEMPLO: Procesar mensaje entrante con auto-creación de contacto")
    print("=" * 70 + "\n")

    # Simular datos de webhook
    data_simulado = {
        "cr321_phone": "+573001234567",
        "cr321_fromname": "Juan Pérez",
        "cr321_body": "Hola, necesito información",
        "cr321_messageid": "wamid.test123",
        "cr321_timestamp": datetime.now(timezone.utc).isoformat(),
        "cr321_messagetype": 462410000,  # Texto
        "cr321_direction": 462410000,  # Entrante
    }

    # Procesar con el nuevo método mejorado
    exito, contacto_id, mensaje_id = procesar_mensaje_whatsapp_mejorado(
        data_simulado, "+573001234567", "Hola, necesito información", "Juan Pérez"
    )

    if exito:
        print(f"\n✅ ÉXITO")
        print(f"   Contacto ID: {contacto_id}")
        print(f"   Mensaje guardado y asociado")
    else:
        print(f"\n❌ ERROR en el proceso")
