"""
Verificar sincronización lookup
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
print("ESTADO SINCRONIZACION")
print("="*70)

token = get_token()
headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

# Obtener mapeo
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_grups?$select=cr321_grupid,cr321_grupoid,cr321_nombre"
response = requests.get(url, headers=headers)

INT_TO_GUID = {}
if response.status_code == 200:
    for g in response.json().get("value", []):
        int_val = int(g.get("cr321_grupoid"))
        INT_TO_GUID[int_val] = g.get("cr321_grupid")

# Verificar mensajes
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$select=cr321_grupo,_cr321_grupoid_value"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    mensajes = response.json().get("value", [])
    sincronizados = 0
    desincronizados = 0
    
    for msg in mensajes:
        grupo_int = msg.get("cr321_grupo")
        lookup = msg.get("_cr321_grupoid_value")
        
        if grupo_int is not None and grupo_int in INT_TO_GUID:
            if lookup == INT_TO_GUID[grupo_int]:
                sincronizados += 1
            else:
                desincronizados += 1
    
    print(f"\nTotal mensajes: {len(mensajes)}")
    print(f"Sincronizados: {sincronizados}")
    print(f"Desincronizados: {desincronizados}")
    
    if desincronizados == 0:
        print("\nOK - Todos los mensajes estan sincronizados")
    else:
        print(f"\nPENDIENTE - {desincronizados} mensajes sin sincronizar")

print("="*70)
