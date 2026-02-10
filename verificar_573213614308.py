"""
Verificar grupo de conversacion 573213614308
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
print(f"Verificando {phone}...")

token = get_token()
headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$filter=cr321_phone eq '{phone}'&$select=cr321_messageid,cr321_grupo,_cr321_grupoid_value&$expand=cr321_grupoid($select=cr321_nombre)&$orderby=cr321_timestamp desc&$top=1"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    mensajes = response.json().get("value", [])
    if mensajes:
        msg = mensajes[0]
        grupo_int = msg.get("cr321_grupo")
        lookup = msg.get("_cr321_grupoid_value")
        grupo_obj = msg.get("cr321_grupoid")
        grupo_nombre = grupo_obj.get("cr321_nombre") if grupo_obj else "Sin grupo"
        
        print(f"  Integer: {grupo_int}")
        print(f"  Lookup: {lookup}")
        print(f"  Nombre: {grupo_nombre}")
