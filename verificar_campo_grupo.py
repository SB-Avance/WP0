"""
Verificar si el campo cr321_grupo existe y es editable en cr321_adatawp0s
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

auth_response = requests.post(auth_url, data=auth_data)
token = auth_response.json().get("access_token")
headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

print("\n=== VERIFICANDO CAMPO cr321_grupo ===\n")

# Obtener un mensaje de muestra
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$top=1"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    mensajes = data.get("value", [])
    
    if mensajes:
        msg = mensajes[0]
        print("Campos disponibles en un mensaje:")
        for key in sorted(msg.keys()):
            if not key.startswith("@"):
                value = msg[key]
                print(f"   {key}: {value}")
        
        # Verificar si tiene cr321_grupo
        if "cr321_grupo" in msg:
            print(f"\n✅ Campo cr321_grupo EXISTE")
            print(f"   Valor actual: {msg['cr321_grupo']}")
        else:
            print(f"\n❌ Campo cr321_grupo NO EXISTE")
            print("\n💡 El campo debe ser creado en Dataverse primero")
    else:
        print("❌ No hay mensajes en la tabla")
else:
    print(f"❌ Error: {response.status_code}")
