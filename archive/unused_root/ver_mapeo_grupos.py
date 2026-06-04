"""
Ver mapeo de códigos de grupo
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

import requests
from goot import DATAVERSE_URL, get_token

token = get_token()
headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

print("\n=== TABLA cr321_grup ===\n")

# Ver grupos
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_grups?$select=cr321_grupoid,cr321_nombre,cr321_tipo"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    grupos = response.json().get("value", [])
    print(f"Grupos existentes ({len(grupos)}):\n")
    for g in grupos:
        print(
            f"  {g.get('cr321_grupoid')} -> {g.get('cr321_nombre')} (tipo: {g.get('cr321_tipo')})"
        )

print("\n\n=== TABLA cr321_usuariogrupos ===\n")

# Ver asignaciones
url2 = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuariogrupos?$select=_cr321_usuarioid_value,cr321_usuariogrupo1"
response2 = requests.get(url2, headers=headers)

if response2.status_code == 200:
    asignaciones = response2.json().get("value", [])
    print(f"Asignaciones existentes ({len(asignaciones)}):\n")
    for a in asignaciones:
        usuario_id = a.get("_cr321_usuarioid_value")
        grupo_codigo = a.get("cr321_usuariogrupo1")
        usuario_short = usuario_id[:8] if usuario_id else "N/A"
        print(f"  Usuario {usuario_short}... -> Grupo código '{grupo_codigo}'")
