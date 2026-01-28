# ============ IMPORTACIONES ============
# Azure deployment fix - 2026-01-24
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timezone
from msal import ConfidentialClientApplication
import requests
import os

# Importar configuración desde goot.py
import goot
from goot import (
    PHONE_NUMBER_ID0, PHONE_NUMBER_ID1, PHONE_NUMBER_ID, VERIFY_TOKEN, ACCESS_TOKEN, 
    TENANT_ID, CLIENT_ID, CLIENT_SECRET, DATAVERSE_URL, ENTITY_SET, clear_screen
)
from api.auth import bp_auth
from api.users import bp_users
from api.messages import bp_messages
from api.conversations import bp_conversations
from api.webhook import bp_webhook
from api.reportes import bp_reportes
from api.settings import bp_settings

# ============ INICIALIZAR FLASK ============
app = Flask(__name__)

# CORS optimizado para desarrollo y producción
allowed_origins = [
    "http://localhost:*",  # Local development
    "http://127.0.0.1:*",
    "https://whatsapp-flask-app-f4gsb7dhhybcg6f6.eastus-01.azurewebsites.net",  # Azure backend
]

CORS(app, 
     resources={r"/api/*": {"origins": "*"}},  # API endpoints abiertos
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"])

# ============ INICIO ============
clear_screen()
print("--------------  Inicio ----------****------")
print(goot.mostrar_variables())

# ============ CONSTANTES ============
# Mapeo de grupos: string <-> integer (Dataverse)
GROUP_TO_INT = {
    "SERVICIOS": 1,
    "COTIZACIONES": 2,
    "SOPORTE": 3,
    "GENERAL": None,
    "TODOS": None
}

INT_TO_GROUP = {
    1: "SERVICIOS",
    2: "COTIZACIONES",
    3: "SOPORTE",
    None: "GENERAL"
}

# Mapeo de tipos de mensaje
MESSAGE_TYPES = {
    "text": 462410000,
    "image": 462410001,
    "audio": 462410002
}

# Mapeo de dirección
MESSAGE_DIRECTION = {
    "incoming": 462410000,
    "outgoing": 462410001
}

# ============ FUNCIONES AUXILIARES ============

def convert_timestamp(timestamp):
    """Convierte timestamp Unix a formato ISO para Dataverse"""
    if str(timestamp).isdigit():
        return datetime.fromtimestamp(int(timestamp), tz=timezone.utc).isoformat().replace("+00:00", "Z")
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def parse_group_filter(group_filter):
    """Convierte grupo string a integer, None si no aplica filtro"""
    if not group_filter or group_filter.upper() in ["TODOS", "NONE", "NULL"]:
        return None
    
    if group_filter.isdigit():
        return int(group_filter)
    
    return GROUP_TO_INT.get(group_filter.upper())

def get_token():
    """Obtiene token de autenticación de Azure AD para Dataverse"""
    try:
        authority = f"https://login.microsoftonline.com/{TENANT_ID}"
        app_auth = ConfidentialClientApplication(
            CLIENT_ID, 
            authority=authority, 
            client_credential=CLIENT_SECRET
        )
        token = app_auth.acquire_token_for_client(scopes=[f"{DATAVERSE_URL}/.default"])
       
        if "access_token" in token:
            print("[TOKEN] Token obtenido exitosamente")
            return token["access_token"]
        else:
            error_desc = token.get("error_description", "Sin descripcion")
            error_code = token.get("error", "Sin codigo")
            print(f"[TOKEN ERROR] Codigo: {error_code}, Descripcion: {error_desc}")
            return None
            
    except Exception as e:
        print(f"[TOKEN EXCEPTION] {e}")
        return None

def determine_group_from_message(text):
    """Determina el grupo según el número de opción seleccionada por el usuario"""
    text_lower = str(text).lower().strip()
    
    option_to_group = {
        "1": "SERVICIOS",
        "2": "COTIZACIONES",
        "3": "SOPORTE",
    }
    
    return option_to_group.get(text_lower, "GENERAL")

def save_bot_response(phone_number, fromname, bot_message, timestamp, message_id=None, group=None):
    """Guarda respuesta del bot en Dataverse"""
    token = get_token()
    if not token:
        print("[SAVE_BOT] No se pudo obtener token")
        return False
    
    timestamp_iso = convert_timestamp(timestamp)
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    payload = {
        "cr321_phone": str(phone_number),
        "cr321_fromname": fromname,
        "cr321_body": str(bot_message),
        "cr321_timestamp": timestamp_iso,
        "cr321_direction": MESSAGE_DIRECTION["outgoing"]
    }

    if message_id:
        payload["cr321_messageid"] = message_id
    
    # Agregar grupo si aplica
    grupo_int = GROUP_TO_INT.get(group) if group else None
    if grupo_int is not None:
        payload["cr321_grupo"] = grupo_int

    # Limpiar valores None o vacíos
    payload = {k: v for k, v in payload.items() if v not in [None, ""]}

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code in [200, 201, 204]:
            print(f"[SAVE_BOT] Guardado exitoso [Grupo: {group}]")
            return True
        else:
            print(f"[SAVE_BOT ERROR] {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"[SAVE_BOT EXCEPTION] {e}")
        return False

def save_to_dataverse(message_id, fromphone, timestamp, message_type, body, fromname, group=None):
    """Guarda mensaje entrante en Dataverse"""
    token = get_token()
    if not token:
        print("[SAVE_DATAVERSE] No se pudo obtener token")
        return

    timestamp_iso = convert_timestamp(timestamp)
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    payload = {
        "cr321_messageid": str(message_id),  
        "cr321_phone": fromphone,
        "cr321_timestamp": timestamp_iso,              
        "cr321_messagetype": MESSAGE_TYPES.get(message_type, MESSAGE_TYPES["text"]),
        "cr321_body": body,
        "cr321_fromname": fromname,
        "cr321_direction": MESSAGE_DIRECTION["incoming"]
    }
    
    # Agregar grupo si aplica
    grupo_int = GROUP_TO_INT.get(group) if group else None
    if grupo_int is not None:
        payload["cr321_grupo"] = grupo_int
    
    # Limpiar valores None o vacíos
    payload = {k: v for k, v in payload.items() if v not in [None, ""]}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"[SAVE_DATAVERSE] {response.status_code} - De: {fromname} ({fromphone}) - Grupo: {group}")
    except Exception as e:
        print(f"[SAVE_DATAVERSE ERROR] {e}")

def send_reply(phonenumber, text, timestamp, fromname="", group=None):
    """Envía respuesta automática por WhatsApp"""
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}

    greeting = f"Hola {fromname}! que servicio requiere" if fromname else "Hola! que servicio requiere"

    if text in ["hola", "menu", "mm"]:
        message = f"{greeting} Opciones:\n1. PERSONAS\n2. EMPRESAS\n3. COORDINACION"
    elif text == "1":
        message = "Has seleccionado PERSONAS. En que podemos ayudarte?"
    elif text == "2":
        message = "Has seleccionado EMPRESAS. Envianos los detalles."
    elif text == "3":
        message = "Has seleccionado COORDINACION. Te contactaremos pronto."
    else:
        message = "No entendi tu mensaje. Escribe 'menu' para ver opciones."
    
    payload = {
        "messaging_product": "whatsapp",
        "to": phonenumber,
        "type": "text",
        "text": {"body": message}
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"[SEND_REPLY] {response.status_code} -> {fromname}")
            
        if response.status_code == 200:
            message_id = response.json().get("messages", [{}])[0].get("id")
            save_bot_response(phonenumber, fromname, message, timestamp, message_id, group)
    except Exception as e:
        print(f"[SEND_REPLY ERROR] {e}")


# ============ RUTAS / ENDPOINTS ============

# ============ HEALTH CHECK ============
@app.route("/", methods=["GET"])
@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint para Azure App Services y monitoreo"""
    is_production = os.environ.get("WEBSITE_INSTANCE_ID") is not None
    return jsonify({
        "status": "healthy",
        "service": "WhatsApp Manager API",
        "environment": "AZURE" if is_production else "LOCAL",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "1.0.0"
    }), 200

@app.route("/api/status", methods=["GET"])
def api_status():
    """Status detallado incluyendo conexión a Dataverse"""
    token = get_token()
    dataverse_connected = token is not None
    
    return jsonify({
        "status": "operational",
        "dataverse": "connected" if dataverse_connected else "disconnected",
        "phone_id": PHONE_NUMBER_ID[:10] + "..." if PHONE_NUMBER_ID else "not configured",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200

# ============ ENDPOINT LOGIN USUARIO ============
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    correo = data.get("correo")
    clave = data.get("clave")
    print(f"[LOGIN] Correo recibido: {correo} Clave recibida: {clave}")
    from goot import get_user_by_email
    user = get_user_by_email(correo)
    print(f"[LOGIN] Usuario encontrado: {user}")
    if user:
        clave_db = user.get("cr321_clave")
        print(f"[LOGIN] Clave almacenada: {clave_db}")
        if clave_db == clave:
            return jsonify({"success": True, "nombre": user.get("cr321_nombre"), "rol": user.get("cr321_rol"), "correo": user.get("cr321_correo")})
        else:
            print("[LOGIN] Clave incorrecta")
            return jsonify({"success": False, "error": "Clave incorrecta"})
    else:
        print("[LOGIN] Usuario no encontrado")
        return jsonify({"success": False, "error": "Usuario no encontrado"})

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        token_sent = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        return challenge if token_sent == VERIFY_TOKEN else "Invalid token"

    if request.method == "POST":
        data = request.get_json()
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                messages = value.get("messages", [])
                    
                contacts = value.get("contacts", [])
                fromname = ""
                if contacts:
                    fromname = contacts[0].get("profile", {}).get("name", "Sin nombre")

                for message in messages:
                    message_id = message.get("id")
                    fromphone = message.get("from")
                    timestamp = message.get("timestamp")    
                    message_type = message.get("type", "")
                    body = message.get("text", {}).get("body", "").lower()
                    
                    # Determinar grupo basado en el contenido del mensaje
                    group = determine_group_from_message(body)
                    print(f"[WEBHOOK] Mensaje recibido de {fromphone}: '{body}' -> Grupo: {group}")
                    
                    save_to_dataverse(message_id, fromphone, timestamp, message_type, body, fromname, group)
                    send_reply(fromphone, body, timestamp, fromname, group)
                    
        return "OK", 200

# ============ ENDPOINTS REST PARA APP MÓVIL ============

@app.route("/api/conversations", methods=["GET"])
def get_conversations():
    """Obtiene las últimas conversaciones de WhatsApp, agrupadas por grupo"""
    print("[API] Solicitud de conversaciones recibida")
    
    token = get_token()
    if not token:
        return jsonify({"error": "Error de autenticacion"}), 500
    
    limit = request.args.get('limit', 50)
    group_filter = request.args.get('group', None)
    grupo_int = parse_group_filter(group_filter)
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$top={limit}&$orderby=cr321_timestamp desc"
    
    if grupo_int is not None:
        url += f"&$filter=cr321_grupo eq {grupo_int}"
        print(f"[CONVERSATIONS] Filtrando por grupo: {grupo_int}")
    else:
        print(f"[CONVERSATIONS] Mostrando TODOS los grupos")
    
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            records = data.get("value", [])
            print(f"[CONVERSATIONS] Registros encontrados: {len(records)}")
            
            conversations = {}
            groups = set()
            
            for record in records:
                phone = record.get("cr321_phone")
                group_int = record.get("cr321_grupo")
                group = INT_TO_GROUP.get(group_int, "GENERAL")
                groups.add(group)
                
                if phone:
                    conv_key = f"{phone}_{group}"
                    
                    if conv_key not in conversations:
                        conversations[conv_key] = {
                            "phone": phone,
                            "name": record.get("cr321_fromname", "Desconocido"),
                            "last_message": record.get("cr321_body", ""),
                            "timestamp": record.get("cr321_timestamp"),
                            "group": group,
                            "unread": 0
                        }
            
            conv_list = list(conversations.values())
            print(f"[CONVERSATIONS] Conversaciones unicas: {len(conv_list)}")
            
            return jsonify({
                "success": True,
                "conversations": conv_list,
                "groups": list(groups)
            })
        else:
            print(f"[CONVERSATIONS ERROR] {response.text}")
            return jsonify({"error": "Error al consultar Dataverse"}), 500
            
    except Exception as e:
        print(f"[CONVERSATIONS EXCEPTION] {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/messages/<phone_number>", methods=["GET"])
def get_messages(phone_number):
    """Obtiene todos los mensajes de un número específico, opcionalmente filtrado por grupo"""
    print(f"[API] Solicitud de mensajes para: {phone_number}")
    
    token = get_token()
    if not token:
        return jsonify({"error": "Error de autenticacion"}), 500
    
    group_filter = request.args.get('group', None)
    grupo_int = parse_group_filter(group_filter)
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$filter=cr321_phone eq '{phone_number}'"
    
    if grupo_int is not None:
        url += f" and cr321_grupo eq {grupo_int}"
        print(f"[MESSAGES] Filtrando por grupo: {grupo_int}")
    
    url += "&$orderby=cr321_timestamp asc"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            records = data.get("value", [])
            print(f"[MESSAGES] Mensajes encontrados: {len(records)}")
            
            messages = []
            for record in records:
                messages.append({
                    "id": record.get("cr321_messageid"),
                    "body": record.get("cr321_body"),
                    "timestamp": record.get("cr321_timestamp"),
                    "direction": "incoming" if record.get("cr321_direction") == MESSAGE_DIRECTION["incoming"] else "outgoing",
                    "type": record.get("cr321_messagetype")
                })
            
            return jsonify({"success": True, "messages": messages})
        else:
            return jsonify({"error": "Error al consultar mensajes"}), 500
            
    except Exception as e:
        print(f"[MESSAGES EXCEPTION] {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/send_message", methods=["POST"])
def send_manual_message():
    """Envía un mensaje desde la app móvil"""
    data = request.get_json()
    phone = data.get("phone")
    message = data.get("message")
    group = data.get("group", "GENERAL")  # Grupo por defecto
    
    print(f"\n{'='*60}")
    print(f"[SEND_MESSAGE] NUEVA SOLICITUD DE ENVÍO")
    print(f"[SEND_MESSAGE] Recibiendo solicitud: phone={phone}, message={message}, group={group}")
    print(f"[DEBUG GRUPO SEND] Valor recibido: '{group}' (tipo: {type(group)})")
    print(f"[DEBUG GRUPO SEND] Datos completos del request: {data}")
    print(f"{'='*60}\n")
    
    if not phone or not message:
        return jsonify({"error": "Faltan parámetros"}), 400
    
    # Asegurar formato correcto del número (debe incluir código de país sin +)
    clean_phone = phone.replace("+", "").replace("-", "").replace(" ", "")
    print(f"[SEND_MESSAGE] Número limpio: {clean_phone}")
    
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": clean_phone,
        "type": "text",
        "text": {"body": message}
    }
    
    print(f"[SEND_MESSAGE] Enviando a WhatsApp API: {url}")
    print(f"[SEND_MESSAGE] Payload: {payload}")
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"[SEND_MESSAGE] Respuesta de WhatsApp: {response.status_code}")
        print(f"[SEND_MESSAGE] Contenido: {response.text}")
        
        if response.status_code == 200:
            message_id = response.json().get("messages", [{}])[0].get("id")
            timestamp = int(datetime.now(timezone.utc).timestamp())
            print(f"[SEND_MESSAGE] Guardando en Dataverse: message_id={message_id}, grupo={group}")
            save_result = save_bot_response(clean_phone, "", message, timestamp, message_id, group)
            print(f"[SEND_MESSAGE] Resultado de guardar en Dataverse: {save_result}")
            
            return jsonify({
                "success": True,
                "message_id": message_id
            })
        else:
            return jsonify({
                "success": False,
                "error": response.json()
            }), 500
            
    except Exception as e:
        print(f"[SEND_MESSAGE] Excepción: {e}")
        return jsonify({"error": str(e)}), 500

# Registrar blueprints
app.register_blueprint(bp_auth)
app.register_blueprint(bp_users)
app.register_blueprint(bp_messages)
app.register_blueprint(bp_conversations)
app.register_blueprint(bp_webhook)
app.register_blueprint(bp_reportes)
app.register_blueprint(bp_settings)

# ============ EJECUTAR APLICACIÓN ============
if __name__ == "__main__":
    # Debug mode solo en desarrollo local
    is_production = os.environ.get("WEBSITE_INSTANCE_ID") is not None  # Variable de Azure App Services
    debug_mode = False  # Desactivar debug temporalmente para Windows
    
    print(f"[STARTUP] Modo: {'PRODUCCION (Azure)' if is_production else 'DESARROLLO (Local)'}")
    print(f"[STARTUP] Debug: {'Desactivado' if not debug_mode else 'Activado'}")
    print(f"[STARTUP] Iniciando servidor en http://localhost:5000")
    
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=debug_mode, use_reloader=False)