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
CORS(app)  # Permitir peticiones desde otras aplicaciones

# ============ INICIO ============
clear_screen()
print("--------------  Inicio ----------****------")
print(goot.mostrar_variables())

# ============ FUNCIONES AUXILIARES ============

def get_token():
    try:
        authority = f"https://login.microsoftonline.com/{TENANT_ID}"
        app_auth = ConfidentialClientApplication(
            CLIENT_ID, 
            authority=authority, 
            client_credential=CLIENT_SECRET
        )
        token = app_auth.acquire_token_for_client(scopes=[f"{DATAVERSE_URL}/.default"])
        print("📋 ********** Respuesta MSAL completa::", str(token)[:55])
       
        if "access_token" in token:
            print("✅ ********** Token obtenido exitosamente ")
            return token["access_token"]
        else:
            error_desc = token.get("error_description", "Sin descripción")
            error_code = token.get("error", "Sin código")
            print(f"❌ -/-/-/-/ Error al obtener token Codigo : {error_code}")
            print(f"❌ -/-/-/-/ Error al obtener token Descripcion: {error_desc}")
            return None
            
    except Exception as e:
        print(f"💥 ********** Excepción en get_token: {e}")
        return None

def save_bot_response(phone_number, fromname, bot_message, timestamp, message_id=None, group=None):
    token = get_token()
    if not token:
        print("⚠️ No se pudo obtener token para guardar respuesta del bot.")
        return
    
    timestamp_iso = None
    if str(timestamp).isdigit():
        timestamp_iso = datetime.fromtimestamp(int(timestamp), tz=timezone.utc).isoformat().replace("+00:00", "Z")
    else:
        timestamp_iso = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    direction_map = {
        "incoming": 462410000,
        "outgoing": 462410001
    }
    
    payload = {
        "cr321_phone": str(phone_number),
        "cr321_fromname": fromname,
        "cr321_body": str(bot_message),
        "cr321_timestamp": timestamp_iso,
        "cr321_direction": direction_map["outgoing"]
    }

    if message_id:
        payload["cr321_messageid"] = message_id
    
    if group:
        payload["cr321_grupo"] = str(group)

    payload = {k: v for k, v in payload.items() if v not in [None, ""]}

    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"✅ ********** Respuesta guardada en Dataverse: {response.status_code} [Grupo: {group}]")
    except Exception as e:
        print(f"❌ Error al guardar respuesta del bot: {e}")

def save_to_dataverse(message_id, fromphone, timestamp, message_type, body, fromname, group=None):
    token = get_token()
  
    if not token:
        print("⚠️ **********  No se pudo obtener token, no se guarda en Dataverse.")
        return

    timestamp_iso = None
    if str(timestamp).isdigit():
        timestamp_iso = datetime.fromtimestamp(int(timestamp), tz=timezone.utc).isoformat().replace("+00:00", "Z")

    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
   
    option_map = {
        "text": 462410000,
        "image": 462410001,
        "audio": 462410002
    }
    
    payload = {
        "cr321_messageid": str(message_id),  
        "cr321_phone": fromphone,
        "cr321_timestamp": timestamp_iso,              
        "cr321_messagetype": option_map.get(message_type, 462410000),
        "cr321_body": body,
        "cr321_fromname": fromname,
        "cr321_direction": 462410000
    }
    
    if group:
        payload["cr321_grupo"] = str(group)
    
    payload = {k: v for k, v in payload.items() if v not in [None, ""]}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"✅ ********** Respuesta Dataverse: Código HTTP: {response.status_code} [Grupo: {group}]")
        print(f"✅ **** ***** De: {fromname} - Phone ({fromphone}) - Mensaje: {body}")
    except Exception as e:
        print(f"❌  ********** Error al guardar en Dataverse: {e}")

def send_reply(phonenumber, text, timestamp, fromname=""):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}

    greeting = f"👋 ¡Hola {fromname}!" if fromname else "👋 ¡Hola!"

    if text in ["hola", "menu", "mm"]:
        message = f"{greeting} Opciones:\n1️⃣ SERVICIOS A \n2️⃣ COTIZACIONES B \n3️⃣ Hablar con un asesor"
    elif text == "1":
        message = "SERVICIOS"
    elif text == "2":
        message = "COTIZACIONES"
    elif text == "3":
        message = "📞 SOLICITAR UNA LLAMADA"
    else:
        message = "❓ No entendí tu mensaje. Escribe 'menu o mm' para ver opciones."
    
    payload = {
        "messaging_product": "whatsapp",
        "to": phonenumber,
        "type": "text",
        "text": {"body": message}
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"✅ **** ***** Mensaje enviado -> {fromname} Status -> {response.status_code}")
            
        if response.status_code == 200:
            message_id = response.json().get("messages", [{}])[0].get("id")
            save_bot_response(phonenumber, fromname, message, timestamp, message_id)
    except Exception as e:
        print(f"❌ Excepción al enviar mensaje: {e}")


# ============ RUTAS / ENDPOINTS ============

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
                    
                    save_to_dataverse(message_id, fromphone, timestamp, message_type, body, fromname)
                    send_reply(fromphone, body, timestamp, fromname)
                    
        return "OK", 200

# ============ ENDPOINTS REST PARA APP MÓVIL ============

@app.route("/api/conversations", methods=["GET"])
def get_conversations():
    """Obtiene las últimas conversaciones de WhatsApp, agrupadas por grupo"""
    print("📱 ********** Solicitud de conversaciones recibida")
    
    token = get_token()
    if not token:
        print("❌ No se pudo obtener token")
        return jsonify({"error": "Error de autenticación"}), 500
    
    limit = request.args.get('limit', 50)
    group_filter = request.args.get('group', None)  # Parámetro opcional para filtrar por grupo
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s"
    url += f"?$top={limit}&$orderby=cr321_timestamp desc"
    
    # Si se especifica un grupo, filtrar por él
    if group_filter and group_filter.upper() != "TODOS":
        url += f"&$filter=cr321_grupo eq '{group_filter}'"
        print(f"🔍 Filtrando por grupo: {group_filter}")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
    try:
        print(f"🔍 Consultando Dataverse: {url}")
        response = requests.get(url, headers=headers)
        print(f"📊 Respuesta Dataverse: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            records = data.get("value", [])
            print(f"✅ Registros encontrados: {len(records)}")
            
            conversations = {}
            groups = set()  # Conjunto de grupos únicos
            
            for record in records:
                phone = record.get("cr321_phone")
                group = record.get("cr321_grupo", "GENERAL")
                groups.add(group)
                
                if phone:
                    # Usar phone+group como clave para separar conversaciones por grupo
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
            print(f"✅ Conversaciones únicas: {len(conv_list)}")
            print(f"✅ Grupos encontrados: {list(groups)}")
            
            return jsonify({
                "success": True,
                "conversations": conv_list,
                "groups": list(groups)  # Lista de grupos disponibles
            })
        else:
            print(f"❌ Error en Dataverse: {response.text}")
            return jsonify({"error": "Error al consultar Dataverse"}), 500
            
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/messages/<phone_number>", methods=["GET"])
def get_messages(phone_number):
    """Obtiene todos los mensajes de un número específico, opcionalmente filtrado por grupo"""
    print(f"📱 ********** Solicitud de mensajes para: {phone_number}")
    
    token = get_token()
    if not token:
        return jsonify({"error": "Error de autenticación"}), 500
    
    group_filter = request.args.get('group', None)  # Parámetro opcional para filtrar por grupo
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s"
    url += f"?$filter=cr321_phone eq '{phone_number}'"
    
    # Si se especifica un grupo, agregar filtro
    if group_filter and group_filter.upper() != "TODOS":
        url += f" and cr321_grupo eq '{group_filter}'"
        print(f"🔍 Filtrando mensajes por grupo: {group_filter}")
    
    url += "&$orderby=cr321_timestamp asc"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            records = data.get("value", [])
            print(f"✅ Mensajes encontrados: {len(records)}")
            
            messages = []
            for record in records:
                messages.append({
                    "id": record.get("cr321_messageid"),
                    "body": record.get("cr321_body"),
                    "timestamp": record.get("cr321_timestamp"),
                    "direction": "incoming" if record.get("cr321_direction") == 462410000 else "outgoing",
                    "type": record.get("cr321_messagetype")
                })
            
            return jsonify({
                "success": True,
                "messages": messages
            })
        else:
            return jsonify({"error": "Error al consultar mensajes"}), 500
            
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/send_message", methods=["POST"])
def send_manual_message():
    """Envía un mensaje desde la app móvil"""
    data = request.get_json()
    phone = data.get("phone")
    message = data.get("message")
    group = data.get("group", "GENERAL")  # Grupo por defecto
    
    print(f"[SEND_MESSAGE] Recibiendo solicitud: phone={phone}, message={message}, group={group}")
    
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
            save_bot_response(clean_phone, "", message, timestamp, message_id, group)
            
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
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)