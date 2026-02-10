"""
Verificar si lookup _cr321_grupo_value está poblado
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

token = get_token()
headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

print("="*80)
print("VERIFICACION LOOKUP _cr321_grupo_value EN cr321_usuariogrupos")
print("="*80)

# Obtener todos los registros de usuariogrupos
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuariogrupos?$select=cr321_usuariogrupoid,_cr321_usuarioid_value,_cr321_grupo_value,cr321_usuariogrupo1"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    relaciones = response.json().get("value", [])
    
    print(f"\nTotal relaciones: {len(relaciones)}")
    print(f"\n{'UsuarioID':<40} {'Lookup Grupo':<40} {'Codigo Texto':<10}")
    print("-"*90)
    
    con_lookup = 0
    sin_lookup = 0
    
    for r in relaciones:
        user_id = r.get("_cr321_usuarioid_value", "")[:38]
        lookup_grupo = r.get("_cr321_grupo_value")
        codigo_texto = r.get("cr321_usuariogrupo1", "")
        
        if lookup_grupo:
            con_lookup += 1
            print(f"{user_id:<40} {lookup_grupo[:38]:<40} {codigo_texto:<10}")
        else:
            sin_lookup += 1
            print(f"{user_id:<40} {'NULL':<40} {codigo_texto:<10}")
    
    print("\n" + "="*80)
    print("RESUMEN")
    print("="*80)
    print(f"Con lookup poblado: {con_lookup}")
    print(f"Sin lookup (NULL):  {sin_lookup}")
    
    if sin_lookup > 0:
        print("\n⚠️  PROBLEMA: El lookup _cr321_grupo_value existe pero NO está poblado")
        print("   Solo se usa el campo cr321_usuariogrupo1 (texto)")
        
        print("\n✅ SOLUCION: Migrar cr321_usuariogrupo1 → _cr321_grupo_value")
        print("   1. Obtener mapeo: codigo (0000-0004) -> GUID de grupo")
        print("   2. Actualizar cada registro con OData binding")
        print("   3. backend/api/usuario_grupos.py usar $expand")
    else:
        print("\n✅ Lookup poblado correctamente")
        
        # Intentar $expand
        print("\n" + "="*80)
        print("PRUEBA DE $EXPAND")
        print("="*80)
        
        url_expand = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuariogrupos?$top=1&$expand=cr321_grupo($select=cr321_nombre)"
        response = requests.get(url_expand, headers=headers)
        print(f"\nStatus: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json().get("value", [])
            if data:
                print("✅ $expand funciona correctamente")
                print(f"Datos: {data[0]}")
        elif response.status_code == 400:
            error = response.json().get("error", {}).get("message", "")
            print(f"❌ Error en $expand: {error[:100]}")
            print("   Verificar nombre de navegacion en metadata")
            
else:
    print(f"Error: {response.status_code}")
    print(response.text[:500])
