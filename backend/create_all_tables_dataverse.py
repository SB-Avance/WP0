# Script para crear todas las tablas del sistema WhatsApp CRM en Dataverse
# Azure deployment - 2026-01-25

import requests
import time
from goot import get_token, DATAVERSE_URL

def format_label(text, lang_code=1033):
    """Formatea una etiqueta para Dataverse"""
    return {
        "@odata.type": "Microsoft.Dynamics.CRM.Label",
        "LocalizedLabels": [
            {
                "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                "Label": text,
                "LanguageCode": lang_code
            }
        ]
    }

def format_required_level(value="None"):
    """Formatea el nivel de requerimiento"""
    return {
        "Value": value,
        "CanBeChanged": True,
        "ManagedPropertyLogicalName": "canmodifyrequirementlevelsettings"
    }

def create_entity(entity_name, display_name, description, primary_field_name):
    """Crea una entidad básica en Dataverse"""
    token = get_token()
    if not token:
        print("❌ No se pudo obtener token")
        return None
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0"
    }
    
    table_definition = {
        "@odata.type": "Microsoft.Dynamics.CRM.EntityMetadata",
        "SchemaName": entity_name,
        "DisplayName": format_label(display_name),
        "DisplayCollectionName": format_label(display_name),
        "Description": format_label(description),
        "OwnershipType": "UserOwned",
        "IsActivity": False,
        "HasNotes": False,
        "HasActivities": False,
        "PrimaryNameAttribute": primary_field_name,
        "Attributes": [
            {
                "@odata.type": "Microsoft.Dynamics.CRM.StringAttributeMetadata",
                "SchemaName": primary_field_name,
                "DisplayName": format_label("Nombre"),
                "RequiredLevel": format_required_level("ApplicationRequired"),
                "MaxLength": 200,
                "FormatName": {"Value": "Text"},
                "IsPrimaryName": True
            }
        ],
        "HasFeedback": False
    }
    
    try:
        print(f"📋 Creando tabla {entity_name}...")
        response = requests.post(url, headers=headers, json=table_definition)
        
        if response.status_code in [200, 201, 204]:
            print(f"✅ Tabla {entity_name} creada exitosamente")
            return entity_name
        else:
            print(f"❌ Error al crear {entity_name}: {response.status_code}")
            print(f"   {response.text}")
            return None
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return None

def create_string_attribute(entity_name, schema_name, display_name, max_length, required=False, description=""):
    """Crea un atributo de tipo String"""
    token = get_token()
    if not token:
        return False
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions(LogicalName='{entity_name}')/Attributes"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0"
    }
    
    attr = {
        "@odata.type": "Microsoft.Dynamics.CRM.StringAttributeMetadata",
        "SchemaName": schema_name,
        "DisplayName": format_label(display_name),
        "Description": format_label(description) if description else format_label(display_name),
        "RequiredLevel": format_required_level("ApplicationRequired" if required else "None"),
        "MaxLength": max_length,
        "FormatName": {"Value": "Text"}
    }
    
    try:
        response = requests.post(url, headers=headers, json=attr)
        if response.status_code in [200, 201, 204]:
            print(f"   ✅ {schema_name}")
            return True
        else:
            print(f"   ❌ {schema_name}: {response.status_code} - {response.text[:100]}")
            return False
    except Exception as e:
        print(f"   ❌ {schema_name}: {e}")
        return False

def create_memo_attribute(entity_name, schema_name, display_name, max_length=5000, description=""):
    """Crea un atributo de tipo Memo"""
    token = get_token()
    if not token:
        return False
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions(LogicalName='{entity_name}')/Attributes"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0"
    }
    
    attr = {
        "@odata.type": "Microsoft.Dynamics.CRM.MemoAttributeMetadata",
        "SchemaName": schema_name,
        "DisplayName": format_label(display_name),
        "Description": format_label(description) if description else format_label(display_name),
        "RequiredLevel": format_required_level("None"),
        "MaxLength": max_length,
        "Format": "Text"
    }
    
    try:
        response = requests.post(url, headers=headers, json=attr)
        if response.status_code in [200, 201, 204]:
            print(f"   ✅ {schema_name}")
            return True
        else:
            print(f"   ❌ {schema_name}: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ {schema_name}: {e}")
        return False

def create_boolean_attribute(entity_name, schema_name, display_name, default_value=False):
    """Crea un atributo de tipo Boolean"""
    token = get_token()
    if not token:
        return False
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions(LogicalName='{entity_name}')/Attributes"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0"
    }
    
    attr = {
        "@odata.type": "Microsoft.Dynamics.CRM.BooleanAttributeMetadata",
        "SchemaName": schema_name,
        "DisplayName": format_label(display_name),
        "RequiredLevel": format_required_level("None"),
        "DefaultValue": default_value,
        "OptionSet": {
            "@odata.type": "Microsoft.Dynamics.CRM.BooleanOptionSetMetadata",
            "TrueOption": {
                "Value": 1,
                "Label": format_label("Sí")
            },
            "FalseOption": {
                "Value": 0,
                "Label": format_label("No")
            }
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=attr)
        if response.status_code in [200, 201, 204]:
            print(f"   ✅ {schema_name}")
            return True
        else:
            print(f"   ❌ {schema_name}: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ {schema_name}: {e}")
        return False

def create_datetime_attribute(entity_name, schema_name, display_name):
    """Crea un atributo de tipo DateTime"""
    token = get_token()
    if not token:
        return False
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions(LogicalName='{entity_name}')/Attributes"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0"
    }
    
    attr = {
        "@odata.type": "Microsoft.Dynamics.CRM.DateTimeAttributeMetadata",
        "SchemaName": schema_name,
        "DisplayName": format_label(display_name),
        "RequiredLevel": format_required_level("None"),
        "Format": "DateAndTime",
        "DateTimeBehavior": {
            "Value": "UserLocal"
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=attr)
        if response.status_code in [200, 201, 204]:
            print(f"   ✅ {schema_name}")
            return True
        else:
            print(f"   ❌ {schema_name}: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ {schema_name}: {e}")
        return False

def create_integer_attribute(entity_name, schema_name, display_name, default_value=0):
    """Crea un atributo de tipo Integer"""
    token = get_token()
    if not token:
        return False
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions(LogicalName='{entity_name}')/Attributes"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0"
    }
    
    attr = {
        "@odata.type": "Microsoft.Dynamics.CRM.IntegerAttributeMetadata",
        "SchemaName": schema_name,
        "DisplayName": format_label(display_name),
        "RequiredLevel": format_required_level("None"),
        "Format": "None"
    }
    
    try:
        response = requests.post(url, headers=headers, json=attr)
        if response.status_code in [200, 201, 204]:
            print(f"   ✅ {schema_name}")
            return True
        else:
            print(f"   ❌ {schema_name}: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ {schema_name}: {e}")
        return False

def create_picklist_attribute(entity_name, schema_name, display_name, options, default_value=None):
    """Crea un atributo de tipo Picklist (OptionSet)"""
    token = get_token()
    if not token:
        return False
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions(LogicalName='{entity_name}')/Attributes"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0"
    }
    
    option_list = []
    for opt in options:
        option_list.append({
            "Value": opt["value"],
            "Label": format_label(opt["label"])
        })
    
    attr = {
        "@odata.type": "Microsoft.Dynamics.CRM.PicklistAttributeMetadata",
        "SchemaName": schema_name,
        "DisplayName": format_label(display_name),
        "RequiredLevel": format_required_level("None"),
        "OptionSet": {
            "@odata.type": "Microsoft.Dynamics.CRM.OptionSetMetadata",
            "IsGlobal": False,
            "OptionSetType": "Picklist",
            "Options": option_list
        }
    }
    
    if default_value is not None:
        attr["DefaultFormValue"] = default_value
    
    try:
        response = requests.post(url, headers=headers, json=attr)
        if response.status_code in [200, 201, 204]:
            print(f"   ✅ {schema_name}")
            return True
        else:
            print(f"   ❌ {schema_name}: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ {schema_name}: {e}")
        return False

# ============================================
# CREACIÓN DE TABLAS
# ============================================

def create_contacts_table():
    """Crea la tabla cr321_contacts"""
    print("\n" + "="*60)
    print("TABLA: cr321_contacts (Contactos)")
    print("="*60)
    
    if not create_entity("cr321_contacts", "Contactos", "Gestión de contactos y clientes de WhatsApp", "cr321_name"):
        return False
    
    time.sleep(2)
    
    print("\n📋 Creando atributos...")
    create_string_attribute("cr321_contacts", "cr321_contactid", "ID Numérico", 10, required=True, description="ID numérico secuencial")
    create_string_attribute("cr321_contacts", "cr321_phone", "Teléfono", 20, required=True, description="Número en formato internacional")
    create_string_attribute("cr321_contacts", "cr321_email", "Email", 100, description="Correo electrónico")
    create_string_attribute("cr321_contacts", "cr321_company", "Empresa", 200, description="Nombre de la empresa")
    create_string_attribute("cr321_contacts", "cr321_tags", "Etiquetas", 500, description="Etiquetas separadas por comas")
    create_memo_attribute("cr321_contacts", "cr321_notes", "Notas", 5000, "Notas adicionales")
    create_datetime_attribute("cr321_contacts", "cr321_lastcontact", "Último Contacto")
    create_datetime_attribute("cr321_contacts", "cr321_firstcontact", "Primer Contacto")
    create_picklist_attribute("cr321_contacts", "cr321_status", "Estado", [
        {"value": 462410000, "label": "Nuevo"},
        {"value": 462410001, "label": "Activo"},
        {"value": 462410002, "label": "Inactivo"},
        {"value": 462410003, "label": "Bloqueado"}
    ], 462410000)
    create_picklist_attribute("cr321_contacts", "cr321_source", "Origen", [
        {"value": 462410000, "label": "WhatsApp"},
        {"value": 462410001, "label": "Manual"},
        {"value": 462410002, "label": "Importación"},
        {"value": 462410003, "label": "Landing Page"}
    ])
    
    print("✅ Tabla cr321_contacts completada\n")
    return True

def create_chatbots_table():
    """Crea la tabla cr321_chatbots"""
    print("\n" + "="*60)
    print("TABLA: cr321_chatbots (Chatbots)")
    print("="*60)
    
    if not create_entity("cr321_chatbots", "Chatbots", "Gestión de chatbots de WhatsApp", "cr321_name"):
        return False
    
    time.sleep(2)
    
    print("\n📋 Creando atributos...")
    create_picklist_attribute("cr321_chatbots", "cr321_type", "Tipo de Bot", [
        {"value": 462410000, "label": "FlowBot"},
        {"value": 462410001, "label": "Simple"},
        {"value": 462410002, "label": "AI Assistant"}
    ], 462410000)
    create_memo_attribute("cr321_chatbots", "cr321_config", "Configuración", 100000, "Configuración en formato JSON")
    create_boolean_attribute("cr321_chatbots", "cr321_active", "Activo", True)
    
    print("✅ Tabla cr321_chatbots completada\n")
    return True

def create_flows_table():
    """Crea la tabla cr321_flows"""
    print("\n" + "="*60)
    print("TABLA: cr321_flows (Flujos de Conversación)")
    print("="*60)
    
    if not create_entity("cr321_flows", "Flujos de Conversación", "Definición de flujos para chatbots", "cr321_name"):
        return False
    
    time.sleep(2)
    
    print("\n📋 Creando atributos...")
    create_memo_attribute("cr321_flows", "cr321_nodes", "Nodos", 100000, "Definición de nodos en JSON")
    create_memo_attribute("cr321_flows", "cr321_edges", "Conexiones", 100000, "Conexiones entre nodos en JSON")
    create_integer_attribute("cr321_flows", "cr321_version", "Versión", 1)
    
    print("✅ Tabla cr321_flows completada\n")
    return True

def create_automations_table():
    """Crea la tabla cr321_automations"""
    print("\n" + "="*60)
    print("TABLA: cr321_automations (Automatizaciones)")
    print("="*60)
    
    if not create_entity("cr321_automations", "Automatizaciones", "Reglas de automatización", "cr321_name"):
        return False
    
    time.sleep(2)
    
    print("\n📋 Creando atributos...")
    create_picklist_attribute("cr321_automations", "cr321_trigger", "Disparador", [
        {"value": 462410000, "label": "Mensaje Recibido"},
        {"value": 462410001, "label": "Palabra Clave"},
        {"value": 462410002, "label": "Horario"},
        {"value": 462410003, "label": "Evento de Sistema"}
    ])
    create_memo_attribute("cr321_automations", "cr321_conditions", "Condiciones", 10000, "Condiciones en JSON")
    create_memo_attribute("cr321_automations", "cr321_actions", "Acciones", 10000, "Acciones en JSON")
    create_boolean_attribute("cr321_automations", "cr321_active", "Activa", True)
    
    print("✅ Tabla cr321_automations completada\n")
    return True

def create_templates_table():
    """Crea la tabla cr321_templates"""
    print("\n" + "="*60)
    print("TABLA: cr321_templates (Plantillas)")
    print("="*60)
    
    if not create_entity("cr321_templates", "Plantillas", "Plantillas de mensajes de WhatsApp", "cr321_name"):
        return False
    
    time.sleep(2)
    
    print("\n📋 Creando atributos...")
    create_memo_attribute("cr321_templates", "cr321_content", "Contenido", 5000, "Contenido de la plantilla")
    create_picklist_attribute("cr321_templates", "cr321_category", "Categoría", [
        {"value": 462410000, "label": "Marketing"},
        {"value": 462410001, "label": "Servicio"},
        {"value": 462410002, "label": "Ventas"},
        {"value": 462410003, "label": "Soporte"}
    ])
    create_string_attribute("cr321_templates", "cr321_language", "Idioma", 10, description="Código de idioma")
    create_boolean_attribute("cr321_templates", "cr321_approved", "Aprobada", False)
    
    print("✅ Tabla cr321_templates completada\n")
    return True

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("CREACIÓN DE TABLAS PARA WHATSAPP CRM EN DATAVERSE")
    print("=" * 60)
    print("\nTablas a crear:")
    print("1. cr321_contacts - Contactos")
    print("2. cr321_chatbots - Chatbots")
    print("3. cr321_flows - Flujos de Conversación")
    print("4. cr321_automations - Automatizaciones")
    print("5. cr321_templates - Plantillas")
    print("\n" + "=" * 60)
    
    results = {
        "cr321_contacts": create_contacts_table(),
        "cr321_chatbots": create_chatbots_table(),
        "cr321_flows": create_flows_table(),
        "cr321_automations": create_automations_table(),
        "cr321_templates": create_templates_table()
    }
    
    print("\n" + "=" * 60)
    print("RESUMEN DE CREACIÓN")
    print("=" * 60)
    
    for table, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {table}")
    
    total = sum(results.values())
    print(f"\n📊 Total: {total}/{len(results)} tablas creadas exitosamente")
    print("=" * 60)
