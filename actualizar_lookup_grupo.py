"""
Actualizar conversaciones usando el lookup _cr321_grupoid_value
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

import requests
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), 'backend', '.env'))

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
token = auth_response.json().get("access_token")
print("✅")

headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

# Primero, obtener el GUID del grupo Contabilidad (0004)
print("\nObteniendo GUID del grupo Contabilidad...", end=" ")
url_grupo = f"{DATAVERSE_URL}/api/data/v9.2/cr321_grups?$filter=cr321_grupoid eq '0004'"
response_grupo = requests.get(url_grupo, headers=headers)

if response_grupo.status_code != 200:
    print(f"❌ Error {response_grupo.status_code}")
    exit(1)

grupos = response_grupo.json().get("value", [])
if not grupos:
    print("❌ Grupo 0004 no encontrado")
    exit(1)

grupo_guid = grupos[0].get("cr321_grupoid")
print(f"✅ {grupo_guid}")

# Obtener mensajes
print("\nObteniendo mensajes...", end=" ")
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$top=100"
response = requests.get(url, headers=headers)

if response.status_code != 200:
    print(f"❌ Error {response.status_code}")
    exit(1)

mensajes = response.json().get("value", [])
print(f"✅ {len(mensajes)} mensajes")

# Agrupar por teléfono
conversaciones = {}
for msg in mensajes:
    phone = msg.get("cr321_phone")
    if not phone:
        continue
    if phone not in conversaciones:
        conversaciones[phone] = []
    conversaciones[phone].append(msg["cr321_adatawp0id"])

# Seleccionar 2 conversaciones
conv_list = list(conversaciones.items())[:2]

print(f"\nActualizando {len(conv_list)} conversaciones...\n")

headers_update = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "If-Match": "*",
    "Prefer": "return=representation"
}

for phone, mensaje_ids in conv_list:
    print(f"Conversación {phone}: {len(mensaje_ids)} mensajes")
    
    actualizados = 0
    for msg_id in mensaje_ids:
        url_update = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s({msg_id})"
        
        # Usar OData binding para el lookup
        payload = {
            "cr321_grupoid@odata.bind": f"/cr321_grups({grupo_guid})"
        }
        
        resp = requests.patch(url_update, json=payload, headers=headers_update)
        if resp.status_code in [200, 204]:
            actualizados += 1
        else:
            print(f"  ⚠️ Error en mensaje {msg_id[:8]}: {resp.status_code}")
    
    print(f"  ✅ {actualizados}/{len(mensaje_ids)} mensajes actualizados\n")

print("✅ Completado")
