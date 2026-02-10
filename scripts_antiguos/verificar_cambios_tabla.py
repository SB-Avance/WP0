"""
Script para verificar cambios en la tabla cr321_adatawp0
- Campo cr321_grupoid (Lookup hacia cr321_grup)
- Campo cr321_idcontacto eliminado
- Campo cr321_contactorelacion (Lookup hacia cr321_contacto)
"""

import requests
import os
from dotenv import load_dotenv
from msal import ConfidentialClientApplication

# Cargar configuración
env_path = os.path.join(os.path.dirname(__file__), 'backend', '.env')
load_dotenv(env_path)

DATAVERSE_URL = os.getenv("DATAVERSE_URL")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")

def get_access_token():
    """Obtener token de acceso"""
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
        raise Exception(f"Error: {result.get('error_description', 'Unknown')}")

def verificar_campos_tabla():
    """Verificar campos de cr321_adatawp0"""
    token = get_access_token()
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json',
        'OData-MaxVersion': '4.0',
        'OData-Version': '4.0'
    }
    
    # Obtener metadatos de la tabla
    url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions(LogicalName='cr321_adatawp0')/Attributes"
    params = {
        "$select": "LogicalName,AttributeType,DisplayName",
        "$filter": "LogicalName eq 'cr321_grupoid' or LogicalName eq 'cr321_grupo' or LogicalName eq 'cr321_idcontacto' or LogicalName eq 'cr321_contactorelacion'"
    }
    
    response = requests.get(url, headers=headers, params=params, timeout=15)
    
    if response.status_code == 200:
        campos = response.json().get("value", [])
        return campos
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text[:300])
        return []

def buscar_lookups_en_tabla():
    """Buscar todos los campos Lookup en cr321_adatawp0"""
    token = get_access_token()
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json',
        'OData-MaxVersion': '4.0',
        'OData-Version': '4.0'
    }
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions(LogicalName='cr321_adatawp0')/Attributes/Microsoft.Dynamics.CRM.LookupAttributeMetadata"
    params = {
        "$select": "LogicalName,DisplayName"
    }
    
    response = requests.get(url, headers=headers, params=params, timeout=15)
    
    if response.status_code == 200:
        lookups = response.json().get("value", [])
        return lookups
    else:
        return []

print("=" * 70)
print("VERIFICACIÓN DE CAMBIOS EN cr321_adatawp0 (WhatsApp Chats)")
print("=" * 70)

# 1. Verificar campos específicos
print("\n📋 1. Verificando campos específicos...")
campos = verificar_campos_tabla()

campos_encontrados = {c['LogicalName']: c for c in campos}

print("\n📊 Resultados:")
print("-" * 70)

# cr321_grupo (Integer - debería estar si no se migró)
if 'cr321_grupo' in campos_encontrados:
    campo = campos_encontrados['cr321_grupo']
    tipo = campo.get('AttributeType')
    print(f"⚠️  cr321_grupo: {tipo} (debería cambiarse a Lookup)")
else:
    print(f"✅ cr321_grupo: NO EXISTE (migrado)")

# cr321_grupoid (Lookup - nuevo)
if 'cr321_grupoid' in campos_encontrados:
    campo = campos_encontrados['cr321_grupoid']
    tipo = campo.get('AttributeType')
    print(f"✅ cr321_grupoid: {tipo} (NUEVO - Lookup hacia grupos)")
else:
    print(f"❌ cr321_grupoid: NO EXISTE (pendiente crear)")

# cr321_idcontacto (Integer - obsoleto)
if 'cr321_idcontacto' in campos_encontrados:
    campo = campos_encontrados['cr321_idcontacto']
    tipo = campo.get('AttributeType')
    print(f"⚠️  cr321_idcontacto: {tipo} (OBSOLETO - eliminar)")
else:
    print(f"✅ cr321_idcontacto: NO EXISTE (eliminado correctamente)")

# cr321_contactorelacion (Lookup - nuevo)
if 'cr321_contactorelacion' in campos_encontrados:
    campo = campos_encontrados['cr321_contactorelacion']
    tipo = campo.get('AttributeType')
    print(f"✅ cr321_contactorelacion: {tipo} (ACTIVO - Lookup contactos)")
else:
    print(f"❌ cr321_contactorelacion: NO EXISTE (error crítico)")

# 2. Listar todos los Lookups
print("\n\n🔍 2. Todos los campos Lookup en cr321_adatawp0:")
print("-" * 70)
lookups = buscar_lookups_en_tabla()

if lookups:
    for lookup in lookups:
        nombre = lookup.get('LogicalName')
        display = lookup.get('DisplayName', {}).get('UserLocalizedLabel', {})
        display_name = display.get('Label', 'Sin nombre') if display else 'Sin nombre'
        print(f"   🔗 {nombre} - {display_name}")
else:
    print("   ❌ No se encontraron campos Lookup")

# 3. Resumen
print("\n\n" + "=" * 70)
print("📊 RESUMEN DE CAMBIOS")
print("=" * 70)

cambios_completados = 0
cambios_pendientes = 0

if 'cr321_grupoid' in campos_encontrados:
    print("✅ Campo cr321_grupoid (Lookup grupos) CREADO")
    cambios_completados += 1
else:
    print("❌ Campo cr321_grupoid (Lookup grupos) PENDIENTE")
    cambios_pendientes += 1

if 'cr321_idcontacto' not in campos_encontrados:
    print("✅ Campo cr321_idcontacto (obsoleto) ELIMINADO")
    cambios_completados += 1
else:
    print("⚠️  Campo cr321_idcontacto (obsoleto) AÚN EXISTE")
    cambios_pendientes += 1

if 'cr321_contactorelacion' in campos_encontrados:
    print("✅ Campo cr321_contactorelacion (Lookup contactos) ACTIVO")
    cambios_completados += 1
    
if 'cr321_grupo' not in campos_encontrados:
    print("✅ Campo cr321_grupo (Integer) ELIMINADO")
elif 'cr321_grupoid' not in campos_encontrados:
    print("⚠️  Campo cr321_grupo (Integer) aún existe - pendiente migrar")

print("\n" + "=" * 70)
print(f"Total completado: {cambios_completados}")
print(f"Total pendiente: {cambios_pendientes}")
print("=" * 70)
