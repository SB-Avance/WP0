"""
API para gestión de Templates de WhatsApp en Dataverse
Tabla: cr321_template
"""

import os
import sys

from flask import Blueprint, jsonify, request

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import requests
from goot import DATAVERSE_URL, get_token

bp_templates = Blueprint("templates", __name__)


def get_categoria_nombre(categoria_valor):
    """Convertir valor de categoría a nombre legible"""
    categorias = {
        462410000: "Marketing",
        462410001: "Utilidad",
        462410002: "Autenticación",
    }
    return categorias.get(categoria_valor, "Desconocido")


@bp_templates.route("/api/templates", methods=["GET"])
def get_templates():
    """Obtener todos los templates"""
    token = get_token()
    if not token:
        return jsonify({"error": "No se pudo obtener token"}), 500

    try:
        url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_templates"
        url += "?$select=cr321_templateid,cr321_name,cr321_categoria,cr321_contenido,cr321_activo"
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
            templates = []
            for item in data.get("value", []):
                templates.append(
                    {
                        "id": item.get("cr321_templateid"),
                        "nombre": item.get("cr321_name", "Sin nombre"),
                        "categoria": get_categoria_nombre(item.get("cr321_categoria")),
                        "categoria_valor": item.get("cr321_categoria"),
                        "contenido": item.get("cr321_contenido", ""),
                        "activo": item.get("cr321_activo", False),
                    }
                )

            return jsonify({"templates": templates}), 200
        else:
            return (
                jsonify(
                    {"error": f"Error al obtener templates: {response.status_code}"}
                ),
                response.status_code,
            )

    except Exception as e:
        print(f"Error en get_templates: {e}")
        return jsonify({"error": str(e)}), 500


@bp_templates.route("/api/templates", methods=["POST"])
def create_template():
    """Crear nuevo template"""
    token = get_token()
    if not token:
        return jsonify({"error": "No se pudo obtener token"}), 500

    data = request.get_json()

    # Validar campos requeridos
    if not data.get("nombre") or not data.get("contenido"):
        return jsonify({"error": "Nombre y contenido son requeridos"}), 400

    try:
        url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_templates"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "OData-MaxVersion": "4.0",
            "OData-Version": "4.0",
        }

        payload = {
            "cr321_name": data.get("nombre"),
            "cr321_categoria": data.get("categoria", 462410001),  # Default: Utilidad
            "cr321_contenido": data.get("contenido"),
            "cr321_activo": data.get("activo", True),
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)

        if response.status_code == 204:
            # Obtener el ID del nuevo registro del header Location
            location = response.headers.get("OData-EntityId", "")
            template_id = (
                location.split("(")[-1].split(")")[0] if "(" in location else None
            )
            return (
                jsonify(
                    {
                        "success": True,
                        "id": template_id,
                        "message": "Template creado exitosamente",
                    }
                ),
                201,
            )
        else:
            return (
                jsonify(
                    {
                        "error": f"Error al crear template: {response.status_code}",
                        "details": response.text,
                    }
                ),
                response.status_code,
            )

    except Exception as e:
        print(f"Error en create_template: {e}")
        return jsonify({"error": str(e)}), 500


@bp_templates.route("/api/templates/<template_id>", methods=["PATCH", "PUT"])
def update_template(template_id):
    """Actualizar template existente"""
    token = get_token()
    if not token:
        return jsonify({"error": "No se pudo obtener token"}), 500

    data = request.get_json()

    try:
        url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_templates({template_id})"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "OData-MaxVersion": "4.0",
            "OData-Version": "4.0",
        }

        payload = {}
        if "nombre" in data:
            payload["cr321_name"] = data["nombre"]
        if "categoria" in data:
            payload["cr321_categoria"] = data["categoria"]
        if "contenido" in data:
            payload["cr321_contenido"] = data["contenido"]
        if "activo" in data:
            payload["cr321_activo"] = data["activo"]

        response = requests.patch(url, json=payload, headers=headers, timeout=10)

        if response.status_code in [200, 204]:
            return (
                jsonify(
                    {"success": True, "message": "Template actualizado exitosamente"}
                ),
                200,
            )
        else:
            return (
                jsonify(
                    {
                        "error": f"Error al actualizar template: {response.status_code}",
                        "details": response.text,
                    }
                ),
                response.status_code,
            )

    except Exception as e:
        print(f"Error en update_template: {e}")
        return jsonify({"error": str(e)}), 500


@bp_templates.route("/api/templates/<template_id>", methods=["DELETE"])
def delete_template(template_id):
    """Eliminar template"""
    token = get_token()
    if not token:
        return jsonify({"error": "No se pudo obtener token"}), 500

    try:
        url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_templates({template_id})"

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "OData-MaxVersion": "4.0",
            "OData-Version": "4.0",
        }

        response = requests.delete(url, headers=headers, timeout=10)

        if response.status_code in [200, 204]:
            return (
                jsonify(
                    {"success": True, "message": "Template eliminado exitosamente"}
                ),
                200,
            )
        else:
            return (
                jsonify(
                    {
                        "error": f"Error al eliminar template: {response.status_code}",
                        "details": response.text,
                    }
                ),
                response.status_code,
            )

    except Exception as e:
        print(f"Error en delete_template: {e}")
        return jsonify({"error": str(e)}), 500
