"""
Unificar conversación 573007864877 al grupo Contabilidad (4)
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
print("UNIFICAR CONVERSACIÓN 573007864877 A CONTABILIDAD")
print("=" * 70)

token = get_token()
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}

phone = "573007864877"

# Obtener mensajes con grupo 0 (General)
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$filter=cr321_phone eq '{phone}' and cr321_grupo eq 0&$select=cr321_adatawp0id,cr321_body"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    mensajes = response.json().get("value", [])
    print(f"\n📧 {len(mensajes)} mensajes con grupo General (0)")

    if mensajes:
        print("🔄 Actualizando a Contabilidad (4)...\n")
        actualizados = 0

        for msg in mensajes:
            msg_id = msg.get("cr321_adatawp0id")
            body = (msg.get("cr321_body") or "")[:40]

            update_data = {"cr321_grupo": 4}
            url_update = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s({msg_id})"

            resp = requests.patch(url_update, headers=headers, json=update_data)

            if resp.status_code == 204:
                actualizados += 1
                print(f"  ✅ {body}")
            else:
                print(f"  ❌ Error {resp.status_code}: {body}")

        print(f"\n✅ {actualizados} mensajes actualizados a Contabilidad")
    else:
        print("ℹ️ No hay mensajes para actualizar")
else:
    print(f"❌ Error: {response.status_code}")

print("\n" + "=" * 70)
