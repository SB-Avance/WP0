"""
Script de prueba directo a Dataverse para cr321_chatbot
"""

import os
import requests
from dotenv import load_dotenv
import msal

# Cargar variables de entorno desde backend/.env
env_path = os.path.join(os.path.dirname(__file__), 'backend', '.env')
load_dotenv(env_path)

TENANT_ID = os.getenv('TENANT_ID')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
DATAVERSE_URL = os.getenv('DATAVERSE_URL')
SCOPE = [f"{DATAVERSE_URL}/.default"]

def get_access_token():
    """Obtiene token de acceso usando MSAL"""
    authority = f"https://login.microsoftonline.com/{TENANT_ID}"
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=authority,
        client_credential=CLIENT_SECRET
    )
    
    result = app.acquire_token_for_client(scopes=SCOPE)
    
    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception(f"Error obteniendo token: {result.get('error_description')}")


def test_direct_query(token):
    """Prueba consulta directa a cr321_chatbot"""
    
    # Intentar con diferentes nombres
    test_names = [
        "cr321_chatbot",
        "cr321_chatbots",
        "cr321_chatbot"
    ]
    
    for entity_name in test_names:
        url = f"{DATAVERSE_URL}/api/data/v9.2/{entity_name}?$select=cr321_chatbotid,cr321_name,cr321_active&$top=1"
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "OData-MaxVersion": "4.0",
            "OData-Version": "4.0"
        }
        
        print(f"\nProbando: {entity_name}")
        print(f"URL: {url}")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                records = data.get('value', [])
                print(f"✓ EXITO! Status: {response.status_code}")
                print(f"  Registros encontrados: {len(records)}")
                if records:
                    print(f"  Primer registro: {records[0].get('cr321_name')}")
                return entity_name
            else:
                print(f"✗ Error: {response.status_code}")
                print(f"  Detalle: {response.text[:200]}")
                
        except Exception as e:
            print(f"✗ Excepción: {e}")
    
    return None


def main():
    """Función principal"""
    print("=" * 60)
    print("PRUEBA DIRECTA A DATAVERSE - cr321_chatbot")
    print("=" * 60)
    
    token = get_access_token()
    print("✓ Token obtenido")
    
    working_name = test_direct_query(token)
    
    if working_name:
        print(f"\n{'=' * 60}")
        print(f"RESULTADO: Usar '{working_name}' en el código")
        print(f"{'=' * 60}")
    else:
        print(f"\n{'=' * 60}")
        print(f"ERROR: No se pudo encontrar la tabla")
        print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
