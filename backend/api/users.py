"""
CRUD de usuarios (solo admin puede crear, editar, eliminar)
"""
from flask import Blueprint, request, jsonify
from goot import get_user_by_email, create_user, print_all_users
from api.auth import token_required

bp_users = Blueprint('users', __name__)

@bp_users.route('/api/users', methods=['GET'])
@token_required
def list_users(current_user):
    # Solo admin puede ver todos los usuarios
    if str(current_user.get('cr321_rol', '')).lower() != 'administrador':
        return jsonify({'message': 'No autorizado'}), 403
    # Aquí deberías usar una función que devuelva todos los usuarios
    # Por ahora, solo imprime en consola
    print_all_users()
    return jsonify({'message': 'Función listar usuarios implementa aquí'}), 200

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
