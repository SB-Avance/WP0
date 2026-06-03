import json
import os

import requests
from dotenv import load_dotenv

# Cargar variables de entorno desde backend/.env
env_path = os.path.join(os.path.dirname(__file__), "backend", ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    print(f"⚠️  Archivo .env no encontrado en {env_path}")

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
DATAVERSE_URL = os.getenv("DATAVERSE_URL")
SCOPE = [f"{DATAVERSE_URL}/.default"]

# Validar variables requeridas
missing = []
for var in ["TENANT_ID", "CLIENT_ID", "CLIENT_SECRET", "DATAVERSE_URL"]:
    if not os.getenv(var):
        missing.append(var)
if missing:
    print(f"❌ Faltan variables de entorno: {', '.join(missing)}")
    exit(1)

# Obtener token


def get_access_token():
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": f"{DATAVERSE_URL}/.default",
        "grant_type": "client_credentials",
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception(f"Error obteniendo token: {response.text}")


# Crear tabla


def crear_tabla(nombre_logico, display_name):
    token = get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions"
    body = {
        "LogicalName": nombre_logico,
        "SchemaName": nombre_logico.capitalize(),
        "DisplayName": {
            "LocalizedLabels": [{"Label": display_name, "LanguageCode": 3082}]
        },
        "Description": {
            "LocalizedLabels": [
                {"Label": f"Tabla {display_name}", "LanguageCode": 3082}
            ]
        },
        "OwnershipType": "UserOwned",
        "IsActivity": False,
        "HasActivities": False,
        "HasNotes": True,
        "PrimaryNameAttribute": f"{nombre_logico}_name",
    }
    response = requests.post(url, headers=headers, data=json.dumps(body))
    if response.status_code == 201:
        print(f"Tabla '{display_name}' creada correctamente.")
    else:
        print(f"Error: {response.status_code}", response.text)


if __name__ == "__main__":
    print("=== Crear tabla personalizada en Dataverse ===")
    nombre_logico = input("Nombre lógico de la tabla (ej: cr321_ejemplo): ").strip()
    display_name = input("Nombre visible de la tabla (ej: Ejemplo): ").strip()
    if not nombre_logico or not display_name:
        print("❌ Debes ingresar ambos nombres.")
    else:
        crear_tabla(nombre_logico, display_name)
