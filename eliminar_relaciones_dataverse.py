"""
Script para eliminar relaciones (lookups) de una columna en una tabla de Dataverse
Requiere: variables de entorno en backend/.env (CLIENT_ID, CLIENT_SECRET, TENANT_ID, DATAVERSE_URL)
Uso: python eliminar_relaciones_dataverse.py <tabla_logica> <columna_logica>
"""

import os
import sys

import requests
from dotenv import load_dotenv
from msal import ConfidentialClientApplication

if len(sys.argv) != 3:
    print(
        "Uso: python eliminar_relaciones_dataverse.py <tabla_logica> <columna_logica>"
    )
    sys.exit(1)

logical_table = sys.argv[1]
logical_column = sys.argv[2]

# Cargar variables de entorno
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend", ".env")
load_dotenv(env_path)
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
DATAVERSE_URL = os.getenv("DATAVERSE_URL")


def get_token():
    authority = f"https://login.microsoftonline.com/{TENANT_ID}"
    app = ConfidentialClientApplication(
        CLIENT_ID, authority=authority, client_credential=CLIENT_SECRET
    )
    result = app.acquire_token_for_client(scopes=[f"{DATAVERSE_URL}/.default"])
    if "access_token" in result:
        return result["access_token"]
    else:
        print(f"Error obteniendo token: {result.get('error_description', 'Unknown')}")
        sys.exit(1)


def get_relationships(token, logical_table, logical_column):
    url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions(LogicalName='{logical_table}')/ManyToOneRelationships?$select=SchemaName,ReferencingAttribute,MetadataId"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print(f"Error consultando relaciones: {resp.text}")
        sys.exit(1)
    data = resp.json().get("value", [])
    # Filtrar relaciones que usan la columna
    return [r for r in data if r.get("ReferencingAttribute") == logical_column]


def delete_relationship(token, metadata_id):
    url = f"{DATAVERSE_URL}/api/data/v9.2/RelationshipDefinitions({metadata_id})"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    resp = requests.delete(url, headers=headers)
    if resp.status_code in (204, 200):
        print(f"✅ Relación {metadata_id} eliminada")
    else:
        print(f"❌ Error eliminando relación {metadata_id}: {resp.text}")


def main():
    token = get_token()
    relaciones = get_relationships(token, logical_table, logical_column)
    if not relaciones:
        print(
            f"No se encontraron relaciones para la columna {logical_column} en la tabla {logical_table}"
        )
        return
    print(f"Relaciones encontradas:")
    for r in relaciones:
        print(f"- {r['SchemaName']} (MetadataId: {r['MetadataId']})")
    for r in relaciones:
        delete_relationship(token, r["MetadataId"])
    print("Listo. Ahora puedes eliminar la columna desde el portal o API.")


if __name__ == "__main__":
    main()
