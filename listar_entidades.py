"""
Script para listar todas las entidades personalizadas en Dataverse
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


def list_custom_entities(token):
    """Lista todas las entidades personalizadas (cr321_)"""
    url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions?$select=LogicalName,SchemaName,DisplayName"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            entities = data.get('value', [])
            
            # Filtrar solo las entidades cr321_
            custom_entities = [e for e in entities if e.get('LogicalName', '').startswith('cr321_')]
            
            print(f"Entidades personalizadas encontradas: {len(custom_entities)}")
            print()
            
            for entity in custom_entities:
                logical_name = entity.get('LogicalName', '')
                schema_name = entity.get('SchemaName', '')
                display_name_obj = entity.get('DisplayName', {})
                display_labels = display_name_obj.get('LocalizedLabels', [])
                display_name = display_labels[0].get('Label', '') if display_labels else ''
                
                print(f"- LogicalName: {logical_name}")
                print(f"  SchemaName: {schema_name}")
                print(f"  DisplayName: {display_name}")
                print()
                
            return custom_entities
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return []
            
    except Exception as e:
        print(f"Excepción: {e}")
        return []


def main():
    """Función principal"""
    print("=" * 60)
    print("LISTAR ENTIDADES PERSONALIZADAS EN DATAVERSE")
    print("=" * 60)
    print()
    
    token = get_access_token()
    list_custom_entities(token)


if __name__ == "__main__":
    main()
