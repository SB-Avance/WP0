"""
Verificar lookup existente _cr321_grupoid_value
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
print("VERIFICAR LOOKUP _cr321_grupoid_value")
print("=" * 70)

token = get_token()
headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

# 1. Verificar campos disponibles
print("\n1. Verificando campos de mensajes...")
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$top=1"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    mensajes = response.json().get("value", [])
    if mensajes:
        msg = mensajes[0]
        campos_grupo = {k: v for k, v in msg.items() if 'grupo' in k.lower() or 'grup' in k.lower()}
        
        print("   ✅ Campos relacionados con grupo:")
        for campo, valor in campos_grupo.items():
            print(f"      {campo}: {valor}")

# 2. Obtener GUIDs de todos los grupos
print("\n2. Obteniendo GUIDs de grupos...")
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_grups?$select=cr321_grupid,cr321_grupoid,cr321_nombre"
response = requests.get(url, headers=headers)

grupos_map = {}
if response.status_code == 200:
    grupos = response.json().get("value", [])
    print(f"   ✅ {len(grupos)} grupos encontrados:")
    for g in grupos:
        guid = g.get("cr321_grupid")
        codigo = g.get("cr321_grupoid")
        nombre = g.get("cr321_nombre")
        grupos_map[codigo] = {"guid": guid, "nombre": nombre}
        print(f"      {codigo} ({nombre}): {guid}")

# 3. Comparar cr321_grupo vs _cr321_grupoid_value
print("\n3. Comparando campo integer vs lookup...")
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$select=cr321_phone,cr321_grupo,_cr321_grupoid_value&$top=10&$orderby=cr321_timestamp desc"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    mensajes = response.json().get("value", [])
    
    print(f"\n   {'Phone':<18} {'Integer':<10} {'Lookup (GUID)':<40}")
    print("   " + "-" * 68)
    
    for msg in mensajes:
        phone = msg.get("cr321_phone", "N/A")[:16]
        grupo_int = msg.get("cr321_grupo")
        grupo_lookup = msg.get("_cr321_grupoid_value")
        
        int_str = str(grupo_int) if grupo_int is not None else "NULL"
        lookup_str = grupo_lookup[:38] if grupo_lookup else "NULL"
        
        print(f"   {phone:<18} {int_str:<10} {lookup_str:<40}")
    
    # Estadísticas
    con_int = sum(1 for m in mensajes if m.get("cr321_grupo") is not None)
    con_lookup = sum(1 for m in mensajes if m.get("_cr321_grupoid_value") is not None)
    
    print(f"\n   📊 Estadísticas (últimos 10 mensajes):")
    print(f"      Mensajes con cr321_grupo: {con_int}/10")
    print(f"      Mensajes con _cr321_grupoid_value: {con_lookup}/10")

print("\n" + "=" * 70)
print("RECOMENDACIÓN:")
print("=" * 70)
print("\n✅ USAR LOOKUP en lugar de integer:")
print("   1. Eliminar campo cr321_grupo (integer)")
print("   2. Usar campo _cr321_grupoid_value (lookup existente)")
print("   3. Refactorizar backend para usar lookup")
print("\n📝 Ventajas del lookup:")
print("   - Integridad referencial automática")
print("   - Navegación con $expand")
print("   - Validación automática de Dataverse")
print("   - No necesita mapeo manual INT_TO_GROUP")
print("\n" + "=" * 70)
