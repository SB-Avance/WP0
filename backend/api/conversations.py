"""
Gestión de conversaciones: listar conversaciones recientes
"""
from flask import Blueprint, request, jsonify
from goot import get_conversations_for_user
from api.auth import token_required

bp_conversations = Blueprint('conversations', __name__)

@bp_conversations.route('/api/conversations', methods=['GET'])
@token_required
def list_conversations(current_user):
    # Un usuario solo puede ver sus propias conversaciones, admin puede ver todas
    conversations = get_conversations_for_user(current_user)
    return jsonify({'conversations': conversations})
