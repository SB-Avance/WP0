"""
CRUD de usuarios (solo admin puede crear, editar, eliminar)
"""

import requests
from api.auth import token_required
from flask import Blueprint, jsonify, request
from goot import (DATAVERSE_URL, create_user, get_all_users, get_token,
                  get_user_by_email, print_all_users)

bp_users = Blueprint("users", __name__)


@bp_users.route("/api/users", methods=["GET"])
@token_required
def list_users(current_user):
    # Solo admin puede ver todos los usuarios
    if str(current_user.get("cr321_rol", "")).lower() != "administrador":
        return jsonify({"message": "No autorizado"}), 403
    users = get_all_users()
    # Mapear campos relevantes
    users_list = [
        {
            "id": u.get("cr321_usuariosid"),
            "nombre": u.get("cr321_nombre"),
            "correo": u.get("cr321_correo"),
            "rol": u.get("cr321_rol"),
        }
        for u in users
    ]
    return jsonify({"users": users_list}), 200


@bp_users.route("/api/users", methods=["POST"])
@token_required
def create_new_user(current_user):
    if str(current_user.get("cr321_rol", "")).lower() != "administrador":
        return jsonify({"message": "No autorizado"}), 403
    data = request.get_json()
    nombre = data.get("nombre")
    correo = data.get("correo")
    clave = data.get("clave")
    rol = data.get("rol", "usuario")

    if not all([nombre, correo, clave]):
        return jsonify({"message": "Faltan campos requeridos"}), 400

    user_id = create_user(nombre, correo, rol, clave)
    if user_id:
        return jsonify({"message": "Usuario creado", "id": user_id}), 201
    else:
        return jsonify({"message": "Error al crear usuario"}), 400


@bp_users.route("/api/users/<user_id>", methods=["PATCH", "PUT"])
@token_required
def update_user(current_user, user_id):
    """Actualizar usuario existente"""
    if str(current_user.get("cr321_rol", "")).lower() != "administrador":
        return jsonify({"message": "No autorizado"}), 403

    token = get_token()
    if not token:
        return jsonify({"error": "No se pudo obtener token"}), 500

    data = request.get_json()

    try:
        url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuarioses({user_id})"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "OData-MaxVersion": "4.0",
            "OData-Version": "4.0",
        }

        update_data = {}
        if "nombre" in data:
            update_data["cr321_nombre"] = data["nombre"]
        if "correo" in data:
            update_data["cr321_correo"] = data["correo"]
        if "rol" in data:
            update_data["cr321_rol"] = data["rol"]
        if "clave" in data:
            update_data["cr321_clave"] = data["clave"]

        response = requests.patch(url, json=update_data, headers=headers, timeout=10)

        if response.status_code in [200, 204]:
            return jsonify({"success": True, "message": "Usuario actualizado"}), 200
        else:
            return (
                jsonify({"error": f"Error al actualizar: {response.status_code}"}),
                response.status_code,
            )

    except Exception as e:
        print(f"Error al actualizar usuario: {e}")
        return jsonify({"error": str(e)}), 500


@bp_users.route("/api/users/<user_id>", methods=["DELETE"])
@token_required
def delete_user(current_user, user_id):
    """Eliminar usuario"""
    if str(current_user.get("cr321_rol", "")).lower() != "administrador":
        return jsonify({"message": "No autorizado"}), 403

    token = get_token()
    if not token:
        return jsonify({"error": "No se pudo obtener token"}), 500

    try:
        url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuarioses({user_id})"

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "OData-MaxVersion": "4.0",
            "OData-Version": "4.0",
        }

        response = requests.delete(url, headers=headers, timeout=10)

        if response.status_code in [200, 204]:
            return jsonify({"success": True, "message": "Usuario eliminado"}), 200
        else:
            return (
                jsonify({"error": f"Error al eliminar: {response.status_code}"}),
                response.status_code,
            )

    except Exception as e:
        print(f"Error al eliminar usuario: {e}")
        return jsonify({"error": str(e)}), 500
