"""
API para gestión de Tickets en Dataverse
Tabla: cr321_tickets

Campos:
- cr321_ticketid (PK, GUID)
- cr321_idticket (consecutivo, int)
- cr321_fromnombre (string - nombre del contacto)
- cr321_telefono (string - teléfono del contacto)
- cr321_empresa (string - empresa del contacto)
- cr321_descripcion (string - descripción del ticket)
- cr321_tipo (int - tipo de ticket: 1=Soporte, 2=Cotización, 3=Información, 4=Atención Agente)
- cr321_grupoId (Lookup - relación a cr321_grup)
- cr321_estadoId (Lookup - relación a cr321_estado)
- cr321_contactoId (Lookup - relación a cr321_contacto)
- cr321_fechacreacion (datetime)
- cr321_fechaactualizacion (datetime)
"""
from flask import Blueprint, request, jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from goot import get_token, DATAVERSE_URL
import requests
from datetime import datetime, timezone

bp_tickets = Blueprint('tickets', __name__)

# Mapeo de tipos de ticket
TIPO_TICKET_MAP = {
    "soporte": 462410000,
    "cotizacion": 462410001,
    "informacion": 462410002,
    "atencion_agente": 462410003
}

TIPO_TICKET_REVERSE = {v: k for k, v in TIPO_TICKET_MAP.items()}


def get_next_ticket_id():
    """Obtiene el siguiente ID consecutivo para ticket"""
    token = get_token()
    if not token:
        return 1
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_ticketses?$select=cr321_idticket&$orderby=cr321_idticket desc&$top=1"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            tickets = data.get("value", [])
            if tickets:
                return tickets[0].get("cr321_idticket", 0) + 1
        return 1
    except Exception as e:
        print(f"Error obteniendo próximo ID de ticket: {e}")
        return 1


@bp_tickets.route('/api/tickets', methods=['GET'])
def get_tickets():
    """Obtener lista de tickets. Filtros opcionales: grupo, estado, tipo"""
    grupo_id = request.args.get('grupo')
    estado_id = request.args.get('estado')
    tipo = request.args.get('tipo')
    
    token = get_token()
    if not token:
        return jsonify({"error": "No se pudo autenticar con Dataverse"}), 503
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_ticketses?$select=cr321_ticketid,cr321_idticket,cr321_fromnombre,cr321_telefono,cr321_empresa,cr321_descripcion,cr321_tipo,cr321_estado,cr321_fechacreacion,cr321_fechaactualizacion"
    
    filters = []
    if grupo_id:
        filters.append(f"_cr321_grupoid_value eq {grupo_id}")
    if estado_id:
        filters.append(f"cr321_estado eq {estado_id}")
    if tipo:
        tipo_val = TIPO_TICKET_MAP.get(tipo.lower())
        if tipo_val is not None:
            filters.append(f"cr321_tipo eq {tipo_val}")
    
    if filters:
        url += "&$filter=" + " and ".join(filters)
    
    url += "&$orderby=cr321_fechacreacion desc"
    
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            tickets = []
            for ticket in data.get("value", []):
                tipo_num = ticket.get("cr321_tipo")
                tickets.append({
                    "id": ticket.get("cr321_ticketid"),
                    "idticket": ticket.get("cr321_idticket"),
                    "fromnombre": ticket.get("cr321_fromnombre"),
                    "telefono": ticket.get("cr321_telefono"),
                    "empresa": ticket.get("cr321_empresa", ""),
                    "descripcion": ticket.get("cr321_descripcion", ""),
                    "tipo": TIPO_TICKET_REVERSE.get(tipo_num, "soporte"),
                    "estado": ticket.get("cr321_estado"),
                    "fechacreacion": ticket.get("cr321_fechacreacion"),
                    "fechaactualizacion": ticket.get("cr321_fechaactualizacion")
                })
            return jsonify({"tickets": tickets}), 200
        else:
            return jsonify({"error": f"Error Dataverse: {response.status_code}"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_tickets.route('/api/tickets', methods=['POST'])
def create_ticket():
    """Crear nuevo ticket"""
    data = request.get_json()
    fromnombre = data.get("fromnombre")
    telefono = data.get("telefono")
    empresa = data.get("empresa", "")
    descripcion = data.get("descripcion", "")
    tipo = data.get("tipo", "soporte").lower()
    grupo_id = data.get("grupo_id")
    estado_id = data.get("estado_id")  # Lookup a cr321_estado
    contacto_id = data.get("contacto_id")  # Lookup a cr321_contacto
    
    if not fromnombre or not telefono:
        return jsonify({"error": "El nombre y teléfono son obligatorios"}), 400
    
    if tipo not in TIPO_TICKET_MAP:
        return jsonify({"error": "Tipo de ticket inválido"}), 400
    
    token = get_token()
    if not token:
        return jsonify({"error": "No se pudo autenticar con Dataverse"}), 503
    
    # Obtener siguiente ID consecutivo
    next_id = get_next_ticket_id()
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_ticketses"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    
    payload = {
        "cr321_idticket": next_id,
        "cr321_fromnombre": fromnombre,
        "cr321_telefono": telefono,
        "cr321_empresa": empresa,
        "cr321_descripcion": descripcion,
        "cr321_tipo": TIPO_TICKET_MAP[tipo],
        "cr321_fechacreacion": now,
        "cr321_fechaactualizacion": now
    }
    
    # Asociar relaciones si se proporcionan (usando lookups)
    if grupo_id:
        payload["cr321_grupoId@odata.bind"] = f"/cr321_grups({grupo_id})"
    if estado_id:
        payload["cr321_estadoId@odata.bind"] = f"/cr321_estados({estado_id})"
    if contacto_id:
        payload["cr321_contactoId@odata.bind"] = f"/cr321_contactos({contacto_id})"
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 204:
            return jsonify({
                "message": "Ticket creado exitosamente",
                "idticket": next_id
            }), 201
        else:
            return jsonify({"error": f"Error Dataverse: {response.status_code}", "details": response.text}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_tickets.route('/api/tickets/<int:idticket>', methods=['GET'])
def get_ticket(idticket):
    """Obtener detalles de un ticket específico"""
    token = get_token()
    if not token:
        return jsonify({"error": "No se pudo autenticar con Dataverse"}), 503
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_ticketses?$filter=cr321_idticket eq {idticket}"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            tickets = data.get("value", [])
            if tickets:
                ticket = tickets[0]
                tipo_num = ticket.get("cr321_tipo")
                return jsonify({
                    "ticket": {
                        "id": ticket.get("cr321_ticketid"),
                        "idticket": ticket.get("cr321_idticket"),
                        "fromnombre": ticket.get("cr321_fromnombre"),
                        "telefono": ticket.get("cr321_telefono"),
                        "empresa": ticket.get("cr321_empresa", ""),
                        "descripcion": ticket.get("cr321_descripcion", ""),
                        "tipo": TIPO_TICKET_REVERSE.get(tipo_num, "soporte"),
                        "estado": ticket.get("cr321_estado"),
                        "fechacreacion": ticket.get("cr321_fechacreacion"),
                        "fechaactualizacion": ticket.get("cr321_fechaactualizacion")
                    }
                }), 200
            else:
                return jsonify({"error": "Ticket no encontrado"}), 404
        else:
            return jsonify({"error": f"Error Dataverse: {response.status_code}"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_tickets.route('/api/tickets/<int:idticket>', methods=['PUT'])
def update_ticket(idticket):
    """Actualizar un ticket existente"""
    data = request.get_json()
    
    token = get_token()
    if not token:
        return jsonify({"error": "No se pudo autenticar con Dataverse"}), 503
    
    # Buscar el ticket por idticket
    search_url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_ticketses?$filter=cr321_idticket eq {idticket}&$select=cr321_ticketid"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    
    try:
        search_response = requests.get(search_url, headers=headers)
        if search_response.status_code != 200:
            return jsonify({"error": "Ticket no encontrado"}), 404
        
        tickets = search_response.json().get("value", [])
        if not tickets:
            return jsonify({"error": "Ticket no encontrado"}), 404
        
        ticket_guid = tickets[0]["cr321_ticketid"]
        
        # Actualizar el ticket
        update_url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_ticketses({ticket_guid})"
        headers["Content-Type"] = "application/json"
        
        payload = {
            "cr321_fechaactualizacion": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        }
        
        if "descripcion" in data:
            payload["cr321_descripcion"] = data["descripcion"]
        if "estado" in data:
            payload["cr321_estado"] = data["estado"]
        if "tipo" in data:
            tipo = data["tipo"].lower()
            if tipo in TIPO_TICKET_MAP:
                payload["cr321_tipo"] = TIPO_TICKET_MAP[tipo]
        if "empresa" in data:
            payload["cr321_empresa"] = data["empresa"]
        
        response = requests.patch(update_url, json=payload, headers=headers)
        if response.status_code == 204:
            return jsonify({"message": "Ticket actualizado exitosamente"}), 200
        else:
            return jsonify({"error": f"Error Dataverse: {response.status_code}", "details": response.text}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_tickets.route('/api/tickets/<int:idticket>', methods=['DELETE'])
def delete_ticket(idticket):
    """Eliminar un ticket"""
    token = get_token()
    if not token:
        return jsonify({"error": "No se pudo autenticar con Dataverse"}), 503
    
    # Buscar el ticket por idticket
    search_url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_ticketses?$filter=cr321_idticket eq {idticket}&$select=cr321_ticketid"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    
    try:
        search_response = requests.get(search_url, headers=headers)
        if search_response.status_code != 200:
            return jsonify({"error": "Ticket no encontrado"}), 404
        
        tickets = search_response.json().get("value", [])
        if not tickets:
            return jsonify({"error": "Ticket no encontrado"}), 404
        
        ticket_guid = tickets[0]["cr321_ticketid"]
        
        # Eliminar el ticket
        delete_url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_ticketses({ticket_guid})"
        response = requests.delete(delete_url, headers=headers)
        
        if response.status_code == 204:
            return jsonify({"message": "Ticket eliminado exitosamente"}), 200
        else:
            return jsonify({"error": f"Error Dataverse: {response.status_code}", "details": response.text}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500
