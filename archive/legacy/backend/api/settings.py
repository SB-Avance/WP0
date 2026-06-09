"""
Configuración de usuario (cambiar contraseña, nombre, etc.)
"""

from api.auth import token_required
from flask import Blueprint, jsonify, request
from goot import update_user_settings

bp_settings = Blueprint("settings", __name__)


@bp_settings.route("/api/settings", methods=["PATCH"])
@token_required
def update_settings(current_user):
    data = request.get_json()
    # Aquí deberías validar y actualizar los datos del usuario
    ok = update_user_settings(current_user, data)
    if ok:
        return jsonify({"message": "Configuración actualizada"})
    else:
        return jsonify({"message": "Error al actualizar configuración"}), 400
