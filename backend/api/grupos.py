"""
API para gestión de Grupos en Dataverse
Tabla: cr321_grup

Campos:
- cr321_grupoid (PK, GUID)
- cr321_idgrupo (consecutivo, int)
- cr321_nombre (string)
- cr321_tipo (string: "A", "B", "C")
- cr321_descripcion (string)
"""
from flask import Blueprint, request, jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from goot import get_token, DATAVERSE_URL
import requests

bp_grupos = Blueprint('grupos', __name__)

# Mapeo de tipos de grupo
TIPO_GRUPO_MAP = {
    "A": 462410000,  # Opciones de menú principal
    "B": 462410001,  # Grupos secundarios
    "C": 462410002   # Grupos especiales
}

TIPO_GRUPO_REVERSE = {v: k for k, v in TIPO_GRUPO_MAP.items()}


def get_next_grupo_id():
    """Obtiene el siguiente ID consecutivo para grupo"""
    token = get_token()
    if not token:
        return 1
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_grups?$select=cr321_idgrupo&$orderby=cr321_idgrupo desc&$top=1"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            grupos = data.get("value", [])
            if grupos:
                return grupos[0].get("cr321_idgrupo", 0) + 1
        return 1
    except Exception as e:
        print(f"Error obteniendo próximo ID de grupo: {e}")
        return 1


@bp_grupos.route('/api/grupos', methods=['GET'])
def get_grupos():
    """Obtener lista de grupos. Filtro opcional por tipo"""
    tipo = request.args.get('tipo')
    
    token = get_token()
    if not token:
        return jsonify({"error": "No se pudo autenticar con Dataverse"}), 503
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_grups?$select=cr321_grupoid,cr321_idgrupo,cr321_nombre,cr321_tipo,cr321_descripcion"
    
    if tipo:
        tipo_val = TIPO_GRUPO_MAP.get(tipo.upper())
        if tipo_val is not None:
            url += f"&$filter=cr321_tipo eq {tipo_val}"
    
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            grupos = []
            for grupo in data.get("value", []):
                tipo_num = grupo.get("cr321_tipo")
                grupos.append({
                    "id": grupo.get("cr321_grupoid"),
                    "idgrupo": grupo.get("cr321_idgrupo"),
                    "nombre": grupo.get("cr321_nombre"),
                    "tipo": TIPO_GRUPO_REVERSE.get(tipo_num, "A"),
                    "descripcion": grupo.get("cr321_descripcion", "")
                })
            return jsonify({"grupos": grupos}), 200
        else:
            return jsonify({"error": f"Error Dataverse: {response.status_code}"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_grupos.route('/api/grupos', methods=['POST'])
def create_grupo():
    """Crear nuevo grupo"""
    data = request.get_json()
    nombre = data.get("nombre")
    tipo = data.get("tipo", "A").upper()
    descripcion = data.get("descripcion", "")
    
    if not nombre:
        return jsonify({"error": "El nombre del grupo es obligatorio"}), 400
    
    if tipo not in TIPO_GRUPO_MAP:
        return jsonify({"error": "Tipo inválido. Use A, B o C"}), 400
    
    token = get_token()
    if not token:
        return jsonify({"error": "No se pudo autenticar con Dataverse"}), 503
    
    # Obtener siguiente ID consecutivo
    next_id = get_next_grupo_id()
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_grups"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {
        "cr321_idgrupo": next_id,
        "cr321_nombre": nombre,
        "cr321_tipo": TIPO_GRUPO_MAP[tipo],
        "cr321_descripcion": descripcion
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 204:
            # Dataverse devuelve 204 en creación exitosa
            return jsonify({
                "message": "Grupo creado exitosamente",
                "idgrupo": next_id
            }), 201
        else:
            return jsonify({"error": f"Error Dataverse: {response.status_code}", "details": response.text}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_grupos.route('/api/grupos/<int:idgrupo>', methods=['PUT'])
def update_grupo(idgrupo):
    """Actualizar un grupo existente"""
    data = request.get_json()
    
    token = get_token()
    if not token:
        return jsonify({"error": "No se pudo autenticar con Dataverse"}), 503
    
    # Buscar el grupo por idgrupo
    search_url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_grups?$filter=cr321_idgrupo eq {idgrupo}&$select=cr321_grupoid"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    
    try:
        search_response = requests.get(search_url, headers=headers)
        if search_response.status_code != 200:
            return jsonify({"error": "Grupo no encontrado"}), 404
        
        grupos = search_response.json().get("value", [])
        if not grupos:
            return jsonify({"error": "Grupo no encontrado"}), 404
        
        grupo_guid = grupos[0]["cr321_grupoid"]
        
        # Actualizar el grupo
        update_url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_grups({grupo_guid})"
        headers["Content-Type"] = "application/json"
        
        payload = {}
        if "nombre" in data:
            payload["cr321_nombre"] = data["nombre"]
        if "tipo" in data:
            tipo = data["tipo"].upper()
            if tipo in TIPO_GRUPO_MAP:
                payload["cr321_tipo"] = TIPO_GRUPO_MAP[tipo]
        if "descripcion" in data:
            payload["cr321_descripcion"] = data["descripcion"]
        
        response = requests.patch(update_url, json=payload, headers=headers)
        if response.status_code == 204:
            return jsonify({"message": "Grupo actualizado exitosamente"}), 200
        else:
            return jsonify({"error": f"Error Dataverse: {response.status_code}", "details": response.text}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_grupos.route('/api/grupos/<int:idgrupo>', methods=['DELETE'])
def delete_grupo(idgrupo):
    """Eliminar un grupo"""
    token = get_token()
    if not token:
        return jsonify({"error": "No se pudo autenticar con Dataverse"}), 503
    
    # Buscar el grupo por idgrupo
    search_url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_grups?$filter=cr321_idgrupo eq {idgrupo}&$select=cr321_grupoid"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    
    try:
        search_response = requests.get(search_url, headers=headers)
        if search_response.status_code != 200:
            return jsonify({"error": "Grupo no encontrado"}), 404
        
        grupos = search_response.json().get("value", [])
        if not grupos:
            return jsonify({"error": "Grupo no encontrado"}), 404
        
        grupo_guid = grupos[0]["cr321_grupoid"]
        
        # Eliminar el grupo
        delete_url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_grups({grupo_guid})"
        response = requests.delete(delete_url, headers=headers)
        
        if response.status_code == 204:
            return jsonify({"message": "Grupo eliminado exitosamente"}), 200
        else:
            return jsonify({"error": f"Error Dataverse: {response.status_code}", "details": response.text}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500
