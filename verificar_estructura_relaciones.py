"""
Verificar estructura completa de relaciones usuarios-grupos
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

print("="*70)
print("VERIFICACION ESTRUCTURA RELACIONES")
print("="*70)

token = get_token()
headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

# 1. Tabla cr321_grup (grupos)
print("\n1. TABLA cr321_grup (Grupos)")
print("-"*70)
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_grups?$select=cr321_grupid,cr321_grupoid,cr321_nombre"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    grupos = response.json().get("value", [])
    print(f"Total grupos: {len(grupos)}")
    print(f"\n{'GUID':<40} {'Codigo':<10} {'Nombre':<20}")
    print("-"*70)
    for g in grupos:
        guid = g.get("cr321_grupid", "")[:38]
        codigo = g.get("cr321_grupoid", "")
        nombre = g.get("cr321_nombre", "")
        print(f"{guid:<40} {codigo:<10} {nombre:<20}")

# 2. Tabla cr321_usuarios (usuarios)
print("\n\n2. TABLA cr321_usuarios (Usuarios)")
print("-"*70)
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuarioses?$select=cr321_usuariosid,cr321_correo,cr321_nombre&$top=5"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    usuarios = response.json().get("value", [])
    print(f"Total usuarios (muestra 5): {len(usuarios)}")
    print(f"\n{'GUID':<40} {'Correo':<20} {'Nombre':<20}")
    print("-"*70)
    for u in usuarios:
        guid = u.get("cr321_usuariosid", "")[:38]
        correo = u.get("cr321_correo", "")[:18]
        nombre = u.get("cr321_nombre", "")[:18]
        print(f"{guid:<40} {correo:<20} {nombre:<20}")

# 3. Tabla cr321_usuariogrupos (relacion N:N)
print("\n\n3. TABLA cr321_usuariogrupos (Relacion Usuario-Grupo)")
print("-"*70)
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuariogrupos?$select=cr321_usuariogrupoid,_cr321_usuarioid_value,cr321_usuariogrupo1&$top=5"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    relaciones = response.json().get("value", [])
    print(f"Total relaciones (muestra 5): {len(relaciones)}")
    print(f"\n{'RelacionID':<40} {'UsuarioID':<40} {'Codigo Grupo':<15}")
    print("-"*70)
    for r in relaciones:
        rel_id = r.get("cr321_usuariogrupoid", "")[:38]
        user_id = r.get("_cr321_usuarioid_value", "")[:38]
        codigo = r.get("cr321_usuariogrupo1", "")
        print(f"{rel_id:<40} {user_id:<40} {codigo:<15}")

# 4. Verificar campos lookup en cr321_usuariogrupos
print("\n\n4. ESTRUCTURA DE cr321_usuariogrupos")
print("-"*70)
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuariogrupos?$top=1"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json().get("value", [])
    if data:
        registro = data[0]
        campos_lookup = {k: v for k, v in registro.items() if '_' in k or 'grupo' in k.lower() or 'usuario' in k.lower()}
        
        print("Campos relacionales:")
        for campo, valor in sorted(campos_lookup.items()):
            if not campo.startswith("@"):
                tipo = "GUID" if isinstance(valor, str) and len(valor) == 36 else "Texto"
                print(f"  {campo:<40} {tipo:<10} {str(valor)[:30]}")

# 5. Intentar expandir relaciones
print("\n\n5. PRUEBA DE $EXPAND EN cr321_usuariogrupos")
print("-"*70)

# Intentar expandir usuario
print("\nA. Expandir _cr321_usuarioid_value:")
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuariogrupos?$top=1&$expand=cr321_usuarioid($select=cr321_nombre,cr321_correo)"
response = requests.get(url, headers=headers)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json().get("value", [])
    if data and "cr321_usuarioid" in data[0]:
        user = data[0]["cr321_usuarioid"]
        print(f"   OK - Usuario: {user.get('cr321_nombre')}")
    else:
        print(f"   Sin datos expandidos")
elif response.status_code == 400:
    error = response.json().get("error", {}).get("message", "")
    print(f"   Error: {error[:80]}")

# Intentar expandir grupo (si existe lookup)
print("\nB. Verificar si existe lookup a grupos:")
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuariogrupos?$top=1"
response = requests.get(url, headers=headers)
if response.status_code == 200:
    data = response.json().get("value", [])
    if data:
        campos_grupo = [k for k in data[0].keys() if 'grupo' in k.lower() and k.startswith('_') and k.endswith('_value')]
        if campos_grupo:
            print(f"   Lookups de grupo encontrados: {campos_grupo}")
        else:
            print(f"   NO hay lookup a tabla de grupos")
            print(f"   Solo existe campo de texto: cr321_usuariogrupo1")

print("\n" + "="*70)
print("DIAGNOSTICO")
print("="*70)

print("\nESTRUCTURA ACTUAL:")
print("  cr321_usuarios (PK: cr321_usuariosid)")
print("     |")
print("     +-- cr321_usuariogrupos")
print("             - _cr321_usuarioid_value --> lookup a cr321_usuarios")
print("             - cr321_usuariogrupo1 --> codigo texto (0001-0004)")
print("             - NO HAY lookup a cr321_grup")
print("     |")
print("  cr321_grup (PK: cr321_grupid, codigo: cr321_grupoid)")

print("\nPROBLEMA:")
print("  La tabla cr321_usuariogrupos NO tiene lookup a cr321_grup")
print("  Solo usa un campo de texto 'cr321_usuariogrupo1' con codigos")
print("  Esto NO es una relacion de integridad referencial")

print("\nSOLUCION CORRECTA:")
print("  1. Agregar lookup en cr321_usuariogrupos a cr321_grup")
print("  2. Migrar datos de cr321_usuariogrupo1 al nuevo lookup")
print("  3. Eliminar campo cr321_usuariogrupo1")
print("  4. backend/api/usuario_grupos.py usar $expand para nombres")

print("\n" + "="*70)
