"""
Migración: Sincronizar campo integer cr321_grupo → lookup _cr321_grupoid_value
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
    app = ConfidentialClientApplication(CLIENT_ID, authority=authority, client_credential=CLIENT_SECRET)
    result = app.acquire_token_for_client(scopes=scope)
    return result["access_token"]

print("=" * 70)
print("MIGRACIÓN: INTEGER → LOOKUP")
print("=" * 70)

token = get_token()
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# 1. Obtener mapeo de grupos
print("\n1. Obteniendo mapeo de grupos...")
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_grups?$select=cr321_grupid,cr321_grupoid,cr321_nombre"
response = requests.get(url, headers=headers)

INT_TO_GUID = {}
if response.status_code == 200:
    grupos = response.json().get("value", [])
    print(f"   ✅ {len(grupos)} grupos encontrados:")
    
    # Mapear: 0→0000, 1→0001, etc.
    for g in grupos:
        codigo = g.get("cr321_grupoid")  # "0000", "0001", etc.
        guid = g.get("cr321_grupid")
        nombre = g.get("cr321_nombre")
        
        # Convertir código a integer: "0000"→0, "0001"→1, etc.
        int_val = int(codigo)
        INT_TO_GUID[int_val] = {"guid": guid, "nombre": nombre, "codigo": codigo}
        
        print(f"      {int_val} → {nombre} ({guid})")
else:
    print(f"   ❌ Error: {response.status_code}")
    exit(1)

# 2. Obtener todos los mensajes
print("\n2. Obteniendo mensajes...")
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$select=cr321_adatawp0id,cr321_phone,cr321_grupo,_cr321_grupoid_value&$orderby=cr321_timestamp desc"
response = requests.get(url, headers=headers)

if response.status_code != 200:
    print(f"   ❌ Error: {response.status_code}")
    exit(1)

mensajes = response.json().get("value", [])
print(f"   ✅ {len(mensajes)} mensajes encontrados")

# 3. Identificar mensajes para actualizar
print("\n3. Analizando inconsistencias...")

actualizar = []
for msg in mensajes:
    msg_id = msg.get("cr321_adatawp0id")
    phone = msg.get("cr321_phone")
    grupo_int = msg.get("cr321_grupo")
    lookup_actual = msg.get("_cr321_grupoid_value")
    
    # Verificar si necesita actualización
    if grupo_int is not None and grupo_int in INT_TO_GUID:
        guid_esperado = INT_TO_GUID[grupo_int]["guid"]
        
        # Si el lookup es diferente al esperado, actualizar
        if lookup_actual != guid_esperado:
            actualizar.append({
                "id": msg_id,
                "phone": phone,
                "grupo_int": grupo_int,
                "guid_esperado": guid_esperado,
                "nombre": INT_TO_GUID[grupo_int]["nombre"]
            })

print(f"   📋 {len(actualizar)} mensajes necesitan actualización")
print(f"   ✅ {len(mensajes) - len(actualizar)} mensajes ya sincronizados")

if not actualizar:
    print("\n✅ Todos los mensajes ya están sincronizados")
    exit(0)

# 4. Mostrar resumen por grupo
print("\n4. Resumen de actualización:")
resumen = {}
for item in actualizar:
    nombre = item["nombre"]
    resumen[nombre] = resumen.get(nombre, 0) + 1

for nombre, count in sorted(resumen.items()):
    print(f"   {nombre}: {count} mensajes")

# 5. Confirmar
print(f"\n⚠️  Se actualizarán {len(actualizar)} mensajes")
respuesta = input("¿Continuar? (s/n): ")

if respuesta.lower() != 's':
    print("\n❌ Cancelado por el usuario")
    exit(0)

# 6. Actualizar mensajes
print("\n5. Actualizando mensajes...")
actualizados = 0
errores = 0
progreso = 0

for item in actualizar:
    progreso += 1
    msg_id = item["id"]
    guid = item["guid_esperado"]
    
    # Usar OData binding para el lookup
    update_data = {
        "cr321_grupoid@odata.bind": f"/cr321_grups({guid})"
    }
    
    url_update = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s({msg_id})"
    resp = requests.patch(url_update, headers=headers, json=update_data)
    
    if resp.status_code in [200, 204]:
        actualizados += 1
        if progreso % 10 == 0:
            print(f"   ⏳ {progreso}/{len(actualizar)}...")
    else:
        errores += 1
        if errores <= 5:
            print(f"   ❌ Error en {item['phone']}: {resp.status_code}")

print(f"\n✅ Actualización completada:")
print(f"   ✅ Exitosos: {actualizados}")
print(f"   ❌ Errores: {errores}")

# 7. Verificar resultado
print("\n6. Verificando resultado...")
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$select=cr321_grupo,_cr321_grupoid_value&$top=100"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    mensajes = response.json().get("value", [])
    sincronizados = 0
    desincronizados = 0
    
    for msg in mensajes:
        grupo_int = msg.get("cr321_grupo")
        lookup = msg.get("_cr321_grupoid_value")
        
        if grupo_int is not None and grupo_int in INT_TO_GUID:
            if lookup == INT_TO_GUID[grupo_int]["guid"]:
                sincronizados += 1
            else:
                desincronizados += 1
    
    print(f"   ✅ Sincronizados: {sincronizados}")
    print(f"   ⚠️  Desincronizados: {desincronizados}")

print("\n" + "=" * 70)
print("MIGRACIÓN COMPLETADA")
print("=" * 70)
print("\n📝 PRÓXIMO PASO: Refactorizar backend para usar lookup")
print("   - backend/back.py: Usar _cr321_grupoid_value con $expand")
print("   - Eliminar INT_TO_GROUP y GROUP_TO_INT")
print("\n" + "=" * 70)
