"""
Script simplificado para asignar conversaciones al grupo Contabilidad
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

import requests
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), 'backend', '.env'))

# Autenticación
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET") 
TENANT_ID = os.getenv("TENANT_ID")
DATAVERSE_URL = os.getenv("DATAVERSE_URL")

# Obtener token
auth_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
auth_data = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "scope": f"{DATAVERSE_URL}/.default",
    "grant_type": "client_credentials"
}

print("\nObteniendo token...", end=" ")
auth_response = requests.post(auth_url, data=auth_data)
if auth_response.status_code != 200:
    print(f"❌ Error {auth_response.status_code}")
    print(auth_response.text)
    exit(1)

token = auth_response.json().get("access_token")
print("✅")

headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

# Obtener conversaciones con teléfonos específicos para actualizar
print("\nObteniendo mensajes...", end=" ")
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$top=100"

response = requests.get(url, headers=headers)
if response.status_code != 200:
    print(f"❌ Error {response.status_code}")
    exit(1)

mensajes = response.json().get("value", [])
print(f"✅ {len(mensajes)} mensajes")

# Agrupar por conversación  
conversaciones = {}
for msg in mensajes:
    conv_id = msg.get("cr321_phone")  # Usar teléfono como conversación
    if not conv_id:
        continue
    if conv_id not in conversaciones:
        conversaciones[conv_id] = {
            "mensajes": []
        }
    conversaciones[conv_id]["mensajes"].append(msg["cr321_adatawp0id"])

# Seleccionar primeras 2 conversaciones
conv_list = list(conversaciones.items())[:2]

print(f"\nActualizando {len(conv_list)} conversaciones al grupo 4 (Contabilidad)...\n")

headers_update = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "If-Match": "*"
}

for conv_id, data in conv_list:
    mensaje_ids = data["mensajes"]
    
    print(f"Conversación {conv_id[:20]}... ({len(mensaje_ids)} mensajes)")
    
    for msg_id in mensaje_ids:
        url_update = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s({msg_id})"
        payload = {"cr321_grupo": 4}
        
        resp = requests.patch(url_update, json=payload, headers=headers_update)
        if resp.status_code != 204:
            print(f"  ⚠️ Error en mensaje {msg_id}: {resp.status_code}")
    
    print(f"  ✅ Actualizada\n")

print("✅ Completado. Ahora el usuario 0006 verá 2 conversaciones de Contabilidad")
