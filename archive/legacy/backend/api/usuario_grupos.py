"""
API para gestión de relaciones Usuario-Grupo en Dataverse
Tabla: cr321_usuariogrupos

Campos:
- cr321_usuariogruposid (PK, GUID)
- cr321_usuarioid (GUID - FK a cr321_usuarios)
- cr321_grupoid (GUID - FK a cr321_grup)
"""

import os
import sys

from flask import Blueprint, jsonify, request

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import requests
from goot import DATAVERSE_URL, get_token

bp_usuario_grupos = Blueprint("usuario_grupos", __name__)


@bp_usuario_grupos.route("/api/usuario-grupos", methods=["GET"])
def get_usuario_grupos():
    """Obtener relaciones usuario-grupo. Filtros opcionales: usuario, grupo"""
    usuario_id = request.args.get("usuario_id")
    grupo_id = request.args.get("grupo_id")

    token = get_token()
    if not token:
        return jsonify({"error": "No se pudo autenticar con Dataverse"}), 503

    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuariogrupos?$select=cr321_usuariogruposid"
    url += "&$expand=cr321_usuarioid($select=cr321_usuariosid,cr321_nombre,cr321_correo),cr321_grupoid($select=cr321_grupoid,cr321_nombre,cr321_tipo)"

    filters = []
    if usuario_id:
        filters.append(f"_cr321_usuarioid_value eq {usuario_id}")
    if grupo_id:
        filters.append(f"_cr321_grupoid_value eq {grupo_id}")

    if filters:
        url += "&$filter=" + " and ".join(filters)

    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            relaciones = []
            for rel in data.get("value", []):
                relaciones.append(
                    {
                        "id": rel.get("cr321_usuariogruposid"),
                        "usuario": rel.get("cr321_usuarioid", {}),
                        "grupo": rel.get("cr321_grupoid", {}),
                    }
                )
            return jsonify({"relaciones": relaciones}), 200
        else:
            return (
                jsonify({"error": f"Error Dataverse: {response.status_code}"}),
                response.status_code,
            )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_usuario_grupos.route("/api/usuario-grupos/usuario/<usuario_id>", methods=["GET"])
def get_grupos_by_usuario(usuario_id):
    """Obtener todos los grupos de un usuario usando lookup _cr321_grupo_value"""
    token = get_token()
    if not token:
        return jsonify({"error": "No se pudo autenticar con Dataverse"}), 503

    # Usar lookup _cr321_grupo_value con $expand para obtener nombres directamente
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuariogrupos?$filter=_cr321_usuarioid_value eq {usuario_id}"
    url += "&$select=cr321_usuariogrupoid,_cr321_grupo_value"
    url += "&$expand=cr321_grupo($select=cr321_grupid,cr321_grupoid,cr321_nombre)"

    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()

            grupos = []
            for rel in data.get("value", []):
                # Obtener datos del lookup navegado
                grupo_obj = rel.get("cr321_grupo")

                if grupo_obj:
                    grupos.append(
                        {
                            "id": grupo_obj.get("cr321_grupid"),  # GUID del grupo
                            "grupoid": grupo_obj.get(
                                "cr321_grupoid"
                            ),  # Código (0000-0004)
                            "nombre": grupo_obj.get(
                                "cr321_nombre"
                            ),  # Nombre desde lookup
                            "tipo": None,
                            "descripcion": "",
                        }
                    )

            return jsonify({"grupos": grupos}), 200
        else:
            return (
                jsonify({"error": f"Error Dataverse: {response.status_code}"}),
                response.status_code,
            )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_usuario_grupos.route("/api/usuario-grupos/grupo/<grupo_id>", methods=["GET"])
def get_usuarios_by_grupo(grupo_id):
    """Obtener todos los usuarios de un grupo"""
    token = get_token()
    if not token:
        return jsonify({"error": "No se pudo autenticar con Dataverse"}), 503

    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuariogrupos?$filter=_cr321_grupoid_value eq {grupo_id}"
    url += "&$expand=cr321_usuarioid($select=cr321_usuariosid,cr321_idusuario,cr321_nombre,cr321_correo,cr321_rol)"

    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            usuarios = []
            for rel in data.get("value", []):
                usuario_data = rel.get("cr321_usuarioid", {})
                if usuario_data:
                    usuarios.append(
                        {
                            "id": usuario_data.get("cr321_usuariosid"),
                            "idusuario": usuario_data.get("cr321_idusuario"),
                            "nombre": usuario_data.get("cr321_nombre"),
                            "correo": usuario_data.get("cr321_correo"),
                            "rol": usuario_data.get("cr321_rol"),
                        }
                    )
            return jsonify({"usuarios": usuarios}), 200
        else:
            return (
                jsonify({"error": f"Error Dataverse: {response.status_code}"}),
                response.status_code,
            )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_usuario_grupos.route("/api/usuario-grupos", methods=["POST"])
def create_usuario_grupo():
    """Asignar un usuario a un grupo"""
    data = request.get_json()
    usuario_id = data.get("usuario_id")
    grupo_id = data.get("grupo_id")

    if not usuario_id or not grupo_id:
        return jsonify({"error": "usuario_id y grupo_id son obligatorios"}), 400

    token = get_token()
    if not token:
        return jsonify({"error": "No se pudo autenticar con Dataverse"}), 503

    # Verificar si la relación ya existe
    check_url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuariogrupos?$filter=_cr321_usuarioid_value eq {usuario_id} and _cr321_grupoid_value eq {grupo_id}"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    try:
        check_response = requests.get(check_url, headers=headers)
        if check_response.status_code == 200:
            existing = check_response.json().get("value", [])
            if existing:
                return jsonify({"error": "Esta relación ya existe"}), 400

        # Crear la relación
        url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuariogrupos"
        headers["Content-Type"] = "application/json"

        payload = {
            "cr321_usuarioid@odata.bind": f"/cr321_usuarioses({usuario_id})",
            "cr321_grupoid@odata.bind": f"/cr321_grups({grupo_id})",
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 204:
            return jsonify({"message": "Usuario asignado al grupo exitosamente"}), 201
        else:
            return (
                jsonify(
                    {
                        "error": f"Error Dataverse: {response.status_code}",
                        "details": response.text,
                    }
                ),
                response.status_code,
            )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_usuario_grupos.route("/api/usuario-grupos/<relacion_id>", methods=["DELETE"])
def delete_usuario_grupo(relacion_id):
    """Eliminar relación usuario-grupo"""
    token = get_token()
    if not token:
        return jsonify({"error": "No se pudo autenticar con Dataverse"}), 503

    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuariogrupos({relacion_id})"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.delete(url, headers=headers)
        if response.status_code == 204:
            return jsonify({"message": "Relación eliminada exitosamente"}), 200
        else:
            return (
                jsonify(
                    {
                        "error": f"Error Dataverse: {response.status_code}",
                        "details": response.text,
                    }
                ),
                response.status_code,
            )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
