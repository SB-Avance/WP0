s"""
Script para crear tablas en Dataverse automáticamente vía API
Ejecutar: python crear_tablas_auto.py
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

import requests
from backend.goot import TENANT_ID, CLIENT_ID, CLIENT_SECRET, DATAVERSE_URL
from msal import ConfidentialClientApplication

def get_token():
    """Obtiene token de autenticación"""
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
            print(f"❌ Error al obtener token: {result.get('error_description', 'Unknown error')}")
            return None
    except Exception as e:
        print(f"❌ Excepción al obtener token: {e}")
        return None

def create_table_grupos(token):
    """Crear tabla cr321_grup"""
    print("\n📋 Creando tabla: cr321_grup...")
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Definición simplificada de la tabla
    entity_definition = {
        "@odata.type": "Microsoft.Dynamics.CRM.EntityMetadata",
        "SchemaName": "cr321_grup",
        "DisplayName": {
            "@odata.type": "Microsoft.Dynamics.CRM.Label",
            "LocalizedLabels": [
                {
                    "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                    "Label": "Grupos",
                    "LanguageCode": 1033
                },
                {
                    "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                    "Label": "Grupos",
                    "LanguageCode": 3082  # Español
                }
            ]
        },
        "DisplayCollectionName": {
            "@odata.type": "Microsoft.Dynamics.CRM.Label",
            "LocalizedLabels": [
                {
                    "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                    "Label": "Grupos",
                    "LanguageCode": 1033
                }
            ]
        },
        "Description": {
            "@odata.type": "Microsoft.Dynamics.CRM.Label",
            "LocalizedLabels": [
                {
                    "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                    "Label": "Grupos de categorización para chats",
                    "LanguageCode": 1033
                }
            ]
        },
        "OwnershipType": "UserOwned",
        "IsActivity": False,
        "HasActivities": False,
        "HasNotes": True,
        "Attributes": [
            {
                "@odata.type": "Microsoft.Dynamics.CRM.StringAttributeMetadata",
                "SchemaName": "cr321_nombre",
                "RequiredLevel": {
                    "Value": "ApplicationRequired",
                    "CanBeChanged": True,
                    "ManagedPropertyLogicalName": "canmodifyrequirementlevelsettings"
                },
                "DisplayName": {
                    "@odata.type": "Microsoft.Dynamics.CRM.Label",
                    "LocalizedLabels": [
                        {
                            "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                            "Label": "Nombre",
                            "LanguageCode": 1033
                        }
                    ]
                },
                "Description": {
                    "@odata.type": "Microsoft.Dynamics.CRM.Label",
                    "LocalizedLabels": [
                        {
                            "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                            "Label": "Nombre del grupo",
                            "LanguageCode": 1033
                        }
                    ]
                },
                "MaxLength": 100,
                "FormatName": {
                    "Value": "Text"
                }
            }
        ]
    }
    
    try:
        response = requests.post(url, json=entity_definition, headers=headers)
        if response.status_code == 204:
            print("   ✅ Tabla cr321_grup creada")
            return True
        else:
            print(f"   ❌ Error: {response.status_code}")
            print(f"   Detalles: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"   ❌ Excepción: {e}")
        return False

def main():
    print("\n" + "=" * 60)
    print("🔧 CREACIÓN AUTOMÁTICA DE TABLAS EN DATAVERSE")
    print("=" * 60)
    
    # Verificar variables de entorno
    print("\n🔍 Verificando configuración...")
    if not DATAVERSE_URL or not TENANT_ID or not CLIENT_ID or not CLIENT_SECRET:
        print("❌ ERROR: Variables de entorno no configuradas correctamente")
        print("\nAsegúrate de que .env contenga:")
        print("  - DATAVERSE_URL")
        print("  - TENANT_ID")
        print("  - CLIENT_ID")
        print("  - CLIENT_SECRET")
        return
    
    print(f"   ✅ DATAVERSE_URL: {DATAVERSE_URL}")
    print(f"   ✅ TENANT_ID: {TENANT_ID[:8]}...")
    
    # Obtener token
    print("\n🔐 Obteniendo token de autenticación...")
    token = get_token()
    if not token:
        print("\n❌ No se pudo obtener token de autenticación")
        print("\n⚠️  ALTERNATIVA: Crear tablas manualmente")
        print("   → Seguir guía: GUIA_CREAR_TABLAS_VISUAL.md")
        return
    
    print("   ✅ Token obtenido")
    
    # Nota importante
    print("\n" + "=" * 60)
    print("⚠️  IMPORTANTE:")
    print("=" * 60)
    print("La creación de tablas vía API es compleja y requiere")
    print("definiciones detalladas de metadatos.")
    print("\nRECOMENDACIÓN:")
    print("  1. Crear tablas manualmente en Power Apps")
    print("  2. Seguir: GUIA_CREAR_TABLAS_VISUAL.md")
    print("  3. Toma solo 20-30 minutos")
    print("\nO continuar con creación automática (experimental)?")
    print("=" * 60)
    
    respuesta = input("\n¿Continuar con creación automática? (s/N): ")
    if respuesta.lower() != 's':
        print("\n✋ Creación cancelada")
        print("📖 Abre: GUIA_CREAR_TABLAS_VISUAL.md para instrucciones")
        return
    
    # Intentar crear tablas
    print("\n🚀 Iniciando creación de tablas...")
    
    # Solo intentar crear cr321_grup como ejemplo
    success = create_table_grupos(token)
    
    if success:
        print("\n✅ Tabla creada exitosamente")
        print("\nPuedes crear las demás tablas siguiendo el mismo patrón")
        print("o usar la interfaz de Power Apps (más fácil)")
    else:
        print("\n❌ No se pudo crear la tabla automáticamente")
        print("\n📖 SOLUCIÓN: Usar Power Apps")
        print("   → Seguir: GUIA_CREAR_TABLAS_VISUAL.md")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
