"""
API para gestión de Estados en Dataverse
Tabla: cr321_estado

Campos:
- cr321_estadoid (PK, GUID)
- cr321_idestado (consecutivo, int)
- cr321_nombre (string)
- cr321_descripcion (string)
"""

import os
import sys

from flask import Blueprint, jsonify, request

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import requests
from goot import DATAVERSE_URL, get_token

bp_estados = Blueprint("estados", __name__)


def get_next_estado_id():
    """Obtiene el siguiente ID consecutivo para estado"""
    token = get_token()
    if not token:
        return 1

    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_estados?$select=cr321_idestado&$orderby=cr321_idestado desc&$top=1"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            estados = data.get("value", [])
            if estados:
                return estados[0].get("cr321_idestado", 0) + 1
        return 1
    except Exception as e:
        print(f"Error obteniendo próximo ID de estado: {e}")
        return 1


@bp_estados.route("/api/estados", methods=["GET"])
def get_estados():
    """Obtener lista de estados"""
    token = get_token()
    if not token:
        return jsonify({"error": "No se pudo autenticar con Dataverse"}), 503

    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_estados?$select=cr321_estadoid,cr321_idestado,cr321_nombre,cr321_descripcion"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            estados = []
            for estado in data.get("value", []):
                estados.append(
                    {
                        "id": estado.get("cr321_estadoid"),
                        "idestado": estado.get("cr321_idestado"),
                        "nombre": estado.get("cr321_nombre"),
                        "descripcion": estado.get("cr321_descripcion", ""),
                    }
                )
            return jsonify({"estados": estados}), 200
        else:
            return (
                jsonify({"error": f"Error Dataverse: {response.status_code}"}),
                response.status_code,
            )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_estados.route("/api/estados", methods=["POST"])
def create_estado():
    """Crear nuevo estado"""
    data = request.get_json()
    nombre = data.get("nombre")
    descripcion = data.get("descripcion", "")

    if not nombre:
        return jsonify({"error": "El nombre del estado es obligatorio"}), 400

    token = get_token()
    if not token:
        return jsonify({"error": "No se pudo autenticar con Dataverse"}), 503

    # Obtener siguiente ID consecutivo
    next_id = get_next_estado_id()

    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_estados"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    payload = {
        "cr321_idestado": next_id,
        "cr321_nombre": nombre,
        "cr321_descripcion": descripcion,
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 204:
            return (
                jsonify({"message": "Estado creado exitosamente", "idestado": next_id}),
                201,
            )
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


@bp_estados.route("/api/estados/<int:idestado>", methods=["PUT"])
def update_estado(idestado):
    """Actualizar un estado existente"""
    data = request.get_json()

    token = get_token()
    if not token:
        return jsonify({"error": "No se pudo autenticar con Dataverse"}), 503

    # Buscar el estado por idestado
    search_url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_estados?$filter=cr321_idestado eq {idestado}&$select=cr321_estadoid"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    try:
        search_response = requests.get(search_url, headers=headers)
        if search_response.status_code != 200:
            return jsonify({"error": "Estado no encontrado"}), 404

        estados = search_response.json().get("value", [])
        if not estados:
            return jsonify({"error": "Estado no encontrado"}), 404

        estado_guid = estados[0]["cr321_estadoid"]

        # Actualizar el estado
        update_url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_estados({estado_guid})"
        headers["Content-Type"] = "application/json"

        payload = {}
        if "nombre" in data:
            payload["cr321_nombre"] = data["nombre"]
        if "descripcion" in data:
            payload["cr321_descripcion"] = data["descripcion"]

        response = requests.patch(update_url, json=payload, headers=headers)
        if response.status_code == 204:
            return jsonify({"message": "Estado actualizado exitosamente"}), 200
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


@bp_estados.route("/api/estados/<int:idestado>", methods=["DELETE"])
def delete_estado(idestado):
    """Eliminar un estado"""
    token = get_token()
    if not token:
        return jsonify({"error": "No se pudo autenticar con Dataverse"}), 503

    # Buscar el estado por idestado
    search_url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_estados?$filter=cr321_idestado eq {idestado}&$select=cr321_estadoid"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    try:
        search_response = requests.get(search_url, headers=headers)
        if search_response.status_code != 200:
            return jsonify({"error": "Estado no encontrado"}), 404

        estados = search_response.json().get("value", [])
        if not estados:
            return jsonify({"error": "Estado no encontrado"}), 404

        estado_guid = estados[0]["cr321_estadoid"]

        # Eliminar el estado
        delete_url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_estados({estado_guid})"
        response = requests.delete(delete_url, headers=headers)

        if response.status_code == 204:
            return jsonify({"message": "Estado eliminado exitosamente"}), 200
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
