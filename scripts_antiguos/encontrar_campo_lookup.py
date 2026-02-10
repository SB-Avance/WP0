"""
Script para encontrar todos los campos Lookup en cr321_adatawp0
"""
import requests
import os
from dotenv import load_dotenv
from msal import ConfidentialClientApplication

env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend', '.env')
load_dotenv(env_path)

DATAVERSE_URL = os.getenv("DATAVERSE_URL")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")


def get_token():
    authority = f"https://login.microsoftonline.com/{TENANT_ID}"
    app = ConfidentialClientApplication(
        CLIENT_ID,
        authority=authority,
        client_credential=CLIENT_SECRET
    )
    result = app.acquire_token_for_client(scopes=[f"{DATAVERSE_URL}/.default"])
    return result["access_token"] if "access_token" in result else None


print("🔍 Buscando todos los campos Lookup en cr321_adatawp0...\n")

token = get_token()
headers = {
    'Authorization': f'Bearer {token}',
    'OData-MaxVersion': '4.0',
    'OData-Version': '4.0',
    'Accept': 'application/json'
}

url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions(LogicalName='cr321_adatawp0')/Attributes"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    atributos = response.json().get("value", [])
    
    lookups = []
    contacto_fields = []
    
    for attr in atributos:
        attr_type = attr.get("AttributeTypeName", {}).get("Value", "")
        logical_name = attr.get("LogicalName", "")
        
        # Buscar campos Lookup
        if "Lookup" in attr_type:
            targets = attr.get("Targets", [])
            lookups.append({
                "nombre": logical_name,
                "tipo": attr_type,
                "targets": targets
            })
        
        # Buscar campos que contengan "contacto"
        if "contacto" in logical_name.lower():
            contacto_fields.append({
                "nombre": logical_name,
                "tipo": attr_type,
                "attribute_type": attr.get("AttributeType")
            })
    
    print("=" * 60)
    print("📋 CAMPOS LOOKUP ENCONTRADOS:")
    print("=" * 60)
    for lookup in lookups:
        print(f"\n✅ {lookup['nombre']}")
        print(f"   Tipo: {lookup['tipo']}")
        print(f"   Apunta a: {', '.join(lookup['targets'])}")
        
        # Marcar si apunta a contacto
        if 'cr321_contacto' in lookup['targets']:
            print("   🎯 ← ESTE ES EL CAMPO QUE BUSCAMOS!")
    
    print("\n" + "=" * 60)
    print("📝 TODOS LOS CAMPOS QUE CONTIENEN 'CONTACTO':")
    print("=" * 60)
    for field in contacto_fields:
        print(f"\n- {field['nombre']}")
        print(f"  Tipo: {field['tipo']}")
        print(f"  AttributeType: {field['attribute_type']}")
    
    if not lookups:
        print("\n⚠️ No se encontraron campos Lookup")
    
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text[:500])
