# Script para verificar tablas y permisos en Dataverse
# Azure deployment - 2026-01-25

import requests
from goot import get_token, DATAVERSE_URL

def list_custom_tables():
    """Lista todas las tablas personalizadas (cr321_*)"""
    token = get_token()
    if not token:
        return []
    
    # Lista predefinida de tablas que creamos
    table_names = [
        "cr321_whatsappaccounts",
        "cr321_contacts",
        "cr321_chatbots",
        "cr321_flows",
        "cr321_automations",
        "cr321_templates",
        "cr321_adatawp0s",
        "cr321_usuarioses"
    ]
    
    tables = []
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0"
    }
    
    for table_name in table_names:
        url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions(LogicalName='{table_name}')?$select=SchemaName,LogicalName,DisplayName,MetadataId"
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                tables.append(data)
            elif response.status_code == 404:
                # Tabla no existe, continuar
                pass
            else:
                print(f"⚠️ Error obteniendo {table_name}: {response.status_code}")
        except Exception as e:
            print(f"⚠️ Excepción con {table_name}: {e}")
    
    return tables

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

def get_security_roles_with_privileges(entity_logical_name):
    """Obtiene los roles de seguridad y sus privilegios para una entidad"""
    token = get_token()
    if not token:
        return []
    
    # Primero obtener todos los roles
    url = f"{DATAVERSE_URL}/api/data/v9.2/roles?$select=name,roleid,businessunitid"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
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

def check_role_privileges(role_id, entity_name):
    """Verifica los privilegios de un rol para una entidad específica"""
    token = get_token()
    if not token:
        return None
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/roles({role_id})/Microsoft.Dynamics.CRM.RetrieveRolePrivilegesRole"
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
            return None
    except Exception as e:
        return None

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

def main():
    print("=" * 80)
    print("VERIFICACIÓN DE TABLAS Y PERMISOS EN DATAVERSE")
    print("=" * 80)
    
    # Listar tablas personalizadas
    print("\n📋 Obteniendo tablas personalizadas (cr321_*)...\n")
    tables = list_custom_tables()
    
    if not tables:
        print("❌ No se encontraron tablas personalizadas o error al obtener datos")
        return
    
    print(f"✅ Se encontraron {len(tables)} tablas personalizadas\n")
    
    # Mostrar información de cada tabla
    for idx, table in enumerate(tables, 1):
        schema_name = table.get("SchemaName", "")
        logical_name = table.get("LogicalName", "")
        display_name = format_display_name(table.get("DisplayName"))
        metadata_id = table.get("MetadataId", "")
        
        print("─" * 80)
        print(f"📊 TABLA {idx}: {schema_name}")
        print("─" * 80)
        print(f"   Nombre Lógico:    {logical_name}")
        print(f"   Nombre Display:   {display_name}")
        print(f"   Metadata ID:      {metadata_id}")
        
        # Obtener atributos
        print(f"\n   📝 Atributos:")
        attributes = get_table_attributes(logical_name)
        
        if attributes:
            # Filtrar solo atributos personalizados (cr321_)
            custom_attrs = [a for a in attributes if a.get("LogicalName", "").startswith("cr321_")]
            
            for attr in custom_attrs:
                attr_name = attr.get("SchemaName", "")
                attr_type = attr.get("AttributeType", "")
                attr_display = format_display_name(attr.get("DisplayName"))
                required = attr.get("RequiredLevel", {})
                required_val = required.get("Value", "None") if isinstance(required, dict) else "None"
                
                required_icon = "🔴" if required_val == "ApplicationRequired" else "⚪"
                print(f"      {required_icon} {attr_name:<30} [{attr_type:<15}] - {attr_display}")
        else:
            print("      ⚠️ No se pudieron obtener los atributos")
        
        print()
    
    # Obtener roles de seguridad
    print("\n" + "=" * 80)
    print("🔐 ROLES DE SEGURIDAD DISPONIBLES")
    print("=" * 80)
    
    roles = get_security_roles_with_privileges("")
    
    if roles:
        print(f"\n✅ Se encontraron {len(roles)} roles de seguridad\n")
        
        # Filtrar roles relevantes
        important_roles = [r for r in roles if any(keyword in r.get("name", "").lower() 
                          for keyword in ["system", "administrator", "user", "whatsapp", "crm"])]
        
        for role in important_roles:
            role_name = role.get("name", "Sin nombre")
            role_id = role.get("roleid", "")
            bu_id = role.get("businessunitid", "")
            
            print(f"   🔑 {role_name}")
            print(f"      ID: {role_id}")
            print(f"      Business Unit: {bu_id}")
            print()
    else:
        print("⚠️ No se pudieron obtener los roles de seguridad")
    
    # Resumen
    print("\n" + "=" * 80)
    print("📊 RESUMEN")
    print("=" * 80)
    print(f"\n   Tablas personalizadas encontradas: {len(tables)}")
    print(f"   Roles de seguridad: {len(roles)}")
    print()
    
    print("💡 NOTAS:")
    print("   - Las tablas con prefijo 'cr321_' son personalizadas de este proyecto")
    print("   - Los System Administrators tienen acceso completo automáticamente")
    print("   - Para configurar permisos específicos, usa Power Apps Portal")
    print("   - URL: https://make.powerapps.com > Settings > Security > Security roles")
    print()
    
    print("=" * 80)
    print("✅ VERIFICACIÓN COMPLETADA")
    print("=" * 80)

if __name__ == "__main__":
    main()
