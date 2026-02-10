"""
Script para probar el campo de lookup cr321_idcontacto
"""
import requests
import os
from dotenv import load_dotenv
from msal import ConfidentialClientApplication

# Cargar configuración desde backend/.env
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend', '.env')
load_dotenv(env_path)

DATAVERSE_URL = os.getenv("DATAVERSE_URL")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")


def get_token():
    """Obtener token de acceso"""
    authority = f"https://login.microsoftonline.com/{TENANT_ID}"
    app = ConfidentialClientApplication(
        CLIENT_ID,
        authority=authority,
        client_credential=CLIENT_SECRET
    )
    result = app.acquire_token_for_client(scopes=[f"{DATAVERSE_URL}/.default"])
    return result["access_token"] if "access_token" in result else None


token = get_token()
headers = {
    'Authorization': f'Bearer {token}',
    'OData-MaxVersion': '4.0',
    'OData-Version': '4.0',
    'Accept': 'application/json'
}

# Intentar obtener mensajes sin especificar filtro
print("1. Obteniendo un mensaje para ver estructura completa...\n")
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$top=1"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json().get("value", [])
    if data:
        mensaje = data[0]
        print("Campos del mensaje que contienen 'contacto':")
        for key in sorted(mensaje.keys()):
            if 'contacto' in key.lower() or 'idcontacto' in key.lower():
                print(f"   - {key}: {mensaje[key]}")
        
        print("\nTodos los campos con 'cr321_':")
        for key in sorted(mensaje.keys()):
            if key.startswith('cr321_'):
                valor = mensaje[key]
                print(f"   - {key}: {valor if len(str(valor)) < 50 else str(valor)[:50] + '...'}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)

# Intentar obtener metadata del campo
print("\n\n2. Obteniendo metadata del campo cr321_idcontacto...\n")
url_meta = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions(LogicalName='cr321_adatawp0')/Attributes(LogicalName='cr321_idcontacto')"
response = requests.get(url_meta, headers=headers)

if response.status_code == 200:
    meta = response.json()
    print(f"Tipo de atributo: {meta.get('AttributeType')}")
    print(f"Tipo de atributo específico: {meta.get('AttributeTypeName', {}).get('Value')}")
    if 'Targets' in meta:
        print(f"Targets (tabla relacionada): {meta.get('Targets')}")
else:
    print(f"Error: {response.status_code}")
    print(response.text[:300])
