"""
Verificar disponibilidad del campo cr321_grupo con diferentes métodos
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "backend", ".env"))

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
DATAVERSE_URL = os.getenv("DATAVERSE_URL")

# Obtener token
auth_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
auth_data = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "scope": f"{DATAVERSE_URL}/.default",
    "grant_type": "client_credentials",
}

auth_response = requests.post(auth_url, data=auth_data)
token = auth_response.json().get("access_token")
headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

print("\n=== DIAGNÓSTICO CAMPO cr321_grupo ===\n")

# Método 1: Consulta estándar
print("1. Consulta estándar (sin $select):")
url1 = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$top=1"
r1 = requests.get(url1, headers=headers)
if r1.status_code == 200:
    msg = r1.json().get("value", [{}])[0]
    if "cr321_grupo" in msg:
        print(f"   ✅ Campo existe - Valor: {msg.get('cr321_grupo')}")
    else:
        print(f"   ❌ Campo no aparece")
        print(
            f"   Campos disponibles: {', '.join([k for k in msg.keys() if not k.startswith('@')][:10])}..."
        )

# Método 2: Consulta con $select
print("\n2. Consulta con $select=cr321_grupo:")
url2 = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$top=1&$select=cr321_grupo"
r2 = requests.get(url2, headers=headers)
if r2.status_code == 200:
    print(f"   ✅ Campo es seleccionable")
    msg = r2.json().get("value", [{}])[0]
    print(f"   Valor: {msg.get('cr321_grupo')}")
elif r2.status_code == 400:
    error = r2.json().get("error", {}).get("message", "")
    if "Could not find" in error:
        print(f"   ❌ Campo no existe en el schema")
    else:
        print(f"   ⚠️ Error 400: {error[:100]}")
else:
    print(f"   ⚠️ Error {r2.status_code}")

# Método 3: Intentar actualizar
print("\n3. Prueba de actualización:")
url_test = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$top=1"
r_test = requests.get(url_test, headers=headers)
if r_test.status_code == 200:
    msg_id = r_test.json().get("value", [{}])[0].get("cr321_adatawp0id")
    if msg_id:
        url_update = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s({msg_id})"
        headers_update = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "If-Match": "*",
        }
        payload = {"cr321_grupo": 4}

        r_update = requests.patch(url_update, json=payload, headers=headers_update)
        if r_update.status_code in [200, 204]:
            print(f"   ✅ Actualización exitosa - Campo es editable")
        elif r_update.status_code == 400:
            error = r_update.json().get("error", {}).get("message", "")
            if "does not exist" in error.lower() or "not found" in error.lower():
                print(f"   ❌ Campo no existe")
            else:
                print(f"   ⚠️ Error 400: {error[:150]}")
        else:
            print(f"   ⚠️ Error {r_update.status_code}")

print("\n" + "=" * 60)
print("\n💡 Recomendaciones:")
print("   1. Verifica que el campo se haya guardado en Dataverse")
print("   2. Refresca la página de Dataverse")
print("   3. El campo puede tardar 1-2 minutos en sincronizarse")
print("   4. Verifica que el nombre del campo sea exactamente: cr321_grupo")
