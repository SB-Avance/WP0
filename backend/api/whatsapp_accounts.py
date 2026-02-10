"""
API para gestión de Cuentas de WhatsApp en Dataverse
Tabla: cr321_cuentadewhatsapp

Esta tabla permite configurar múltiples cuentas de WhatsApp Business
para el mismo sistema, cada una con su propio:
- Phone Number ID (identificador de número de teléfono)
- Access Token (token de acceso de Meta)
- Verify Token (token de verificación para webhook)
"""
from flask import Blueprint, request, jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from goot import get_token, DATAVERSE_URL
import requests

bp_whatsapp_accounts = Blueprint('whatsapp_accounts', __name__)


@bp_whatsapp_accounts.route('/api/whatsapp-accounts', methods=['GET'])
def get_whatsapp_accounts():
    """Obtener todas las cuentas de WhatsApp"""
    token = get_token()
    if not token:
        return jsonify({"error": "No se pudo obtener token"}), 500
    
    try:
        url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_cuentadewhatsapps"
        url += "?$select=cr321_cuentadewhatsappid,cr321_name,cr321_phonenumberid,cr321_accesstoken,cr321_verifytoken,cr321_activo"
        url += "&$orderby=cr321_name asc"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "OData-MaxVersion": "4.0",
            "OData-Version": "4.0"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            accounts = []
            for item in data.get("value", []):
                accounts.append({
                    "id": item.get("cr321_cuentadewhatsappid"),
                    "nombre": item.get("cr321_name", "Sin nombre"),
                    "phone_number_id": item.get("cr321_phonenumberid", ""),
                    "access_token": item.get("cr321_accesstoken", "")[:20] + "...",  # Ocultar token completo
                    "verify_token": item.get("cr321_verifytoken", ""),
                    "activo": item.get("cr321_activo", False)
                })
            
            return jsonify({"success": True, "accounts": accounts}), 200
        else:
            return jsonify({"error": f"Error al obtener cuentas: {response.status_code}"}), response.status_code
    
    except Exception as e:
        print(f"Error al obtener cuentas WhatsApp: {e}")
        return jsonify({"error": str(e)}), 500


@bp_whatsapp_accounts.route('/api/whatsapp-accounts/<account_id>', methods=['GET'])
def get_whatsapp_account(account_id):
    """Obtener cuenta específica con token completo (para uso interno)"""
    token = get_token()
    if not token:
        return jsonify({"error": "No se pudo obtener token"}), 500
    
    try:
        url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_cuentadewhatsapps({account_id})"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            item = response.json()
            account = {
                "id": item.get("cr321_cuentadewhatsappid"),
                "nombre": item.get("cr321_name"),
                "phone_number_id": item.get("cr321_phonenumberid"),
                "access_token": item.get("cr321_accesstoken"),  # Token completo
                "verify_token": item.get("cr321_verifytoken"),
                "activo": item.get("cr321_activo", False)
            }
            return jsonify({"success": True, "account": account}), 200
        else:
            return jsonify({"error": f"Cuenta no encontrada"}), 404
    
    except Exception as e:
        print(f"Error al obtener cuenta WhatsApp: {e}")
        return jsonify({"error": str(e)}), 500


@bp_whatsapp_accounts.route('/api/whatsapp-accounts/active', methods=['GET'])
def get_active_accounts():
    """Obtener solo cuentas activas (para envío de mensajes)"""
    token = get_token()
    if not token:
        return jsonify({"error": "No se pudo obtener token"}), 500
    
    try:
        url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_cuentadewhatsapps"
        url += "?$select=cr321_cuentadewhatsappid,cr321_name,cr321_phonenumberid,cr321_accesstoken,cr321_verifytoken"
        url += "&$filter=cr321_activo eq true"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            accounts = []
            for item in data.get("value", []):
                accounts.append({
                    "id": item.get("cr321_cuentadewhatsappid"),
                    "nombre": item.get("cr321_name"),
                    "phone_number_id": item.get("cr321_phonenumberid"),
                    "access_token": item.get("cr321_accesstoken"),
                    "verify_token": item.get("cr321_verifytoken")
                })
            
            return jsonify({"success": True, "accounts": accounts}), 200
        else:
            return jsonify({"error": f"Error: {response.status_code}"}), response.status_code
    
    except Exception as e:
        print(f"Error al obtener cuentas activas: {e}")
        return jsonify({"error": str(e)}), 500


@bp_whatsapp_accounts.route('/api/whatsapp-accounts', methods=['POST'])
def create_whatsapp_account():
    """Crear nueva cuenta de WhatsApp"""
    token = get_token()
    if not token:
        return jsonify({"error": "No se pudo obtener token"}), 500
    
    data = request.get_json()
    nombre = data.get("nombre")
    phone_number_id = data.get("phone_number_id")
    access_token = data.get("access_token")
    verify_token = data.get("verify_token", "")
    activo = data.get("activo", True)
    
    if not nombre or not phone_number_id or not access_token:
        return jsonify({"error": "Nombre, phone_number_id y access_token son requeridos"}), 400
    
    try:
        url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_cuentadewhatsapps"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        account_data = {
            "cr321_name": nombre,
            "cr321_phonenumberid": phone_number_id,
            "cr321_accesstoken": access_token,
            "cr321_verifytoken": verify_token,
            "cr321_activo": activo
        }
        
        response = requests.post(url, json=account_data, headers=headers, timeout=10)
        
        if response.status_code in [200, 201, 204]:
            return jsonify({"success": True, "message": "Cuenta creada exitosamente"}), 201
        else:
            return jsonify({"error": f"Error: {response.status_code} - {response.text}"}), response.status_code
    
    except Exception as e:
        print(f"Error al crear cuenta WhatsApp: {e}")
        return jsonify({"error": str(e)}), 500


@bp_whatsapp_accounts.route('/api/whatsapp-accounts/<account_id>', methods=['PATCH'])
def update_whatsapp_account(account_id):
    """Actualizar cuenta de WhatsApp existente"""
    token = get_token()
    if not token:
        return jsonify({"error": "No se pudo obtener token"}), 500
    
    data = request.get_json()
    
    try:
        url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_cuentadewhatsapps({account_id})"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Solo actualizar campos proporcionados
        update_data = {}
        if "nombre" in data:
            update_data["cr321_name"] = data["nombre"]
        if "phone_number_id" in data:
            update_data["cr321_phonenumberid"] = data["phone_number_id"]
        if "access_token" in data:
            update_data["cr321_accesstoken"] = data["access_token"]
        if "verify_token" in data:
            update_data["cr321_verifytoken"] = data["verify_token"]
        if "activo" in data:
            update_data["cr321_activo"] = data["activo"]
        
        response = requests.patch(url, json=update_data, headers=headers, timeout=10)
        
        if response.status_code in [200, 204]:
            return jsonify({"success": True, "message": "Cuenta actualizada exitosamente"}), 200
        else:
            return jsonify({"error": f"Error: {response.status_code}"}), response.status_code
    
    except Exception as e:
        print(f"Error al actualizar cuenta WhatsApp: {e}")
        return jsonify({"error": str(e)}), 500


@bp_whatsapp_accounts.route('/api/whatsapp-accounts/<account_id>', methods=['DELETE'])
def delete_whatsapp_account(account_id):
    """Eliminar cuenta de WhatsApp"""
    token = get_token()
    if not token:
        return jsonify({"error": "No se pudo obtener token"}), 500
    
    try:
        url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_cuentadewhatsapps({account_id})"
        
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        response = requests.delete(url, headers=headers, timeout=10)
        
        if response.status_code in [200, 204]:
            return jsonify({"success": True, "message": "Cuenta eliminada exitosamente"}), 200
        else:
            return jsonify({"error": f"Error: {response.status_code}"}), response.status_code
    
    except Exception as e:
        print(f"Error al eliminar cuenta WhatsApp: {e}")
        return jsonify({"error": str(e)}), 500
