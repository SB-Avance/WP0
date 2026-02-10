"""
Script para verificar campos reales de las tablas
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


def verificar_tabla(tabla_nombre, descripcion):
    """Verificar campos de una tabla"""
    print(f"\n{'='*60}")
    print(f"📋 {descripcion} ({tabla_nombre})")
    print(f"{'='*60}")
    
    token = get_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'OData-MaxVersion': '4.0',
        'OData-Version': '4.0',
        'Accept': 'application/json'
    }
    
    # Obtener un registro de ejemplo
    url = f"{DATAVERSE_URL}/api/data/v9.2/{tabla_nombre}?$top=1"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json().get("value", [])
        if data:
            campos = list(data[0].keys())
            print(f"\n✅ Tabla existe - Campos encontrados ({len(campos)}):\n")
            for campo in sorted(campos):
                if campo.startswith("cr321_") or campo in ["@odata.etag"]:
                    print(f"   - {campo}")
        else:
            print(f"\n⚠️ Tabla existe pero no tiene registros")
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(response.text[:200])


if __name__ == "__main__":
    verificar_tabla("cr321_contactos", "CONTACTOS")
    verificar_tabla("cr321_adatawp0s", "CHATS WHATSAPP")
    verificar_tabla("cr321_grups", "GRUPOS")
