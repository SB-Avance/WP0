"""
API Extendida para Chats - Aprovecha Lookups (cr321_grupoid, cr321_contactorelacion)
======================================================================================

Endpoints que usan $expand de OData para traer datos relacionados en una sola consulta.
Implementado: Febrero 2026

CAMPOS CORRECTOS EN DATAVERSE:
- cr321_adatawp0s: cr321_body, cr321_createdon, cr321_fromname, cr321_phone, cr321_direction
- cr321_contacto: cr321_fromname, cr321_phone (NO tiene email)

Beneficios:
- Menos requests HTTP (1 en vez de N+1)
- Datos relacionados automáticamente
- Mejor performance
"""

import os

import requests
from dotenv import load_dotenv
from flask import Blueprint, jsonify, request
from msal import ConfidentialClientApplication

# Cargar configuración
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(env_path)

DATAVERSE_URL = os.getenv("DATAVERSE_URL")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")

bp = Blueprint("chats_extended", __name__)


def get_access_token():
    """Obtener token de acceso para Dataverse"""
    authority = f"https://login.microsoftonline.com/{TENANT_ID}"
    app = ConfidentialClientApplication(
        CLIENT_ID, authority=authority, client_credential=CLIENT_SECRET
    )
    result = app.acquire_token_for_client(scopes=[f"{DATAVERSE_URL}/.default"])

    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception(
            f"Error obteniendo token: {result.get('error_description', 'Unknown')}"
        )


def get_headers():
    """Headers con autenticación"""
    token = get_access_token()
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0",
    }


@bp.route("/api/chats/con-contacto", methods=["GET"])
def get_chats_con_contacto():
    """
    Obtener chats con información de contacto expandida

    Query params:
    - top: número de resultados (default 50)
    - orderby: campo para ordenar (default: cr321_createdon desc)
    - filter: filtro adicional OData

    Returns:
        JSON con lista de chats incluyendo datos del contacto relacionado

    Ejemplo:
        GET /api/chats/con-contacto?top=20
    """
    try:
        # Parámetros de consulta
        top = request.args.get("top", 50, type=int)
        orderby = request.args.get("orderby", "cr321_createdon desc")
        custom_filter = request.args.get("filter", "")

        url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s"

        # Construir filtro base (solo chats con contacto)
        base_filter = "_cr321_contactorelacion_value ne null"
        if custom_filter:
            final_filter = f"({base_filter}) and ({custom_filter})"
        else:
            final_filter = base_filter

        params = {
            "$select": "cr321_adatawp0id,cr321_body,cr321_createdon,cr321_fromname,cr321_phone,cr321_direction",
            "$expand": "cr321_contactorelacion($select=cr321_contactoid,cr321_fromnombre,cr321_telefono)",
            "$filter": final_filter,
            "$orderby": orderby,
            "$top": top,
            "$count": "true",
        }

        response = requests.get(url, headers=get_headers(), params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()

            # Formatear respuesta
            chats = []
            for item in data.get("value", []):
                contacto = item.get("cr321_contactorelacion", {})

                chat = {
                    "id": item.get("cr321_adatawp0id"),
                    "mensaje": item.get("cr321_body"),
                    "fecha_hora": item.get("cr321_createdon"),
                    "from_nombre": item.get("cr321_fromname"),
                    "telefono": item.get("cr321_phone"),
                    "direccion": item.get("cr321_direction"),
                    "contacto": (
                        {
                            "id": contacto.get("cr321_contactoid"),
                            "nombre": contacto.get("cr321_fromname"),
                            "telefono": contacto.get("cr321_phone"),
                        }
                        if contacto
                        else None
                    ),
                }
                chats.append(chat)

            return (
                jsonify(
                    {
                        "success": True,
                        "total": data.get("@odata.count", len(chats)),
                        "data": chats,
                    }
                ),
                200,
            )

        else:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": f"Error {response.status_code}: {response.text[:200]}",
                    }
                ),
                response.status_code,
            )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@bp.route("/api/chats/por-grupo/<grupo_id>", methods=["GET"])
def get_chats_por_grupo(grupo_id):
    """
    Obtener todos los chats de un grupo específico con info expandida

    Args:
        grupo_id: GUID del grupo

    Query params:
        - top: número de resultados (default 100)
        - expand_contacto: incluir datos de contacto (default true)

    Returns:
        JSON con lista de chats del grupo

    Ejemplo:
        GET /api/chats/por-grupo/{guid}?top=50
    """
    try:
        top = request.args.get("top", 100, type=int)
        expand_contacto = request.args.get("expand_contacto", "true").lower() == "true"

        url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s"

        # Construir $expand
        expand_parts = ["cr321_grupoid($select=cr321_grupoid,cr321_nombre,cr321_tipo)"]
        if expand_contacto:
            expand_parts.append(
                "cr321_contactorelacion($select=cr321_contactoid,cr321_fromnombre,cr321_telefono)"
            )

        params = {
            "$select": "cr321_adatawp0id,cr321_body,cr321_createdon,cr321_fromname,cr321_phone",
            "$expand": ",".join(expand_parts),
            "$filter": f"cr321_grupoid/cr321_grupoid eq '{grupo_id}'",  # Filtro usando path de navegación
            "$orderby": "cr321_createdon desc",
            "$top": top,
            "$count": "true",
        }

        response = requests.get(url, headers=get_headers(), params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()

            # Formatear respuesta
            chats = []
            for item in data.get("value", []):
                grupo = item.get("cr321_grupoid", {})
                contacto = item.get("cr321_contactorelacion", {})

                chat = {
                    "id": item.get("cr321_adatawp0id"),
                    "mensaje": item.get("cr321_body"),
                    "fecha_hora": item.get("cr321_createdon"),
                    "from_nombre": item.get("cr321_fromname"),
                    "telefono": item.get("cr321_phone"),
                    "grupo": (
                        {
                            "id": grupo.get("cr321_grupoid"),
                            "nombre": grupo.get("cr321_nombre"),
                            "tipo": grupo.get("cr321_tipo"),
                        }
                        if grupo
                        else None
                    ),
                }

                if expand_contacto and contacto:
                    chat["contacto"] = {
                        "id": contacto.get("cr321_contactoid"),
                        "nombre": contacto.get("cr321_fromname"),
                        "telefono": contacto.get("cr321_phone"),
                    }

                chats.append(chat)

            return (
                jsonify(
                    {
                        "success": True,
                        "total": data.get("@odata.count", len(chats)),
                        "grupo_id": grupo_id,
                        "data": chats,
                    }
                ),
                200,
            )

        else:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": f"Error {response.status_code}: {response.text[:200]}",
                    }
                ),
                response.status_code,
            )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@bp.route("/api/chats/estadisticas-grupos", methods=["GET"])
def get_estadisticas_grupos():
    """
    Obtener estadísticas de mensajes por grupo

    Returns:
        JSON con conteo de mensajes por cada grupo

    Ejemplo:
        GET /api/chats/estadisticas-grupos
    """
    try:
        url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s"

        params = {
            "$select": "cr321_adatawp0id",
            "$expand": "cr321_grupoid($select=cr321_grupoid,cr321_nombre,cr321_tipo)",
            "$filter": "_cr321_grupoid_value ne null",
            "$top": 5000,  # Ajustar según volumen
        }

        response = requests.get(url, headers=get_headers(), params=params, timeout=45)

        if response.status_code == 200:
            data = response.json()

            # Contar por grupo
            grupos_stats = {}
            for item in data.get("value", []):
                grupo = item.get("cr321_grupoid", {})
                if grupo:
                    grupo_id = grupo.get("cr321_grupoid")  # Este es el GUID correcto
                    if grupo_id not in grupos_stats:
                        grupos_stats[grupo_id] = {
                            "id": grupo_id,
                            "nombre": grupo.get("cr321_nombre"),
                            "tipo": grupo.get("cr321_tipo"),
                            "total_mensajes": 0,
                        }
                    grupos_stats[grupo_id]["total_mensajes"] += 1

            # Convertir a lista ordenada
            stats_list = sorted(
                grupos_stats.values(), key=lambda x: x["total_mensajes"], reverse=True
            )

            return (
                jsonify(
                    {
                        "success": True,
                        "total_grupos": len(stats_list),
                        "data": stats_list,
                    }
                ),
                200,
            )

        else:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": f"Error {response.status_code}: {response.text[:200]}",
                    }
                ),
                response.status_code,
            )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@bp.route("/api/chats/buscar", methods=["GET"])
def buscar_chats():
    """
    Búsqueda avanzada de chats con múltiples filtros

    Query params:
        - texto: buscar en cr321_body (contains)
        - grupo_id: filtrar por grupo
        - contacto_id: filtrar por contacto
        - fecha_desde: fecha inicio (ISO format)
        - fecha_hasta: fecha fin (ISO format)
        - top: límite de resultados (default 50)

    Returns:
        JSON con chats que coinciden con los filtros

    Ejemplo:
        GET /api/chats/buscar?texto=precio&grupo_id={guid}&top=20
    """
    try:
        texto = request.args.get("texto", "")
        grupo_id = request.args.get("grupo_id", "")
        contacto_id = request.args.get("contacto_id", "")
        fecha_desde = request.args.get("fecha_desde", "")
        fecha_hasta = request.args.get("fecha_hasta", "")
        top = request.args.get("top", 50, type=int)

        # Construir filtros
        filters = []

        if texto:
            filters.append(f"contains(cr321_body, '{texto}')")

        if grupo_id:
            filters.append(f"_cr321_grupoid_value eq {grupo_id}")

        if contacto_id:
            filters.append(f"_cr321_contactorelacion_value eq {contacto_id}")

        if fecha_desde:
            filters.append(f"cr321_createdon ge {fecha_desde}")

        if fecha_hasta:
            filters.append(f"cr321_createdon le {fecha_hasta}")

        if not filters:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Debe proporcionar al menos un filtro de búsqueda",
                    }
                ),
                400,
            )

        filter_str = " and ".join(filters)

        url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s"

        params = {
            "$select": "cr321_adatawp0id,cr321_body,cr321_createdon,cr321_fromname,cr321_phone",
            "$expand": "cr321_grupoid($select=cr321_nombre),cr321_contactorelacion($select=cr321_fromnombre,cr321_telefono)",
            "$filter": filter_str,
            "$orderby": "cr321_createdon desc",
            "$top": top,
            "$count": "true",
        }

        response = requests.get(url, headers=get_headers(), params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()

            chats = []
            for item in data.get("value", []):
                grupo = item.get("cr321_grupoid", {})
                contacto = item.get("cr321_contactorelacion", {})

                chat = {
                    "id": item.get("cr321_adatawp0id"),
                    "mensaje": item.get("cr321_body"),
                    "fecha_hora": item.get("cr321_createdon"),
                    "from_nombre": item.get("cr321_fromname"),
                    "telefono": item.get("cr321_phone"),
                    "grupo_nombre": grupo.get("cr321_nombre") if grupo else None,
                    "contacto_nombre": (
                        contacto.get("cr321_fromname") if contacto else None
                    ),
                }
                chats.append(chat)

            return (
                jsonify(
                    {
                        "success": True,
                        "total": data.get("@odata.count", len(chats)),
                        "filtros_aplicados": {
                            "texto": texto,
                            "grupo_id": grupo_id,
                            "contacto_id": contacto_id,
                            "fecha_desde": fecha_desde,
                            "fecha_hasta": fecha_hasta,
                        },
                        "data": chats,
                    }
                ),
                200,
            )

        else:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": f"Error {response.status_code}: {response.text[:200]}",
                    }
                ),
                response.status_code,
            )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@bp.route("/api/chats/contacto/<contacto_id>/historial", methods=["GET"])
def get_historial_contacto(contacto_id):
    """
    Obtener historial completo de mensajes de un contacto

    Args:
        contacto_id: GUID del contacto

    Query params:
        - ordenar: 'asc' o 'desc' (default asc para timeline)

    Returns:
        JSON con timeline completo del contacto

    Ejemplo:
        GET /api/chats/contacto/{contacto_id}/historial
    """
    try:
        orden = request.args.get("ordenar", "asc")
        orderby = f"cr321_createdon {orden}"

        url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s"

        params = {
            "$select": "cr321_adatawp0id,cr321_body,cr321_createdon,cr321_direction,cr321_fromname",
            "$expand": "cr321_grupoid($select=cr321_nombre,cr321_tipo)",
            "$filter": f"_cr321_contactorelacion_value eq {contacto_id}",
            "$orderby": orderby,
            "$count": "true",
        }

        response = requests.get(url, headers=get_headers(), params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()

            historial = []
            for item in data.get("value", []):
                grupo = item.get("cr321_grupoid", {})

                mensaje = {
                    "id": item.get("cr321_adatawp0id"),
                    "mensaje": item.get("cr321_body"),
                    "fecha_hora": item.get("cr321_createdon"),
                    "direccion": item.get("cr321_direction"),  # 1=entrante, 2=saliente
                    "from_nombre": item.get("cr321_fromname"),
                    "grupo": (
                        {
                            "nombre": grupo.get("cr321_nombre"),
                            "tipo": grupo.get("cr321_tipo"),
                        }
                        if grupo
                        else None
                    ),
                }
                historial.append(mensaje)

            # Estadísticas del historial
            total = len(historial)
            entrantes = sum(1 for m in historial if m["direccion"] == 1)
            salientes = sum(1 for m in historial if m["direccion"] == 2)

            return (
                jsonify(
                    {
                        "success": True,
                        "contacto_id": contacto_id,
                        "total_mensajes": total,
                        "resumen": {
                            "entrantes": entrantes,
                            "salientes": salientes,
                            "primera_interaccion": (
                                historial[0]["fecha_hora"] if historial else None
                            ),
                            "ultima_interaccion": (
                                historial[-1]["fecha_hora"] if historial else None
                            ),
                        },
                        "historial": historial,
                    }
                ),
                200,
            )

        else:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": f"Error {response.status_code}: {response.text[:200]}",
                    }
                ),
                response.status_code,
            )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# Endpoint de health check
@bp.route("/api/chats/health", methods=["GET"])
def health_check():
    """Verificar que la API está funcionando"""
    return (
        jsonify(
            {
                "success": True,
                "message": "Chats Extended API funcionando correctamente",
                "endpoints": [
                    "GET /api/chats/con-contacto",
                    "GET /api/chats/por-grupo/<grupo_id>",
                    "GET /api/chats/estadisticas-grupos",
                    "GET /api/chats/buscar",
                    "GET /api/chats/contacto/<contacto_id>/historial",
                ],
            }
        ),
        200,
    )
