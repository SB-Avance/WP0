"""
Webhook para recibir notificaciones de WhatsApp y almacenar mensajes en Dataverse
"""
from flask import Blueprint, request, jsonify
from goot import save_incoming_message

bp_webhook = Blueprint('webhook', __name__)

@bp_webhook.route('/webhook', methods=['POST'])
def whatsapp_webhook():
    data = request.get_json()
    # Aquí deberías procesar el payload de WhatsApp y guardar en Dataverse
    # Ejemplo simplificado:
    try:
        save_incoming_message(data)
        return jsonify({'message': 'Mensaje recibido'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
