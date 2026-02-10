import requests
import os
from dotenv import load_dotenv
from msal import ConfidentialClientApplication

env_path = os.path.join('backend','.env')
load_dotenv(env_path)

DATAVERSE_URL = os.getenv("DATAVERSE_URL")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")

authority = f"https://login.microsoftonline.com/{TENANT_ID}"
app = ConfidentialClientApplication(CLIENT_ID, authority=authority, client_credential=CLIENT_SECRET)
result = app.acquire_token_for_client(scopes=[f"{DATAVERSE_URL}/.default"])
token = result['access_token']

headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}

# Consultar grupos
r = requests.get(
    f"{DATAVERSE_URL}/api/data/v9.2/cr321_grups",
    headers=headers,
    params={"$select": "cr321_grupoid,cr321_nombre"}
)

print("🔍 Grupos en Dataverse:")
print("=" * 70)
for grupo in r.json().get('value', []):
    print(f"  {grupo.get('cr321_nombre'):20} → {grupo.get('cr321_grupoid')}")
