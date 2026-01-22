"""
Configuración de usuario (cambiar contraseña, nombre, etc.)
"""
from flask import Blueprint, request, jsonify
from goot import update_user_settings
from api.auth import token_required

bp_settings = Blueprint('settings', __name__)

@bp_settings.route('/api/settings', methods=['PATCH'])
@token_required
def update_settings(current_user):
    data = request.get_json()
    # Aquí deberías validar y actualizar los datos del usuario
    ok = update_user_settings(current_user, data)
    if ok:
        return jsonify({'message': 'Configuración actualizada'})
    else:
        return jsonify({'message': 'Error al actualizar configuración'}), 400
