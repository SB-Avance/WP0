"""
Script para consultar dependencias de una tabla en Dataverse
"""
import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend', '.env')
load_dotenv(env_path)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
DATAVERSE_URL = os.getenv("DATAVERSE_URL")

from msal import ConfidentialClientApplication
import requests
import json

def get_token():
    """Obtener token"""
    try:
        authority = f"https://login.microsoftonline.com/{TENANT_ID}"
        app = ConfidentialClientApplication(
            CLIENT_ID,
            authority=authority,
            client_credential=CLIENT_SECRET
        )
        result = app.acquire_token_for_client(scopes=[f"{DATAVERSE_URL}/.default"])
        return result.get("access_token") if "access_token" in result else None
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_table_dependencies(token, table_logical_name):
    """Obtener dependencias de una tabla"""
    
    # Obtener metadata de la tabla
    url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions(LogicalName='{table_logical_name}')?$select=LogicalName,DisplayName&$expand=Attributes($select=LogicalName,AttributeType),OneToManyRelationships($select=ReferencedEntity,ReferencingEntity,SchemaName),ManyToOneRelationships($select=ReferencedEntity,ReferencingEntity,SchemaName)"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"Excepción: {e}")
        return None

def main():
    print("=" * 70)
    print("🔍 CONSULTAR DEPENDENCIAS DE TABLA")
    print("=" * 70)
    
    # Cambiar este nombre por la tabla que quieres consultar
    tabla_a_consultar = "cr321_grup"  # Tabla nueva (singular)
    
    print(f"\nConsultando dependencias de: {tabla_a_consultar}...")
    
    token = get_token()
    if not token:
        print("❌ No se pudo obtener token")
        return
    
    metadata = get_table_dependencies(token, tabla_a_consultar)
    
    if not metadata:
        print(f"❌ No se encontró la tabla '{tabla_a_consultar}'")
        print("\nPosibles nombres:")
        print("  - cr321_grup")
        print("  - cr321_grupo1")
        print("  - cr321_grupo")
        return
    
    print(f"\n✅ Tabla encontrada: {metadata.get('LogicalName')}")
    print(f"   Nombre mostrado: {metadata.get('DisplayName', {}).get('UserLocalizedLabel', {}).get('Label', 'N/A')}")
    
    # Relaciones 1:N (esta tabla es referenciada por otras)
    one_to_many = metadata.get('OneToManyRelationships', [])
    if one_to_many:
        print(f"\n📌 DEPENDENCIAS (Otras tablas que referencian a {tabla_a_consultar}):")
        print("-" * 70)
        for rel in one_to_many:
            referencing = rel.get('ReferencingEntity')
            schema_name = rel.get('SchemaName')
            print(f"  • {referencing} (relación: {schema_name})")
        print(f"\n⚠️  Debes eliminar estas {len(one_to_many)} dependencias primero:")
        print("    1. Ir a cada tabla que referencia")
        print("    2. Eliminar campos de tipo Lookup que apunten a esta tabla")
    else:
        print(f"\n✅ No hay tablas que referencien a {tabla_a_consultar}")
    
    # Relaciones N:1 (esta tabla referencia a otras)
    many_to_one = metadata.get('ManyToOneRelationships', [])
    if many_to_one:
        print(f"\n🔗 REFERENCIAS (Tablas a las que {tabla_a_consultar} apunta):")
        print("-" * 70)
        for rel in many_to_one:
            referenced = rel.get('ReferencedEntity')
            schema_name = rel.get('SchemaName')
            print(f"  • {referenced} (relación: {schema_name})")
        print("\n💡 Estas son seguras - son campos en esta tabla que puedes eliminar")
    
    print("\n" + "=" * 70)
    print("📋 PASOS PARA ELIMINAR LA TABLA:")
    print("=" * 70)
    if one_to_many:
        print("1. Eliminar campos Lookup en las tablas dependientes (listadas arriba)")
        print("2. Eliminar todos los registros de la tabla")
        print("3. Eliminar vistas y formularios personalizados")
        print("4. Finalmente, eliminar la tabla")
    else:
        print("1. Eliminar todos los registros de la tabla")
        print("2. Eliminar la tabla directamente")
    print("=" * 70)

if __name__ == "__main__":
    main()
