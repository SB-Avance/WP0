# Script para verificar la tabla de usuarios en Dataverse
# Azure deployment - 2026-01-25

import requests
from goot import get_token, DATAVERSE_URL

def format_display_name(display_name_obj):
    """Extrae el label del objeto DisplayName"""
    if not display_name_obj:
        return "Sin nombre"
    
    if isinstance(display_name_obj, dict):
        localized_labels = display_name_obj.get("LocalizedLabels", [])
        if localized_labels and len(localized_labels) > 0:
            return localized_labels[0].get("Label", "Sin nombre")
        
        user_localized_label = display_name_obj.get("UserLocalizedLabel")
        if user_localized_label:
            return user_localized_label.get("Label", "Sin nombre")
    
    return "Sin nombre"

def get_table_info(logical_name):
    """Obtiene información de una tabla específica"""
    token = get_token()
    if not token:
        return None
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions(LogicalName='{logical_name}')?$select=SchemaName,LogicalName,DisplayName,MetadataId"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error obteniendo tabla {logical_name}: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return None

def get_table_attributes(logical_name):
    """Obtiene los atributos de una tabla"""
    token = get_token()
    if not token:
        return []
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions(LogicalName='{logical_name}')/Attributes?$select=SchemaName,LogicalName,DisplayName,AttributeType,RequiredLevel"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get("value", [])
        else:
            return []
    except Exception as e:
        return []

def get_table_records_count(entity_name):
    """Obtiene el número de registros en una tabla"""
    token = get_token()
    if not token:
        return 0
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/{entity_name}?$count=true&$top=1"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get("@odata.count", 0)
        else:
            return 0
    except Exception as e:
        return 0

def main():
    print("=" * 80)
    print("VERIFICACIÓN DE TABLAS DE SISTEMA")
    print("=" * 80)
    
    # Tablas principales del sistema
    system_tables = [
        ("cr321_usuarioses", "Usuarios"),
        ("cr321_adatawp0s", "Mensajes WhatsApp"),
        ("cr321_whatsappaccounts", "Cuentas de WhatsApp"),
        ("cr321_contacts", "Contactos"),
        ("cr321_chatbots", "Chatbots"),
        ("cr321_flows", "Flujos"),
        ("cr321_automations", "Automatizaciones"),
        ("cr321_templates", "Plantillas")
    ]
    
    print(f"\n📋 Verificando {len(system_tables)} tablas del sistema...\n")
    
    found_tables = []
    missing_tables = []
    
    for table_name, friendly_name in system_tables:
        print(f"Verificando {table_name}...")
        table_info = get_table_info(table_name)
        
        if table_info:
            found_tables.append((table_name, table_info, friendly_name))
            print(f"  ✅ Encontrada")
        else:
            missing_tables.append((table_name, friendly_name))
            print(f"  ❌ No encontrada")
    
    # Mostrar tablas encontradas con detalle
    print("\n" + "=" * 80)
    print(f"📊 TABLAS ENCONTRADAS ({len(found_tables)})")
    print("=" * 80)
    
    for idx, (logical_name, table_info, friendly_name) in enumerate(found_tables, 1):
        schema_name = table_info.get("SchemaName", "")
        display_name = format_display_name(table_info.get("DisplayName"))
        metadata_id = table_info.get("MetadataId", "")
        
        print(f"\n{'─' * 80}")
        print(f"📊 TABLA {idx}: {schema_name}")
        print(f"{'─' * 80}")
        print(f"   Nombre Lógico:    {logical_name}")
        print(f"   Nombre Display:   {display_name}")
        print(f"   Metadata ID:      {metadata_id}")
        
        # Contar registros
        count = get_table_records_count(logical_name)
        print(f"   Registros:        {count}")
        
        # Obtener atributos
        print(f"\n   📝 Atributos personalizados:")
        attributes = get_table_attributes(logical_name)
        
        if attributes:
            custom_attrs = [a for a in attributes if a.get("LogicalName", "").startswith("cr321_")]
            
            for attr in custom_attrs:
                attr_name = attr.get("SchemaName", "")
                attr_type = attr.get("AttributeType", "")
                attr_display = format_display_name(attr.get("DisplayName"))
                required = attr.get("RequiredLevel", {})
                required_val = required.get("Value", "None") if isinstance(required, dict) else "None"
                
                required_icon = "🔴" if required_val == "ApplicationRequired" else "⚪"
                print(f"      {required_icon} {attr_name:<30} [{attr_type:<15}] - {attr_display}")
    
    # Mostrar tablas faltantes
    if missing_tables:
        print("\n" + "=" * 80)
        print(f"⚠️  TABLAS NO ENCONTRADAS ({len(missing_tables)})")
        print("=" * 80)
        
        for table_name, friendly_name in missing_tables:
            print(f"   ❌ {table_name} ({friendly_name})")
    
    # Resumen
    print("\n" + "=" * 80)
    print("📊 RESUMEN")
    print("=" * 80)
    print(f"\n   ✅ Tablas encontradas: {len(found_tables)}")
    print(f"   ❌ Tablas faltantes:   {len(missing_tables)}")
    print(f"   📊 Total verificadas:  {len(system_tables)}")
    print()
    
    print("=" * 80)

if __name__ == "__main__":
    main()
