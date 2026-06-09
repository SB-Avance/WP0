"""
API para gestión de Chatbots en Dataverse
Tabla: cr321_chatbot
"""

import os
import sys

from flask import Blueprint, jsonify, request

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import requests
from goot import DATAVERSE_URL, get_token

bp_chatbots = Blueprint("chatbots", __name__)


@bp_chatbots.route("/api/chatbots", methods=["GET"])
def get_chatbots():
    """Obtener todos los chatbots"""
    token = get_token()
    if not token:
        return jsonify({"error": "No se pudo obtener token"}), 500

    try:
        url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_chatbots"
        url += "?$select=cr321_chatbotid,cr321_name,cr321_type,cr321_active,cr321_config,cr321_elemento1,cr321_elemento2,cr321_elemento3,cr321_elemento4,cr321_elemento5"
        url += "&$orderby=cr321_name asc"

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "OData-MaxVersion": "4.0",
            "OData-Version": "4.0",
        }

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            chatbots = []
            for item in data.get("value", []):
                chatbots.append(
                    {
                        "id": item.get("cr321_chatbotid"),
                        "nombre": item.get("cr321_name", "Sin nombre"),
                        "tipo": get_tipo_nombre(item.get("cr321_type")),
                        "tipo_valor": item.get("cr321_type"),
                        "activo": item.get("cr321_active", False),
                        "config": item.get("cr321_config", "{}"),
                        "elemento1": item.get("cr321_elemento1", ""),
                        "elemento2": item.get("cr321_elemento2", ""),
                        "elemento3": item.get("cr321_elemento3", ""),
                        "elemento4": item.get("cr321_elemento4", ""),
                        "elemento5": item.get("cr321_elemento5", ""),
                    }
                )

            return jsonify({"success": True, "chatbots": chatbots}), 200
        else:
            return (
                jsonify(
                    {"error": f"Error al obtener chatbots: {response.status_code}"}
                ),
                response.status_code,
            )

    except Exception as e:
        print(f"Error al obtener chatbots: {e}")
        return jsonify({"error": str(e)}), 500


@bp_chatbots.route("/api/chatbots", methods=["POST"])
def create_chatbot():
    """Crear nuevo chatbot"""
    token = get_token()
    if not token:
        return jsonify({"error": "No se pudo obtener token"}), 500

    data = request.get_json()
    nombre = data.get("nombre")
    tipo = data.get("tipo", 462410000)  # FlowBot por defecto
    config = data.get("config", "{}")
    activo = data.get("activo", True)

    if not nombre:
        return jsonify({"error": "El nombre es requerido"}), 400

    try:
        url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_chatbots"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "OData-MaxVersion": "4.0",
            "OData-Version": "4.0",
        }

        chatbot_data = {
            "cr321_name": nombre,
            "cr321_type": tipo,
            "cr321_config": config,
            "cr321_active": activo,
        }

        response = requests.post(url, json=chatbot_data, headers=headers, timeout=10)

        if response.status_code in [200, 201, 204]:
            return (
                jsonify({"success": True, "message": "Chatbot creado exitosamente"}),
                201,
            )
        else:
            return (
                jsonify({"error": f"Error al crear chatbot: {response.status_code}"}),
                response.status_code,
            )

    except Exception as e:
        print(f"Error al crear chatbot: {e}")
        return jsonify({"error": str(e)}), 500


@bp_chatbots.route("/api/chatbots/<chatbot_id>", methods=["PUT", "PATCH"])
def update_chatbot(chatbot_id):
    """Actualizar chatbot existente"""
    token = get_token()
    if not token:
        return jsonify({"error": "No se pudo obtener token"}), 500

    data = request.get_json()

    try:
        url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_chatbots({chatbot_id})"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "OData-MaxVersion": "4.0",
            "OData-Version": "4.0",
        }

        update_data = {}
        if "nombre" in data:
            update_data["cr321_name"] = data["nombre"]
        if "tipo" in data:
            update_data["cr321_type"] = data["tipo"]
        if "config" in data:
            update_data["cr321_config"] = data["config"]
        if "activo" in data:
            update_data["cr321_active"] = data["activo"]

        response = requests.patch(url, json=update_data, headers=headers, timeout=10)

        if response.status_code in [200, 204]:
            return (
                jsonify(
                    {"success": True, "message": "Chatbot actualizado exitosamente"}
                ),
                200,
            )
        else:
            return (
                jsonify(
                    {"error": f"Error al actualizar chatbot: {response.status_code}"}
                ),
                response.status_code,
            )

    except Exception as e:
        print(f"Error al actualizar chatbot: {e}")
        return jsonify({"error": str(e)}), 500


@bp_chatbots.route("/api/chatbots/<chatbot_id>", methods=["DELETE"])
def delete_chatbot(chatbot_id):
    """Eliminar chatbot"""
    token = get_token()
    if not token:
        return jsonify({"error": "No se pudo obtener token"}), 500

    try:
        url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_chatbots({chatbot_id})"

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "OData-MaxVersion": "4.0",
            "OData-Version": "4.0",
        }

        response = requests.delete(url, headers=headers, timeout=10)

        if response.status_code in [200, 204]:
            return (
                jsonify({"success": True, "message": "Chatbot eliminado exitosamente"}),
                200,
            )
        else:
            return (
                jsonify(
                    {"error": f"Error al eliminar chatbot: {response.status_code}"}
                ),
                response.status_code,
            )

    except Exception as e:
        print(f"Error al eliminar chatbot: {e}")
        return jsonify({"error": str(e)}), 500


def get_tipo_nombre(tipo_valor):
    """Convertir valor numérico a nombre de tipo"""
    tipos = {462410000: "FlowBot", 462410001: "Simple", 462410002: "AI Assistant"}
    return tipos.get(tipo_valor, "Desconocido")
