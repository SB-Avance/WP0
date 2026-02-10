"""
Módulo de autenticación JWT y login
"""
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
import jwt
import datetime
from functools import wraps
from goot import get_user_by_email, create_user
from config import SECRET_KEY

bp_auth = Blueprint('auth', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[-1]
        if not token:
            return jsonify({'message': 'Token requerido'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = get_user_by_email(data['correo'])
        except Exception as e:
            return jsonify({'message': 'Token inválido', 'error': str(e)}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@bp_auth.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    correo = data.get('correo')
    clave = data.get('clave')
    print(f"[LOGIN] Correo recibido: {correo}")
    print(f"[LOGIN] Clave recibida: '{clave}' (type: {type(clave)})")
    user = get_user_by_email(correo)
    print(f"[LOGIN] Usuario encontrado: {user}")
    if user:
        clave_db = user.get('cr321_clave')
        print(f"[LOGIN] Clave almacenada: '{clave_db}' (type: {type(clave_db)})")
        print(f"[LOGIN] Comparando: recibida='{clave}' vs almacenada='{clave_db}' -> {clave == clave_db}")
        if clave_db == clave:
            token = jwt.encode({
                'correo': correo,
                'rol': user.get('cr321_rol'),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12)
            }, SECRET_KEY, algorithm="HS256")
            return jsonify({
                'token': token, 
                'user': {
                    'id': user.get('cr321_usuariosid'),  # ID del usuario
                    'nombre': user.get('cr321_nombre'), 
                    'correo': correo, 
                    'rol': user.get('cr321_rol')
                }
            })
        else:
            print("[LOGIN] Clave incorrecta")
            return jsonify({'message': 'Credenciales incorrectas'}), 401
    else:
        print("[LOGIN] Usuario no encontrado")
        return jsonify({'message': 'Credenciales incorrectas'}), 401

@bp_auth.route('/register', methods=['POST'])
def register():
    """Registro público de usuarios (sin autenticación)"""
    data = request.get_json()
    nombre = data.get('nombre')
    correo = data.get('correo')
    clave = data.get('clave')
    rol = data.get('rol', 'Usuario')  # Por defecto, rol 'Usuario'
    
    print(f"[REGISTER] Intentando registrar: {nombre}, {correo}, rol: {rol}")
    
    # Verificar si el usuario ya existe
    existing_user = get_user_by_email(correo)
    if existing_user:
        print(f"[REGISTER] Usuario ya existe: {correo}")
        return jsonify({'success': False, 'message': 'El correo ya está registrado'}), 400
    
    # Crear usuario
    user_id = create_user(nombre, correo, rol, clave)
    
    if user_id:
        print(f"[REGISTER] Usuario creado exitosamente: {user_id}")
        return jsonify({'success': True, 'message': 'Usuario registrado exitosamente', 'id': user_id}), 201
    else:
        print(f"[REGISTER] Error al crear usuario")
        return jsonify({'success': False, 'message': 'Error al registrar usuario'}), 500
