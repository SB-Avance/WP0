"""
Script de prueba para verificar la función de creación automática de contactos
SIN importaciones circulares
"""

import requests
import os
from dotenv import load_dotenv
from msal import ConfidentialClientApplication
from datetime import datetime, timezone

# Cargar configuración
env_path = os.path.join(os.path.dirname(__file__), 'backend', '.env')
load_dotenv(env_path)

DATAVERSE_URL = os.getenv("DATAVERSE_URL")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")

def get_access_token():
    """Obtener token de acceso para Dataverse usando MSAL"""
    try:
        authority = f"https://login.microsoftonline.com/{TENANT_ID}"
        app = ConfidentialClientApplication(
            CLIENT_ID,
            authority=authority,
            client_credential=CLIENT_SECRET
        )
        result = app.acquire_token_for_client(scopes=[f"{DATAVERSE_URL}/.default"])
        
        if "access_token" in result:
            return result["access_token"]
        else:
            raise Exception(f"Error al obtener token: {result.get('error_description', 'Unknown')}")
    except Exception as e:
        raise Exception(f"Excepción al obtener token: {e}")

def crear_contacto_automatico(telefono, nombre=None):
    """
    Crear o obtener contacto automáticamente desde mensaje de WhatsApp
    Retorna el ID del contacto (existente o creado)
    """
    token = get_access_token()
    if not token:
        print("[CONTACTO] No se pudo obtener token")
        return None
    
    headers = {
        'Authorization': f'Bearer {token}',
        'OData-MaxVersion': '4.0',
        'OData-Version': '4.0',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    try:
        # 1. Verificar si ya existe contacto con ese teléfono
        url_buscar = f"{DATAVERSE_URL}/api/data/v9.2/cr321_contactos"
        params = {
            "$filter": f"cr321_telefono eq '{telefono}'",
            "$select": "cr321_contactoid,cr321_fromnombre,cr321_telefono"
        }
        
        response = requests.get(url_buscar, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            contactos = response.json().get("value", [])
            if contactos:
                print(f"   ✅ Contacto existente: {contactos[0]['cr321_contactoid']}")
                return contactos[0]['cr321_contactoid']
        
        # 2. Crear nuevo contacto
        nombre_limpio = nombre.strip() if nombre else f"Contacto {telefono}"
        
        url_crear = f"{DATAVERSE_URL}/api/data/v9.2/cr321_contactos"
        payload = {
            "cr321_fromnombre": nombre_limpio,
            "cr321_telefono": telefono,
            "cr321_descripcion": "Contacto creado automáticamente desde WhatsApp - TEST",
            "cr321_fechacreacion": datetime.now(timezone.utc).isoformat()
        }
        
        response = requests.post(url_crear, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 204:
            # Obtener ID del contacto creado
            contacto_url = response.headers.get('OData-EntityId')
            if contacto_url:
                contacto_id = contacto_url.split('(')[1].split(')')[0]
                print(f"   ✅ Nuevo contacto creado: {contacto_id}")
                return contacto_id
            else:
                # Buscar el contacto recién creado
                response2 = requests.get(url_buscar, params=params, headers=headers, timeout=10)
                if response2.status_code == 200:
                    contactos = response2.json().get("value", [])
                    if contactos:
                        print(f"   ✅ Contacto encontrado después de crear: {contactos[0]['cr321_contactoid']}")
                        return contactos[0]['cr321_contactoid']
        else:
            print(f"   ❌ Error al crear: {response.status_code}")
            print(f"   {response.text[:200]}")
            return None
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

print("=" * 60)
print("PRUEBA: Creación Automática de Contactos (sin import circular)")
print("=" * 60)

# 1. Verificar configuración
print("\n1️⃣  Verificando configuración...")
print(f"   URL: {DATAVERSE_URL}")
print(f"   Tenant: {TENANT_ID[:8]}...")

# 2. Probar con número de prueba
print("\n2️⃣  Probando crear_contacto_automatico()...")
telefono_prueba = "+34666777999"
nombre_prueba = "Test Webhook Auto"

print(f"   📱 Teléfono: {telefono_prueba}")
print(f"   👤 Nombre: {nombre_prueba}")

contacto_id = crear_contacto_automatico(telefono_prueba, nombre_prueba)

if contacto_id:
    print(f"\n✅ ÉXITO - Contacto ID: {contacto_id}")
else:
    print(f"\n❌ FALLO - No se pudo procesar contacto")

print("\n" + "=" * 60)
