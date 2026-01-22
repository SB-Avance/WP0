"""
Gestión de mensajes: listar, eliminar, enviar (solo admin puede eliminar)
"""
from flask import Blueprint, request, jsonify
from goot import get_messages_by_phone, delete_message_by_id
from api.auth import token_required

bp_messages = Blueprint('messages', __name__)

@bp_messages.route('/api/messages/<phone>', methods=['GET'])
@token_required
def list_messages(current_user, phone):
    # Un usuario solo puede ver sus propios mensajes, admin puede ver todos
    if str(current_user.get('cr321_rol', '')).lower() != 'administrador' and current_user.get('cr321_correo') != phone:
        return jsonify({'message': 'No autorizado'}), 403
    messages = get_messages_by_phone(phone)
    return jsonify({'messages': messages})

@bp_messages.route('/api/messages/<msg_id>', methods=['DELETE'])
@token_required
def delete_message(current_user, msg_id):
    if str(current_user.get('cr321_rol', '')).lower() != 'administrador':
        return jsonify({'message': 'No autorizado'}), 403
    ok = delete_message_by_id(msg_id)
    if ok:
        return jsonify({'message': 'Mensaje eliminado'})
    else:
        return jsonify({'message': 'Error al eliminar mensaje'}), 400
