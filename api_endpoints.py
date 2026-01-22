# ============ IMPORTACIONES ============
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timezone
from msal import ConfidentialClientApplication
import requests
import os

# Importar configuración desde goot.py
import goot.py
from goot import (
    PHONE_NUMBER_ID0, PHONE_NUMBER_ID1, PHONE_NUMBER_ID, VERIFY_TOKEN, ACCESS_TOKEN, 
    TENANT_ID, CLIENT_ID, CLIENT_SECRET, DATAVERSE_URL, ENTITY_SET, clear_screen
)

# ============ INICIALIZAR FLASK ============
app = Flask(__name__)
CORS(app)  # Permitir peticiones desde otras aplicaciones

# ============ INICIO ============
clear_screen()
print("--------------  Inicio ----------****------")
print(goot.mostrar_variables())

# ============ FUNCIONES AUXILIARES ============

# -------------- Obtener token de acceso       
def get_token():
    try:
        authority = f"https://login.microsoftonline.com/{TENANT_ID}"
        app_auth = ConfidentialClientApplication(
            CLIENT_ID, 
            authority=authority, 
            client_credential=CLIENT_SECRET
        )
        # Scope correcto para Dataverse
        token = app_auth.acquire_token_for_client(scopes=[f"{DATAVERSE_URL}/.default"])
        print("📋 ********** ********** Respuesta MSAL completa::", str(token)[:55])
       
        if "access_token" in token:
            print("✅ ********** Token obtenido exitosamente ")
            return token["access_token"]
        else:
            # Mostrar el error específico
            error_desc = token.get("error_description", "Sin descripción")
            error_code = token.get("error", "Sin código")
            print(f"❌ -/-/-/-/ Error al obtener token Codigo : {error_code}")
            print(f"❌ -/-/-/-/ Error al obtener token Descripcion: {error_desc}")
            return None
            
    except Exception as e:
        print(f"💥 ********** Excepción en get_token: {e}")
        return None

# -------------- Guardar respuesta del bot en Dataverse
def save_bot_response(phone_number, fromname, bot_message, timestamp, message_id=None):
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
        "incoming": 462410000,  # Usuario → Bot
        "outgoing": 462410001   # Bot → Usuario
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

    payload = {k: v for k, v in payload.items() if v not in [None, ""]}

    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"✅ ********** Respuesta guardada en Dataverse: {response.status_code} - {response.text}")
        if response.status_code != 200 and response.status_code != 204:
            try:
                print("⚠️ Error en la API:", response.json())
            except ValueError:
                print("⚠️ Error en la API: Respuesta no es JSON ->", response.text)
    except Exception as e:
        print(f"❌ Error al guardar respuesta del bot: {e}")

# -------------- Guardar mensaje en Dataverse
def save_to_dataverse(message_id, fromphone, timestamp, message_type, body, fromname):
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
        "cr321_direction": 462410000  # Incoming
    }
    
    # Elimina claves con valor None para evitar errores
    payload = {k: v for k, v in payload.items() if v not in [None, ""]}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"✅ ********** Respuesta Dataverse: Código HTTP: {response.status_code} - {response.text}")
        print(f"✅ **** ***** De: {fromname} - Hora {timestamp_iso} - Phone ({fromphone}) - Mensaje: {body}")
    except Exception as e:
        print(f"❌  ********** Error al guardar en Dataverse: {e}")

# -------------- Enviar respuesta por WhatsApp
def send_reply(phonenumber, text, timestamp, fromname=""):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}

    # ✅ Personalizar mensaje con el nombre
    greeting = f"👋 ¡Hola {fromname}!" if fromname else "👋 ¡Hola!"

    if text in ["hola", "menu", "mm"]:
        message = f"{greeting} Opciones:\n1️⃣ Consultar \n2️⃣ Ver promociones\n3️⃣ Hablar con un asesor"
    elif text == "1":
        message = "💰 Opcion 1 COP"
    elif text == "2":
        message = "🎉 Opcion 2  2x1 \n- 10% en planes"
    elif text == "3":
        message = "📞 Opcion 3 Un asesor se comunicará contigo pronto."
    else:
        message = "❓ No entendí tu mensaje. Escribe 'menu o mm' para ver opciones."
    
    payload = {
        "messaging_product": "whatsapp",
        "to": phonenumber,
        "type": "text",
        "text": {"body": message}
    }

    # ⚠️ CRÍTICO: Enviar el mensaje a WhatsApp
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"✅ **** ***** Mensaje enviado -> {fromname} Phone -> ({phonenumber}) Status -> {response.status_code}")
            
        if response.status_code == 200:
            message_id = response.json().get("messages", [{}])[0].get("id")
            save_bot_response(phonenumber, fromname, message, timestamp, message_id)
        else:
            print(f"⚠️ Error al enviar mensaje: {response.json()}")           
    except Exception as e:
        print(f"❌ Excepción al enviar mensaje: {e}")

# ============ RUTAS / ENDPOINTS ============

# -------------- Webhook para WhatsApp
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
                    
                # ✅ Extraer el nombre del contacto correctamente
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

# ============ NUEVOS ENDPOINTS PARA LA APP MÓVIL ============

# 📊 Obtener conversaciones recientes
@app.route("/api/conversations", methods=["GET"])
def get_conversations():
    """Obtiene las últimas conversaciones de WhatsApp"""
    token = get_token()
    if not token:
        return jsonify({"error": "Error de autenticación"}), 500
    
    limit = request.args.get('limit', 50)
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s"
    url += f"?$top={limit}&$orderby=cr321_timestamp desc"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            
            # Agrupar por número de teléfono
            conversations = {}
            for record in data.get("value", []):
                phone = record.get("cr321_phone")
                if phone not in conversations:
                    conversations[phone] = {
                        "phone": phone,
                        "name": record.get("cr321_fromname", "Desconocido"),
                        "last_message": record.get("cr321_body", ""),
                        "timestamp": record.get("cr321_timestamp"),
                        "unread": 0
                    }
            
            return jsonify({
                "success": True,
                "conversations": list(conversations.values())
            })
        else:
            return jsonify({"error": "Error al consultar Dataverse"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 💬 Obtener mensajes de una conversación
@app.route("/api/messages/<phone_number>", methods=["GET"])
def get_messages(phone_number):
    """Obtiene todos los mensajes de un número específico"""
    token = get_token()
    if not token:
        return jsonify({"error": "Error de autenticación"}), 500
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s"
    url += f"?$filter=cr321_phone eq '{phone_number}'"
    url += "&$orderby=cr321_timestamp asc"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            
            messages = []
            for record in data.get("value", []):
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
        return jsonify({"error": str(e)}), 500

# 📤 Enviar mensaje manual
@app.route("/api/send_message", methods=["POST"])
def send_manual_message():
    """Envía un mensaje desde la app móvil"""
    data = request.get_json()
    phone = data.get("phone")
    message = data.get("message")
    
    if not phone or not message:
        return jsonify({"error": "Faltan parámetros"}), 400
    
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": message}
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            message_id = response.json().get("messages", [{}])[0].get("id")
            timestamp = int(datetime.now(timezone.utc).timestamp())
            save_bot_response(phone, "", message, timestamp, message_id)
            
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
        return jsonify({"error": str(e)}), 500

# ============ EJECUTAR APLICACIÓN ============
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)