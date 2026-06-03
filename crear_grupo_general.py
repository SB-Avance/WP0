"""
Script para crear grupo General en Dataverse
"""

import requests
from msal import ConfidentialClientApplication

CLIENT_ID = "d05fd904-f1fb-4fe3-89e9-1779d914c828"
CLIENT_SECRET = "QYG8Q~J38KfJGUSIy-O2h-o_9pRTNuTNC7909aWg"
TENANT_ID = "41ddee82-dfb3-4c4a-bbe6-de9c741c754e"
DATAVERSE_URL = "https://org460b8a6c.crm2.dynamics.com"


def get_token():
    authority = f"https://login.microsoftonline.com/{TENANT_ID}"
    scope = [f"{DATAVERSE_URL}/.default"]
    app = ConfidentialClientApplication(
        CLIENT_ID, authority=authority, client_credential=CLIENT_SECRET
    )
    result = app.acquire_token_for_client(scopes=scope)
    return result["access_token"]


print("=" * 70)
print("CREAR GRUPO GENERAL EN DATAVERSE")
print("=" * 70)

token = get_token()
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}

# 1. Verificar estructura de tabla cr321_grup
print("\n1. Verificando estructura de cr321_grup...")
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_grups?$top=1"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    grupos = response.json().get("value", [])
    if grupos:
        print("   ✅ Campos disponibles:")
        for campo in grupos[0].keys():
            if not campo.startswith("@") and not campo.startswith("_"):
                valor = grupos[0][campo]
                print(f"      {campo}: {valor}")
else:
    print(f"   ❌ Error: {response.status_code}")

# 2. Verificar si código 0000 ya existe
print("\n2. Verificando si código '0000' existe...")
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_grups?$filter=cr321_grupoid eq '0000'"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    grupos_existentes = response.json().get("value", [])
    if grupos_existentes:
        print("   ⚠️ Ya existe grupo con código 0000:")
        for g in grupos_existentes:
            print(f"      ID: {g.get('cr321_grupid')}")
            print(f"      Código: {g.get('cr321_grupoid')}")
            print(f"      Nombre: {g.get('cr321_nombre')}")
        print("\n   No se creará nuevo grupo.")
        exit(0)
    else:
        print("   ✅ Código 0000 disponible")

# 3. Crear grupo General
print("\n3. Creando grupo General...")

nuevo_grupo = {
    "cr321_grupoid": "0000",
    "cr321_nombre": "General",
    "cr321_tipo": 462410000,  # Primer tipo válido
}

url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_grups"
response = requests.post(url, headers=headers, json=nuevo_grupo)

if response.status_code == 204:
    print("   ✅ Grupo General creado exitosamente")

    # Obtener el ID del registro creado
    grupo_url = response.headers.get("OData-EntityId", "")
    print(f"   📍 URL: {grupo_url}")

elif response.status_code == 201:
    print("   ✅ Grupo General creado exitosamente")
    resultado = response.json()
    print(f"   📍 ID: {resultado.get('cr321_grupid')}")
else:
    print(f"   ❌ Error {response.status_code}")
    print(f"   {response.text[:500]}")
    exit(1)

# 4. Verificar creación
print("\n4. Verificando grupo creado...")
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_grups?$filter=cr321_grupoid eq '0000'"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    grupos = response.json().get("value", [])
    if grupos:
        grupo = grupos[0]
        print("   ✅ Grupo verificado:")
        print(f"      ID (GUID): {grupo.get('cr321_grupid')}")
        print(f"      Código: {grupo.get('cr321_grupoid')}")
        print(f"      Nombre: {grupo.get('cr321_nombre')}")
        print(f"      Tipo: {grupo.get('cr321_tipo')}")

        guid = grupo.get("cr321_grupid")
    else:
        print("   ❌ Grupo no encontrado después de crear")
        exit(1)

# 5. Actualizar conversaciones NULL al grupo General (0)
print("\n5. Actualizando conversaciones NULL al grupo General (0)...")

# Obtener mensajes con grupo NULL
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$filter=cr321_grupo eq null&$select=cr321_adatawp0id,cr321_phone"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    mensajes = response.json().get("value", [])
    print(f"   📧 {len(mensajes)} mensajes con grupo NULL")

    if mensajes:
        print("   🔄 Actualizando...")
        actualizados = 0
        errores = 0

        for msg in mensajes:
            msg_id = msg.get("cr321_adatawp0id")
            phone = msg.get("cr321_phone")

            # Actualizar a grupo 0
            update_data = {"cr321_grupo": 0}
            url_update = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s({msg_id})"

            resp = requests.patch(url_update, headers=headers, json=update_data)

            if resp.status_code == 204:
                actualizados += 1
            else:
                errores += 1
                if errores <= 3:  # Mostrar solo primeros errores
                    print(f"      ⚠️ Error en {phone[:15]}: {resp.status_code}")

        print(f"\n   ✅ Actualizados: {actualizados}")
        if errores > 0:
            print(f"   ❌ Errores: {errores}")
    else:
        print("   ℹ️ No hay mensajes para actualizar")
else:
    print(f"   ❌ Error obteniendo mensajes: {response.status_code}")

print("\n" + "=" * 70)
print("RESUMEN:")
print("=" * 70)
print("\n✅ Grupo 'General' creado con código '0000'")
print("✅ Conversaciones actualizadas al grupo 0")
print("\n📝 SIGUIENTE PASO: Actualizar backend/back.py")
print("   Cambiar INT_TO_GROUP:")
print("   {")
print("     0: 'General',")
print("     1: 'Soporte',")
print("     2: 'Ventas',")
print("     3: 'Administracion',")
print("     4: 'Contabilidad',")
print("     None: 'General'  # Fallback")
print("   }")
print("\n" + "=" * 70)
