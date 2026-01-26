# Script para crear la tabla cr321_whatsappaccounts en Dataverse
# Azure deployment - 2026-01-25

import requests
from goot import get_token, DATAVERSE_URL

def create_whatsapp_accounts_table():
    """Crea la tabla de Cuentas de WhatsApp en Dataverse"""
    
    token = get_token()
    if not token:
        print("❌ No se pudo obtener token de acceso.")
        return False
    
    # URL para crear entidades (tablas)
    url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0"
    }
    
    # Definición de la tabla
    table_definition = {
        "@odata.type": "Microsoft.Dynamics.CRM.EntityMetadata",
        "SchemaName": "cr321_whatsappaccounts",
        "DisplayName": {
            "@odata.type": "Microsoft.Dynamics.CRM.Label",
            "LocalizedLabels": [
                {
                    "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                    "Label": "Cuentas de WhatsApp",
                    "LanguageCode": 1033
                }
            ]
        },
        "DisplayCollectionName": {
            "@odata.type": "Microsoft.Dynamics.CRM.Label",
            "LocalizedLabels": [
                {
                    "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                    "Label": "Cuentas de WhatsApp",
                    "LanguageCode": 1033
                }
            ]
        },
        "Description": {
            "@odata.type": "Microsoft.Dynamics.CRM.Label",
            "LocalizedLabels": [
                {
                    "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                    "Label": "Gestión de múltiples cuentas de WhatsApp Business API",
                    "LanguageCode": 1033
                }
            ]
        },
        "OwnershipType": "UserOwned",
        "IsActivity": False,
        "HasNotes": False,
        "HasActivities": False,
        "PrimaryNameAttribute": "cr321_name",
        "Attributes": [
            {
                "@odata.type": "Microsoft.Dynamics.CRM.StringAttributeMetadata",
                "SchemaName": "cr321_name",
                "DisplayName": {
                    "@odata.type": "Microsoft.Dynamics.CRM.Label",
                    "LocalizedLabels": [
                        {
                            "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                            "Label": "Nombre de la Cuenta",
                            "LanguageCode": 1033
                        }
                    ]
                },
                "Description": {
                    "@odata.type": "Microsoft.Dynamics.CRM.Label",
                    "LocalizedLabels": [
                        {
                            "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                            "Label": "Nombre identificador de la cuenta",
                            "LanguageCode": 1033
                        }
                    ]
                },
                "RequiredLevel": {
                    "Value": "ApplicationRequired",
                    "CanBeChanged": True,
                    "ManagedPropertyLogicalName": "canmodifyrequirementlevelsettings"
                },
                "MaxLength": 100,
                "FormatName": {
                    "Value": "Text"
                },
                "IsPrimaryName": True
            }
        ],
        "HasFeedback": False
    }
    
    try:
        print("📋 Creando tabla cr321_whatsappaccounts en Dataverse...")
        response = requests.post(url, headers=headers, json=table_definition)
        
        if response.status_code in [200, 201, 204]:
            print("✅ Tabla cr321_whatsappaccounts creada exitosamente")
            entity_id = response.headers.get("OData-EntityId", "")
            print(f"   ID de la entidad: {entity_id}")
            
            # Ahora crear los atributos adicionales
            print("\n📋 Creando atributos adicionales...")
            create_additional_attributes(entity_id, token)
            
            return True
        else:
            print(f"❌ Error al crear tabla: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Excepción al crear tabla: {e}")
        return False


def create_additional_attributes(entity_id, token):
    """Crea los atributos adicionales de la tabla"""
    
    # Extraer el nombre de la entidad del entity_id
    entity_name = "cr321_whatsappaccounts"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0"
    }
    
    # Lista de atributos a crear
    attributes = [
        {
            "@odata.type": "Microsoft.Dynamics.CRM.StringAttributeMetadata",
            "SchemaName": "cr321_phonenumberid",
            "DisplayName": {"Label": "Phone Number ID"},
            "Description": {"Label": "ID del número de teléfono de Meta"},
            "RequiredLevel": {"Value": "ApplicationRequired"},
            "MaxLength": 50,
            "FormatName": {"Value": "Text"}
        },
        {
            "@odata.type": "Microsoft.Dynamics.CRM.StringAttributeMetadata",
            "SchemaName": "cr321_accesstoken",
            "DisplayName": {"Label": "Access Token"},
            "Description": {"Label": "Token de acceso permanente de Meta"},
            "RequiredLevel": {"Value": "ApplicationRequired"},
            "MaxLength": 500,
            "FormatName": {"Value": "Text"}
        },
        {
            "@odata.type": "Microsoft.Dynamics.CRM.StringAttributeMetadata",
            "SchemaName": "cr321_businessaccountid",
            "DisplayName": {"Label": "Business Account ID"},
            "Description": {"Label": "ID de la cuenta de negocio de Meta"},
            "RequiredLevel": {"Value": "None"},
            "MaxLength": 50,
            "FormatName": {"Value": "Text"}
        },
        {
            "@odata.type": "Microsoft.Dynamics.CRM.StringAttributeMetadata",
            "SchemaName": "cr321_phonenumber",
            "DisplayName": {"Label": "Número de Teléfono"},
            "Description": {"Label": "Número de teléfono en formato internacional"},
            "RequiredLevel": {"Value": "None"},
            "MaxLength": 20,
            "FormatName": {"Value": "Text"}
        },
        {
            "@odata.type": "Microsoft.Dynamics.CRM.StringAttributeMetadata",
            "SchemaName": "cr321_displayname",
            "DisplayName": {"Label": "Nombre para Mostrar"},
            "Description": {"Label": "Nombre que aparece en WhatsApp Business"},
            "RequiredLevel": {"Value": "None"},
            "MaxLength": 100,
            "FormatName": {"Value": "Text"}
        },
        {
            "@odata.type": "Microsoft.Dynamics.CRM.BooleanAttributeMetadata",
            "SchemaName": "cr321_active",
            "DisplayName": {"Label": "Activa"},
            "Description": {"Label": "Indica si la cuenta está activa"},
            "RequiredLevel": {"Value": "None"},
            "DefaultValue": True,
            "OptionSet": {
                "@odata.type": "Microsoft.Dynamics.CRM.BooleanOptionSetMetadata",
                "TrueOption": {
                    "Value": 1,
                    "Label": {"Label": "Sí"}
                },
                "FalseOption": {
                    "Value": 0,
                    "Label": {"Label": "No"}
                }
            }
        },
        {
            "@odata.type": "Microsoft.Dynamics.CRM.BooleanAttributeMetadata",
            "SchemaName": "cr321_verified",
            "DisplayName": {"Label": "Verificada"},
            "Description": {"Label": "Indica si la cuenta está verificada por Meta"},
            "RequiredLevel": {"Value": "None"},
            "DefaultValue": False,
            "OptionSet": {
                "@odata.type": "Microsoft.Dynamics.CRM.BooleanOptionSetMetadata",
                "TrueOption": {
                    "Value": 1,
                    "Label": {"Label": "Sí"}
                },
                "FalseOption": {
                    "Value": 0,
                    "Label": {"Label": "No"}
                }
            }
        },
        {
            "@odata.type": "Microsoft.Dynamics.CRM.StringAttributeMetadata",
            "SchemaName": "cr321_webhookurl",
            "DisplayName": {"Label": "Webhook URL"},
            "Description": {"Label": "URL del webhook configurado"},
            "RequiredLevel": {"Value": "None"},
            "MaxLength": 500,
            "FormatName": {"Value": "Url"}
        },
        {
            "@odata.type": "Microsoft.Dynamics.CRM.StringAttributeMetadata",
            "SchemaName": "cr321_verifytoken",
            "DisplayName": {"Label": "Verify Token"},
            "Description": {"Label": "Token de verificación del webhook"},
            "RequiredLevel": {"Value": "None"},
            "MaxLength": 100,
            "FormatName": {"Value": "Text"}
        }
    ]
    
    # Crear cada atributo
    for attr in attributes:
        url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions(LogicalName='{entity_name}')/Attributes"
        
        # Formatear correctamente las etiquetas
        attr["DisplayName"] = {
            "@odata.type": "Microsoft.Dynamics.CRM.Label",
            "LocalizedLabels": [
                {
                    "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                    "Label": attr["DisplayName"]["Label"],
                    "LanguageCode": 1033
                }
            ]
        }
        
        attr["Description"] = {
            "@odata.type": "Microsoft.Dynamics.CRM.Label",
            "LocalizedLabels": [
                {
                    "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                    "Label": attr["Description"]["Label"],
                    "LanguageCode": 1033
                }
            ]
        }
        
        # Formatear RequiredLevel
        attr["RequiredLevel"] = {
            "Value": attr["RequiredLevel"]["Value"],
            "CanBeChanged": True,
            "ManagedPropertyLogicalName": "canmodifyrequirementlevelsettings"
        }
        
        # Para atributos Boolean, formatear las opciones
        if attr["@odata.type"] == "Microsoft.Dynamics.CRM.BooleanAttributeMetadata":
            attr["OptionSet"]["TrueOption"]["Label"] = {
                "@odata.type": "Microsoft.Dynamics.CRM.Label",
                "LocalizedLabels": [
                    {
                        "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                        "Label": attr["OptionSet"]["TrueOption"]["Label"]["Label"],
                        "LanguageCode": 1033
                    }
                ]
            }
            attr["OptionSet"]["FalseOption"]["Label"] = {
                "@odata.type": "Microsoft.Dynamics.CRM.Label",
                "LocalizedLabels": [
                    {
                        "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                        "Label": attr["OptionSet"]["FalseOption"]["Label"]["Label"],
                        "LanguageCode": 1033
                    }
                ]
            }
        
        try:
            response = requests.post(url, headers=headers, json=attr)
            
            if response.status_code in [200, 201, 204]:
                print(f"   ✅ Atributo {attr['SchemaName']} creado")
            else:
                print(f"   ❌ Error al crear {attr['SchemaName']}: {response.status_code}")
                print(f"      {response.text}")
                
        except Exception as e:
            print(f"   ❌ Excepción al crear {attr['SchemaName']}: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("CREACIÓN DE TABLA cr321_whatsappaccounts EN DATAVERSE")
    print("=" * 60)
    
    success = create_whatsapp_accounts_table()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ TABLA CREADA EXITOSAMENTE")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ ERROR AL CREAR LA TABLA")
        print("=" * 60)
