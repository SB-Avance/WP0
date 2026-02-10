"""
Ver estado de la migración y estadísticas
"""
import requests
import os
from dotenv import load_dotenv
from msal import ConfidentialClientApplication

env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend', '.env')
load_dotenv(env_path)

DATAVERSE_URL = os.getenv("DATAVERSE_URL")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")


def get_token():
    authority = f"https://login.microsoftonline.com/{TENANT_ID}"
    app = ConfidentialClientApplication(
        CLIENT_ID,
        authority=authority,
        client_credential=CLIENT_SECRET
    )
    result = app.acquire_token_for_client(scopes=[f"{DATAVERSE_URL}/.default"])
    return result["access_token"] if "access_token" in result else None


token = get_token()
headers = {
    'Authorization': f'Bearer {token}',
    'OData-MaxVersion': '4.0',
    'OData-Version': '4.0',
    'Accept': 'application/json'
}

print("=" * 60)
print("📊 ESTADO DE LA RELACIÓN CONTACTOS-CHATS")
print("=" * 60)

# Total de mensajes
url_total = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$count=true&$top=0"
response_total = requests.get(url_total, headers=headers)
total_mensajes = response_total.json().get("@odata.count", 0) if response_total.status_code == 200 else 0

# Mensajes con contacto
url_con = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$filter=_cr321_contactorelacion_value ne null&$count=true&$top=0"
response_con = requests.get(url_con, headers=headers)
con_contacto = response_con.json().get("@odata.count", 0) if response_con.status_code == 200 else 0

# Mensajes sin contacto
sin_contacto = total_mensajes - con_contacto

# Calcular porcentajes
porcentaje_con = (con_contacto / total_mensajes * 100) if total_mensajes > 0 else 0
porcentaje_sin = (sin_contacto / total_mensajes * 100) if total_mensajes > 0 else 0

print(f"\n📨 Total de mensajes:        {total_mensajes}")
print(f"✅ Con contacto asociado:    {con_contacto} ({porcentaje_con:.1f}%)")
print(f"⚠️  Sin contacto asociado:   {sin_contacto} ({porcentaje_sin:.1f}%)")

# Total de contactos
url_contactos = f"{DATAVERSE_URL}/api/data/v9.2/cr321_contactos?$count=true&$top=0"
response_contactos = requests.get(url_contactos, headers=headers)
total_contactos = response_contactos.json().get("@odata.count", 0) if response_contactos.status_code == 200 else 0

print(f"\n👤 Total de contactos:       {total_contactos}")

# Ejemplo de mensaje con contacto
print("\n📋 EJEMPLO DE MENSAJE CON CONTACTO:")
print("-" * 60)
url_ejemplo = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s"
params = {
    "$filter": "_cr321_contactorelacion_value ne null",
    "$expand": "cr321_contactorelacion($select=cr321_fromnombre,cr321_telefono)",
    "$select": "cr321_fromname,cr321_phone,cr321_timestamp",
    "$top": "1"
}
response_ejemplo = requests.get(url_ejemplo, params=params, headers=headers)

if response_ejemplo.status_code == 200:
    mensajes = response_ejemplo.json().get("value", [])
    if mensajes:
        msg = mensajes[0]
        contacto = msg.get("cr321_contactorelacion", {})
        print(f"De: {msg.get('cr321_fromname', 'N/A')}")
        print(f"Teléfono: {msg.get('cr321_phone', 'N/A')}")
        print(f"Contacto relacionado: {contacto.get('cr321_fromnombre', 'N/A')}")
        print(f"Teléfono contacto: {contacto.get('cr321_telefono', 'N/A')}")
        print("✅ ¡Relación funcionando correctamente!")

print("\n" + "=" * 60)
