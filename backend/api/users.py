"""
CRUD de usuarios (solo admin puede crear, editar, eliminar)
"""
from flask import Blueprint, request, jsonify
from goot import get_user_by_email, create_user, print_all_users, get_all_users
from api.auth import token_required

bp_users = Blueprint('users', __name__)

@bp_users.route('/api/users', methods=['GET'])
@token_required
def list_users(current_user):
    # Solo admin puede ver todos los usuarios
    if str(current_user.get('cr321_rol', '')).lower() != 'administrador':
        return jsonify({'message': 'No autorizado'}), 403
    users = get_all_users()
    # Mapear campos relevantes
    users_list = [{
        'id': u.get('cr321_usuariosid'),
        'nombre': u.get('cr321_nombre'),
        'correo': u.get('cr321_correo'),
        'rol': u.get('cr321_rol')
    } for u in users]
    return jsonify({'users': users_list}), 200

@bp_users.route('/api/users', methods=['POST'])
@token_required
def create_new_user(current_user):
    if str(current_user.get('cr321_rol', '')).lower() != 'administrador':
        return jsonify({'message': 'No autorizado'}), 403
    data = request.get_json()
    nombre = data.get('nombre')
    correo = data.get('correo')
    clave = data.get('clave')
    rol = data.get('rol')
    user_id = create_user(nombre, correo, rol, clave)
    if user_id:
        return jsonify({'message': 'Usuario creado', 'id': user_id}), 201
    else:
        return jsonify({'message': 'Error al crear usuario'}), 400
