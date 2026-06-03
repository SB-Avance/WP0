"""
Script para ver campos de la tabla cr321_chatbot
"""

import os

import msal
import requests
from dotenv import load_dotenv

# Cargar variables de entorno desde backend/.env
env_path = os.path.join(os.path.dirname(__file__), "backend", ".env")
load_dotenv(env_path)

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
DATAVERSE_URL = os.getenv("DATAVERSE_URL")
SCOPE = [f"{DATAVERSE_URL}/.default"]


def get_access_token():
    """Obtiene token de acceso usando MSAL"""
    authority = f"https://login.microsoftonline.com/{TENANT_ID}"
    app = msal.ConfidentialClientApplication(
        CLIENT_ID, authority=authority, client_credential=CLIENT_SECRET
    )

    result = app.acquire_token_for_client(scopes=SCOPE)

    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception(f"Error obteniendo token: {result.get('error_description')}")


def get_entity_attributes(token):
    """Obtiene atributos de la entidad cr321_chatbot"""
    url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions(LogicalName='cr321_chatbot')/Attributes?$select=LogicalName,SchemaName,AttributeType"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    try:
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            attributes = data.get("value", [])

            print(f"Atributos de cr321_chatbot: {len(attributes)}")
            print()

            # Filtrar solo los personalizados (cr321_)
            custom_attrs = [
                a for a in attributes if a.get("LogicalName", "").startswith("cr321_")
            ]

            for attr in custom_attrs:
                logical_name = attr.get("LogicalName", "")
                schema_name = attr.get("SchemaName", "")
                attr_type = attr.get("AttributeType", "")

                print(f"- {logical_name} (Type: {attr_type})")

            return custom_attrs
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
    print("CAMPOS DE LA TABLA cr321_chatbot")
    print("=" * 60)
    print()

    token = get_access_token()
    get_entity_attributes(token)


if __name__ == "__main__":
    main()
