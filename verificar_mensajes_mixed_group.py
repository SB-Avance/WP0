"""
Verificar mensajes de conversación 573007864877 que aparece en 2 grupos
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

phone = "573007864877"
print("=" * 70)
print(f"MENSAJES DE {phone}")
print("=" * 70)

token = get_token()
headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$filter=cr321_phone eq '{phone}'&$select=cr321_messageid,cr321_body,cr321_grupo,cr321_timestamp&$orderby=cr321_timestamp desc"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    mensajes = response.json().get("value", [])
    print(f"\n✅ {len(mensajes)} mensajes encontrados\n")
    
    print(f"{'Timestamp':<20} {'Grupo':<10} {'Body':<40}")
    print("-" * 70)
    
    grupos = {}
    for msg in mensajes:
        grupo = msg.get("cr321_grupo")
        body = (msg.get("cr321_body") or "")[:38]
        timestamp = msg.get("cr321_timestamp", "")[:19]
        
        grupo_str = str(grupo) if grupo is not None else "NULL"
        print(f"{timestamp:<20} {grupo_str:<10} {body:<40}")
        
        grupos[grupo] = grupos.get(grupo, 0) + 1
    
    print("\n" + "=" * 70)
    print("RESUMEN:")
    for grupo, count in sorted(grupos.items(), key=lambda x: (x[0] is None, x[0])):
        if grupo is None:
            print(f"  NULL: {count} mensajes")
        else:
            grupo_nombre = {0: "General", 4: "Contabilidad"}.get(grupo, f"Grupo {grupo}")
            print(f"  {grupo_nombre} ({grupo}): {count} mensajes")
    
    print("\n" + "=" * 70)
    print("PROBLEMA:")
    print("  Esta conversación tiene mensajes con diferentes grupos")
    print("  El backend debe decidir:")
    print("  - Tomar grupo del mensaje más reciente")
    print("  - O unificar todos los mensajes al mismo grupo")
else:
    print(f"❌ Error: {response.status_code}")
