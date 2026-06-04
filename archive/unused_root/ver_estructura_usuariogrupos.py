"""
Ver estructura completa de cr321_usuariogrupos
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

import json

import requests
from goot import DATAVERSE_URL, get_token

token = get_token()
headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

print("\n📋 Consultando cr321_usuariogrupos...")

# Consulta básica
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuariogrupos?$top=2"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    registros = data.get("value", [])

    print(f"\n✅ {len(registros)} registro(s)encontrados\n")

    for i, reg in enumerate(registros, 1):
        print(f"\n=== REGISTRO {i} ===")
        for key, value in sorted(reg.items()):
            if not key.startswith("@"):
                print(f"   {key}: {value}")

    # Intentar con diferentes expands
    print("\n\n🧪 Probando $expand con posibles lookups...\n")

    lookups_posibles = ["cr321_usuariogrupo1", "cr321_Usuario", "cr321_Grupo"]

    for lookup in lookups_posibles:
        test_url = (
            f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuariogrupos?$top=1&$expand={lookup}"
        )
        print(f"   Probando $expand={lookup}...", end=" ")

        test_response = requests.get(test_url, headers=headers)
        if test_response.status_code == 200:
            print("✅")
        else:
            error_msg = test_response.json().get("error", {}).get("message", "")[:80]
            print(f"❌ {error_msg}")
else:
    print(f"❌ Error {response.status_code}: {response.text}")
