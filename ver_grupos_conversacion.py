"""
Ver todos los grupos de mensajes de 573213614308
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

phone = "573213614308"
token = get_token()
headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$filter=cr321_phone eq '{phone}'&$select=cr321_timestamp,_cr321_grupoid_value&$expand=cr321_grupoid($select=cr321_nombre)&$orderby=cr321_timestamp desc"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    mensajes = response.json().get("value", [])
    print(f"Total mensajes: {len(mensajes)}")
    
    grupos_unicos = {}
    for msg in mensajes:
        grupo_obj = msg.get("cr321_grupoid")
        grupo_nombre = grupo_obj.get("cr321_nombre") if grupo_obj else "Sin grupo"
        timestamp = msg.get("cr321_timestamp", "")[:19]
        
        if grupo_nombre not in grupos_unicos:
            grupos_unicos[grupo_nombre] = {"count": 0, "ultimo": timestamp}
        grupos_unicos[grupo_nombre]["count"] += 1
    
    print("\nGrupos en esta conversacion:")
    for nombre, info in sorted(grupos_unicos.items(), key=lambda x: x[1]["count"], reverse=True):
        print(f"  {nombre}: {info['count']} mensajes (ultimo: {info['ultimo']})")
