"""
API para gestión de cotizaciones
Tabla: cr321_cotizacion
"""

import os
import sys

from flask import Blueprint, jsonify, request

# Configurar path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.insert(0, backend_dir)

import requests
from back import DATAVERSE_URL, get_token

cotizaciones_bp = Blueprint("cotizaciones", __name__)

ENTITY_SET = (
    "cr321_cotizacions"  # Dataverse pluraliza cr321_cotizacion -> cr321_cotizacions
)


@cotizaciones_bp.route("/api/cotizaciones", methods=["GET"])
def get_cotizaciones():
    """Obtener todas las cotizaciones"""
    try:
        token = get_token()
        if not token:
            return jsonify({"error": "No se pudo obtener token"}), 401

        # Query parameters
        top = request.args.get("$top", 50)
        skip = request.args.get("$skip", 0)
        filter_param = request.args.get("$filter", "")
        orderby = request.args.get("$orderby", "createdon desc")

        url = f"{DATAVERSE_URL}/api/data/v9.2/{ENTITY_SET}?$top={top}&$skip={skip}&$orderby={orderby}"
        if filter_param:
            url += f"&$filter={filter_param}"

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "OData-MaxVersion": "4.0",
            "OData-Version": "4.0",
        }

        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({"error": response.text}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@cotizaciones_bp.route("/api/cotizaciones/<cotizacion_id>", methods=["GET"])
def get_cotizacion(cotizacion_id):
    """Obtener una cotización específica"""
    try:
        token = get_token()
        if not token:
            return jsonify({"error": "No se pudo obtener token"}), 401

        url = f"{DATAVERSE_URL}/api/data/v9.2/{ENTITY_SET}({cotizacion_id})"
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "OData-MaxVersion": "4.0",
            "OData-Version": "4.0",
        }

        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({"error": response.text}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@cotizaciones_bp.route("/api/cotizaciones", methods=["POST"])
def create_cotizacion():
    """Crear una nueva cotización"""
    try:
        token = get_token()
        if not token:
            return jsonify({"error": "No se pudo obtener token"}), 401

        data = request.get_json()

        # Construir objeto de cotización
        cotizacion_data = {}

        # Campos de texto
        if "cr321_nombre" in data:
            cotizacion_data["cr321_nombre"] = data["cr321_nombre"]
        if "cr321_cliente" in data:
            cotizacion_data["cr321_cliente"] = data["cr321_cliente"]
        if "cr321_descripcion" in data:
            cotizacion_data["cr321_descripcion"] = data["cr321_descripcion"]

        # Campo fecha
        if "cr321_fecha" in data:
            cotizacion_data["cr321_fecha"] = data["cr321_fecha"]

        # Campo entero auto-numerado (solo si se proporciona)
        if "cr321_cotizacion" in data:
            cotizacion_data["cr321_cotizacion"] = data["cr321_cotizacion"]

        # Campos de lookup (si existen)
        if "cr321_contactoId" in data:
            cotizacion_data["cr321_contactoId@odata.bind"] = (
                f"/cr321_contactos({data['cr321_contactoId']})"
            )

        url = f"{DATAVERSE_URL}/api/data/v9.2/{ENTITY_SET}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "OData-MaxVersion": "4.0",
            "OData-Version": "4.0",
            "Prefer": "return=representation",
        }

        response = requests.post(url, json=cotizacion_data, headers=headers, timeout=30)

        if response.status_code in [200, 201, 204]:
            if response.status_code == 204:
                # Obtener ID del header
                created_id = (
                    response.headers.get("OData-EntityId", "")
                    .split("(")[-1]
                    .rstrip(")")
                )
                return jsonify({"id": created_id, "message": "Cotización creada"}), 201
            else:
                return jsonify(response.json()), 201
        else:
            return jsonify({"error": response.text}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@cotizaciones_bp.route("/api/cotizaciones/<cotizacion_id>", methods=["PATCH", "PUT"])
def update_cotizacion(cotizacion_id):
    """Actualizar una cotización existente"""
    try:
        token = get_token()
        if not token:
            return jsonify({"error": "No se pudo obtener token"}), 401

        data = request.get_json()

        # Construir objeto de actualización sin el ID
        update_data = {}

        if "cr321_nombre" in data:
            update_data["cr321_nombre"] = data["cr321_nombre"]
        if "cr321_cliente" in data:
            update_data["cr321_cliente"] = data["cr321_cliente"]
        if "cr321_descripcion" in data:
            update_data["cr321_descripcion"] = data["cr321_descripcion"]
        if "cr321_fecha" in data:
            update_data["cr321_fecha"] = data["cr321_fecha"]
        if "cr321_cotizacion" in data:
            update_data["cr321_cotizacion"] = data["cr321_cotizacion"]

        url = f"{DATAVERSE_URL}/api/data/v9.2/{ENTITY_SET}({cotizacion_id})"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "OData-MaxVersion": "4.0",
            "OData-Version": "4.0",
        }

        response = requests.patch(url, json=update_data, headers=headers, timeout=30)

        if response.status_code in [200, 204]:
            return jsonify({"message": "Cotización actualizada"}), 200
        else:
            return jsonify({"error": response.text}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@cotizaciones_bp.route("/api/cotizaciones/<cotizacion_id>", methods=["DELETE"])
def delete_cotizacion(cotizacion_id):
    """Eliminar una cotización"""
    try:
        token = get_token()
        if not token:
            return jsonify({"error": "No se pudo obtener token"}), 401

        url = f"{DATAVERSE_URL}/api/data/v9.2/{ENTITY_SET}({cotizacion_id})"
        headers = {
            "Authorization": f"Bearer {token}",
            "OData-MaxVersion": "4.0",
            "OData-Version": "4.0",
        }

        response = requests.delete(url, headers=headers, timeout=30)

        if response.status_code == 204:
            return jsonify({"message": "Cotización eliminada"}), 200
        else:
            return jsonify({"error": response.text}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500
