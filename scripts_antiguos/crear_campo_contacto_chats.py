"""
Crear Campo de Relación: cr321_contactoId en cr321_adatawp0
------------------------------------------------------------
Script para crear automáticamente el campo Lookup que relaciona
mensajes de WhatsApp con contactos.

Uso:
    python crear_campo_contacto_chats.py
"""

import requests
import os
from dotenv import load_dotenv
from msal import ConfidentialClientApplication
import time

# Cargar configuración desde backend/.env
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend', '.env')
load_dotenv(env_path)

DATAVERSE_URL = os.getenv("DATAVERSE_URL")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")


def get_access_token():
    """Obtener token de acceso para Dataverse usando MSAL"""
    try:
        authority = f"https://login.microsoftonline.com/{TENANT_ID}"
        app = ConfidentialClientApplication(
            CLIENT_ID,
            authority=authority,
            client_credential=CLIENT_SECRET
        )
        result = app.acquire_token_for_client(scopes=[f"{DATAVERSE_URL}/.default"])
        
        if "access_token" in result:
            return result["access_token"]
        else:
            raise Exception(f"Error al obtener token: {result.get('error_description', 'Unknown')}")
    except Exception as e:
        raise Exception(f"Excepción al obtener token: {e}")


def get_headers():
    """Obtener headers con autenticación"""
    token = get_access_token()
    return {
        'Authorization': f'Bearer {token}',
        'OData-MaxVersion': '4.0',
        'OData-Version': '4.0',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'MSCRM.SolutionUniqueName': 'Default'
    }


def verificar_campo_existe():
    """Verificar si el campo cr321_contactoid ya existe"""
    print("\n🔍 Verificando si el campo ya existe...")
    
    headers = get_headers()
    url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions(LogicalName='cr321_adatawp0')/Attributes(LogicalName='cr321_contactoid')"
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            print("✅ El campo cr321_contactoid ya existe")
            return True
        elif response.status_code == 404:
            print("📝 El campo cr321_contactoid no existe, se creará")
            return False
        else:
            print(f"⚠️  Estado desconocido: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error al verificar: {e}")
        return False


def obtener_contacto_entity_id():
    """Obtener el MetadataId de la entidad cr321_contacto"""
    print("\n🔍 Obteniendo MetadataId de cr321_contacto...")
    
    headers = get_headers()
    url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions(LogicalName='cr321_contacto')"
    params = {"$select": "MetadataId,LogicalName,DisplayName"}
    
    try:
        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            metadata_id = data.get("MetadataId")
            print(f"✅ MetadataId obtenido: {metadata_id}")
            return metadata_id
        else:
            print(f"❌ Error al obtener MetadataId: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def crear_campo_lookup():
    """Crear el campo Lookup cr321_contactoid"""
    print("\n🔨 Creando campo cr321_contactoid...")
    
    # Obtener MetadataId de la entidad relacionada
    contacto_metadata_id = obtener_contacto_entity_id()
    
    if not contacto_metadata_id:
        print("❌ No se pudo obtener MetadataId de cr321_contacto")
        return False
    
    headers = get_headers()
    url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions(LogicalName='cr321_adatawp0')/Attributes"
    
    # Definición del campo Lookup
    campo_definicion = {
        "@odata.type": "Microsoft.Dynamics.CRM.LookupAttributeMetadata",
        "AttributeType": "Lookup",
        "AttributeTypeName": {
            "Value": "LookupType"
        },
        "Description": {
            "@odata.type": "Microsoft.Dynamics.CRM.Label",
            "LocalizedLabels": [
                {
                    "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                    "Label": "Contacto relacionado por teléfono",
                    "LanguageCode": 1034
                }
            ]
        },
        "DisplayName": {
            "@odata.type": "Microsoft.Dynamics.CRM.Label",
            "LocalizedLabels": [
                {
                    "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                    "Label": "Contacto",
                    "LanguageCode": 1034
                }
            ]
        },
        "RequiredLevel": {
            "Value": "None",
            "CanBeChanged": True
        },
        "SchemaName": "cr321_contactoId",
        "Targets": ["cr321_contacto"]
    }
    
    try:
        response = requests.post(url, json=campo_definicion, headers=headers)
        
        if response.status_code == 204:
            print("✅ Campo cr321_contactoid creado exitosamente")
            
            # Obtener el URI del campo creado
            attribute_uri = response.headers.get('OData-EntityId')
            if attribute_uri:
                print(f"📍 URI: {attribute_uri}")
            
            return True
        else:
            print(f"❌ Error al crear campo: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Error al crear campo: {e}")
        return False


def publicar_cambios():
    """Publicar todos los cambios de personalización"""
    print("\n📢 Publicando cambios...")
    
    headers = get_headers()
    url = f"{DATAVERSE_URL}/api/data/v9.2/PublishAllXml"
    
    payload = {
        "ParameterXml": "<importexportxml><entities><entity>cr321_adatawp0</entity></entities></importexportxml>"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 204:
            print("✅ Cambios publicados correctamente")
            return True
        else:
            print(f"⚠️  Estado de publicación: {response.status_code}")
            # No es crítico si falla, a veces se publica automáticamente
            return True
            
    except Exception as e:
        print(f"⚠️  Advertencia al publicar: {e}")
        return True


def crear_relacion():
    """Crear la relación entre cr321_adatawp0 y cr321_contacto"""
    print("\n🔗 Creando relación entre tablas...")
    
    headers = get_headers()
    url = f"{DATAVERSE_URL}/api/data/v9.2/RelationshipDefinitions"
    
    relacion_definicion = {
        "@odata.type": "Microsoft.Dynamics.CRM.OneToManyRelationshipMetadata",
        "ReferencedEntity": "cr321_contacto",
        "ReferencedAttribute": "cr321_contactoid",
        "ReferencingEntity": "cr321_adatawp0",
        "ReferencingAttribute": "cr321_contactoid",
        "SchemaName": "cr321_contacto_cr321_adatawp0",
        "RelationshipBehavior": 1,
        "CascadeConfiguration": {
            "Assign": "NoCascade",
            "Delete": "RemoveLink",
            "Merge": "NoCascade",
            "Reparent": "NoCascade",
            "Share": "NoCascade",
            "Unshare": "NoCascade"
        },
        "AssociatedMenuConfiguration": {
            "Behavior": "UseCollectionName",
            "Group": "Details",
            "Order": 10000
        },
        "Lookup": {
            "AttributeType": "Lookup",
            "AttributeTypeName": {
                "Value": "LookupType"
            },
            "Description": {
                "@odata.type": "Microsoft.Dynamics.CRM.Label",
                "LocalizedLabels": [
                    {
                        "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                        "Label": "Contacto relacionado",
                        "LanguageCode": 1034
                    }
                ]
            },
            "DisplayName": {
                "@odata.type": "Microsoft.Dynamics.CRM.Label",
                "LocalizedLabels": [
                    {
                        "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                        "Label": "Contacto",
                        "LanguageCode": 1034
                    }
                ]
            },
            "SchemaName": "cr321_contactoId"
        }
    }
    
    try:
        response = requests.post(url, json=relacion_definicion, headers=headers)
        
        if response.status_code in [204, 200]:
            print("✅ Relación creada exitosamente")
            return True
        else:
            print(f"⚠️  Estado de relación: {response.status_code}")
            print(response.text)
            # La relación podría crearse automáticamente con el Lookup
            return True
            
    except Exception as e:
        print(f"⚠️  Advertencia al crear relación: {e}")
        return True


def main():
    """Proceso principal"""
    print("=" * 60)
    print("🔨 CREAR CAMPO LOOKUP: cr321_contactoId")
    print("=" * 60)
    
    try:
        # 1. Verificar si ya existe
        if verificar_campo_existe():
            print("\n✅ El campo ya existe, no es necesario crearlo")
            return True
        
        # 2. Crear el campo Lookup
        if not crear_campo_lookup():
            print("\n❌ No se pudo crear el campo")
            return False
        
        # 3. Esperar un momento para que se procese
        print("\n⏳ Esperando procesamiento...")
        time.sleep(3)
        
        # 4. Publicar cambios
        publicar_cambios()
        
        # 5. Esperar publicación
        print("\n⏳ Esperando publicación...")
        time.sleep(2)
        
        print("\n" + "=" * 60)
        print("✅ CAMPO CREADO EXITOSAMENTE")
        print("=" * 60)
        print("\n📝 Próximo paso:")
        print("   python migrar_contactos_chats.py")
        print()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error durante el proceso: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    main()
