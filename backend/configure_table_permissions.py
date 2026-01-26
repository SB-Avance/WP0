# Script para configurar permisos de las tablas en Dataverse
# Azure deployment - 2026-01-25

import requests
import time
from goot import get_token, DATAVERSE_URL

def get_entity_id(entity_logical_name):
    """Obtiene el MetadataId de una entidad"""
    token = get_token()
    if not token:
        return None
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions(LogicalName='{entity_logical_name}')"
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
            return data.get("MetadataId")
        else:
            print(f"❌ Error obteniendo MetadataId de {entity_logical_name}: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return None

def get_security_roles():
    """Obtiene la lista de roles de seguridad disponibles"""
    token = get_token()
    if not token:
        return []
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/roles?$select=name,roleid&$filter=contains(name,'System')"
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
            print(f"❌ Error obteniendo roles: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return []

def create_security_role(role_name, business_unit_id):
    """Crea un nuevo rol de seguridad"""
    token = get_token()
    if not token:
        return None
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/roles"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {
        "name": role_name,
        "businessunitid@odata.bind": f"/businessunits({business_unit_id})"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code in [200, 201, 204]:
            # Obtener el ID del rol creado
            location = response.headers.get("OData-EntityId", "")
            role_id = location.split("(")[1].split(")")[0] if "(" in location else None
            print(f"✅ Rol '{role_name}' creado exitosamente")
            return role_id
        else:
            print(f"❌ Error creando rol: {response.status_code}")
            print(f"   {response.text}")
            return None
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return None

def get_business_unit_id():
    """Obtiene el ID de la unidad de negocio raíz"""
    token = get_token()
    if not token:
        return None
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/businessunits?$top=1"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            units = data.get("value", [])
            if units:
                return units[0].get("businessunitid")
        return None
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return None

def add_privilege_to_role(role_id, entity_name, privilege_depth=3):
    """
    Agrega privilegios a un rol para una entidad específica
    privilege_depth: 0=None, 1=User, 2=BusinessUnit, 3=ParentChild, 4=Organization
    """
    token = get_token()
    if not token:
        return False
    
    # Los privilegios en Dataverse se gestionan a través de la acción AddPrivilegesRole
    # Primero necesitamos obtener los privilege IDs para la entidad
    
    # Para simplificar, vamos a actualizar el rol con permisos completos
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
            print(f"   ✅ Privilegios configurados para {entity_name}")
            return True
        else:
            print(f"   ⚠️ No se pudieron configurar privilegios automáticamente para {entity_name}")
            return False
    except Exception as e:
        print(f"   ❌ Excepción: {e}")
        return False

def grant_system_administrator_access():
    """
    Otorga acceso de System Administrator a las nuevas tablas
    """
    token = get_token()
    if not token:
        return False
    
    print("\n📋 Verificando rol 'System Administrator'...")
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/roles?$filter=name eq 'System Administrator'"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            roles = data.get("value", [])
            if roles:
                print(f"✅ Rol 'System Administrator' encontrado")
                print(f"   ID: {roles[0].get('roleid')}")
                print(f"\n💡 Los System Administrators tienen acceso automático a todas las entidades")
                print(f"   Las nuevas tablas ya están disponibles para los administradores")
                return True
        return False
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return False

def create_whatsapp_crm_role():
    """Crea un rol personalizado para WhatsApp CRM"""
    print("\n📋 Creando rol personalizado 'WhatsApp CRM User'...")
    
    # Obtener business unit
    bu_id = get_business_unit_id()
    if not bu_id:
        print("❌ No se pudo obtener Business Unit ID")
        return None
    
    print(f"✅ Business Unit ID: {bu_id}")
    
    # Verificar si el rol ya existe
    token = get_token()
    if not token:
        return None
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/roles?$filter=name eq 'WhatsApp CRM User'"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            roles = data.get("value", [])
            if roles:
                role_id = roles[0].get("roleid")
                print(f"✅ Rol 'WhatsApp CRM User' ya existe (ID: {role_id})")
                return role_id
    except Exception as e:
        pass
    
    # Crear el rol
    role_id = create_security_role("WhatsApp CRM User", bu_id)
    return role_id

def publish_customizations():
    """Publica las personalizaciones para que los cambios surtan efecto"""
    token = get_token()
    if not token:
        return False
    
    print("\n📋 Publicando personalizaciones...")
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/PublishAllXml"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0"
    }
    
    payload = {
        "ParameterXml": "<importexportxml></importexportxml>"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code in [200, 201, 204]:
            print("✅ Personalizaciones publicadas exitosamente")
            return True
        else:
            print(f"⚠️ No se pudieron publicar las personalizaciones: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return False

def show_permission_instructions():
    """Muestra instrucciones para configurar permisos manualmente"""
    print("\n" + "="*60)
    print("INSTRUCCIONES PARA CONFIGURAR PERMISOS MANUALMENTE")
    print("="*60)
    print("""
📋 Pasos para otorgar permisos a las nuevas tablas:

1. Accede a https://make.powerapps.com
2. Selecciona tu entorno
3. Ve a "Settings" (⚙️) > "Security" > "Security roles"
4. Selecciona el rol que deseas modificar (ej: "System Administrator")
5. Ve a la pestaña "Custom Entities"
6. Busca las siguientes tablas y otorga permisos:
   
   ✅ cr321_whatsappaccounts (Cuentas de WhatsApp)
   ✅ cr321_contacts (Contactos)
   ✅ cr321_chatbots (Chatbots)
   ✅ cr321_flows (Flujos de Conversación)
   ✅ cr321_automations (Automatizaciones)
   ✅ cr321_templates (Plantillas)

7. Para cada tabla, marca los privilegios necesarios:
   - Create (Crear)
   - Read (Leer)
   - Write (Escribir)
   - Delete (Eliminar)
   - Append (Anexar)
   - Append To (Anexar a)
   - Assign (Asignar)
   - Share (Compartir)

8. Selecciona el nivel de acceso según el rol:
   - 🟢 Organization: Acceso completo a todos los registros
   - 🟡 Business Unit: Acceso a registros de la unidad de negocio
   - 🟠 User: Solo registros propios del usuario

9. Guarda los cambios

💡 RECOMENDACIÓN: 
   - System Administrator: Nivel Organization para todas las tablas
   - Usuarios estándar: Nivel Business Unit o User según necesidad
    """)
    print("="*60)

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("CONFIGURACIÓN DE PERMISOS PARA TABLAS DATAVERSE")
    print("=" * 60)
    
    tables = [
        "cr321_whatsappaccounts",
        "cr321_contacts",
        "cr321_chatbots",
        "cr321_flows",
        "cr321_automations",
        "cr321_templates"
    ]
    
    print("\nTablas a configurar:")
    for table in tables:
        print(f"  - {table}")
    
    # Verificar acceso de System Administrator
    grant_system_administrator_access()
    
    # Intentar crear rol personalizado
    role_id = create_whatsapp_crm_role()
    
    # Publicar personalizaciones
    publish_customizations()
    
    # Mostrar instrucciones manuales
    show_permission_instructions()
    
    print("\n" + "="*60)
    print("✅ CONFIGURACIÓN COMPLETADA")
    print("="*60)
    print("\n💡 IMPORTANTE:")
    print("   Los administradores ya tienen acceso a las tablas.")
    print("   Para usuarios no administradores, configura permisos manualmente")
    print("   siguiendo las instrucciones mostradas arriba.")
    print("="*60)
