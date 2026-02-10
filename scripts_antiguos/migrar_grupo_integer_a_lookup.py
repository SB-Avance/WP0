"""
Script para migrar datos de cr321_grupo (Integer) a cr321_grupoid (Lookup)
---------------------------------------------------------------------------
Migra mensajes que tienen cr321_grupo (1, 2, 3...) al nuevo campo 
cr321_grupoid que es un Lookup hacia la tabla cr321_grup.

Mapeo:
- cr321_grupo = 1 → cr321_grup donde cr321_idgrupo = 1
- cr321_grupo = 2 → cr321_grup donde cr321_idgrupo = 2
- etc.
"""

import requests
import os
from dotenv import load_dotenv
from msal import ConfidentialClientApplication
from collections import defaultdict

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


def get_headers():
    """Obtener headers con autenticación"""
    token = get_access_token()
    return {
        'Authorization': f'Bearer {token}',
        'OData-MaxVersion': '4.0',
        'OData-Version': '4.0',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }


def obtener_grupos():
    """Obtener todos los grupos con su cr321_idgrupo y GUID"""
    headers = get_headers()
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_grups"
    params = {
        "$select": "cr321_grupoid,cr321_idgrupo,cr321_nombre",
        "$orderby": "cr321_idgrupo asc"
    }
    
    response = requests.get(url, params=params, headers=headers, timeout=15)
    
    if response.status_code == 200:
        grupos = response.json().get("value", [])
        # Crear mapa: idgrupo (int) → GUID
        mapa = {}
        for g in grupos:
            id_int = g.get('cr321_idgrupo')
            guid = g.get('cr321_grupoid')
            nombre = g.get('cr321_nombre')
            if id_int is not None and guid:
                mapa[id_int] = {'guid': guid, 'nombre': nombre}
        return mapa
    else:
        print(f"❌ Error al obtener grupos: {response.status_code}")
        return {}


def obtener_mensajes_con_grupo_integer():
    """Obtener mensajes que tienen cr321_grupo (Integer) pero no cr321_grupoid (Lookup)"""
    headers = get_headers()
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s"
    params = {
        "$select": "cr321_adatawp0id,cr321_grupo,cr321_phone,cr321_fromname",
        "$filter": "cr321_grupo ne null and _cr321_grupoid_value eq null",
        "$orderby": "cr321_timestamp desc"
    }
    
    response = requests.get(url, params=params, headers=headers, timeout=15)
    
    if response.status_code == 200:
        mensajes = response.json().get("value", [])
        return mensajes
    else:
        print(f"❌ Error al obtener mensajes: {response.status_code}")
        return []


def migrar_mensaje(mensaje_id, grupo_guid):
    """Migrar un mensaje: asignar cr321_grupoid basado en cr321_grupo"""
    headers = get_headers()
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s({mensaje_id})"
    
    payload = {
        "cr321_grupoid@odata.bind": f"/cr321_grups({grupo_guid})"
    }
    
    response = requests.patch(url, json=payload, headers=headers, timeout=10)
    return response.status_code == 204


print("=" * 80)
print("MIGRACIÓN: cr321_grupo (Integer) → cr321_grupoid (Lookup)")
print("=" * 80)

# 1. Obtener mapa de grupos
print("\n📂 1. Obteniendo grupos...")
mapa_grupos = obtener_grupos()

if not mapa_grupos:
    print("❌ No se encontraron grupos. No se puede continuar.")
    exit(1)

print(f"   ✅ {len(mapa_grupos)} grupos encontrados:")
for id_int, info in sorted(mapa_grupos.items()):
    print(f"      {id_int} → {info['nombre']} ({info['guid']})")

# 2. Obtener mensajes pendientes de migración
print("\n📱 2. Buscando mensajes pendientes de migración...")
mensajes = obtener_mensajes_con_grupo_integer()

if not mensajes:
    print("   ✅ No hay mensajes pendientes de migración.")
    print("   Todos los mensajes ya tienen cr321_grupoid asignado o no tienen grupo.")
    exit(0)

print(f"   📊 {len(mensajes)} mensajes encontrados con cr321_grupo (Integer)")

# Agrupar por valor de cr321_grupo
agrupados = defaultdict(list)
for msg in mensajes:
    grupo_int = msg.get('cr321_grupo')
    agrupados[grupo_int].append(msg)

print("\n   📊 Distribución:")
for grupo_int in sorted(agrupados.keys()):
    count = len(agrupados[grupo_int])
    nombre = mapa_grupos.get(grupo_int, {}).get('nombre', 'DESCONOCIDO')
    print(f"      cr321_grupo = {grupo_int} ({nombre}): {count} mensajes")

# 3. Confirmar migración
print("\n" + "=" * 80)
respuesta = input("¿Deseas continuar con la migración? (s/n): ")

if respuesta.lower() != 's':
    print("❌ Migración cancelada")
    exit(0)

# 4. Ejecutar migración
print("\n🔄 3. Migrando mensajes...")
print("-" * 80)

migrados = 0
errores = 0
sin_grupo = 0

for i, mensaje in enumerate(mensajes, 1):
    mensaje_id = mensaje['cr321_adatawp0id']
    grupo_int = mensaje.get('cr321_grupo')
    telefono = mensaje.get('cr321_phone', 'N/A')
    nombre = mensaje.get('cr321_fromname', 'N/A')
    
    # Verificar si el grupo existe en el mapa
    if grupo_int not in mapa_grupos:
        print(f"   ⚠️  Mensaje {i}/{len(mensajes)}: Grupo {grupo_int} no existe en cr321_grup")
        sin_grupo += 1
        continue
    
    grupo_guid = mapa_grupos[grupo_int]['guid']
    grupo_nombre = mapa_grupos[grupo_int]['nombre']
    
    # Migrar
    if migrar_mensaje(mensaje_id, grupo_guid):
        print(f"   ✅ {i}/{len(mensajes)}: {nombre[:20]:20} → Grupo {grupo_int} ({grupo_nombre})")
        migrados += 1
    else:
        print(f"   ❌ {i}/{len(mensajes)}: Error al migrar mensaje de {nombre}")
        errores += 1
    
    # Progress cada 10 mensajes
    if i % 10 == 0:
        print(f"   📊 Progreso: {i}/{len(mensajes)} procesados...")

# 5. Resumen
print("\n" + "=" * 80)
print("📊 RESUMEN DE MIGRACIÓN")
print("=" * 80)
print(f"✅ Migrados exitosamente: {migrados}")
print(f"⚠️  Sin grupo correspondiente: {sin_grupo}")
print(f"❌ Errores: {errores}")
print(f"📝 Total procesados: {len(mensajes)}")
print("=" * 80)

if migrados > 0:
    print("\n✅ Migración completada con éxito")
    print("   Los mensajes ahora tienen cr321_grupoid (Lookup) asignado")
    print("   El campo cr321_grupo (Integer) puede eliminarse cuando estés seguro")
else:
    print("\n⚠️  No se migraron mensajes")
