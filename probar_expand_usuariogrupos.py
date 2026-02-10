"""
Probar $expand con cr321_usuarioid en la tabla cr321_usuariogrupos
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from goot import get_token, DATAVERSE_URL
import requests
import json

token = get_token()
headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

usuario_id = "e45580f3-59fa-f011-8406-002248df122f"

print(f"\n🔍 Buscando grupos del usuario {usuario_id[:8]}...\n")

# Probar con $expand al usuario
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuariogrupos"
url += f"?$filter=_cr321_usuarioid_value eq {usuario_id}"
url += "&$expand=cr321_usuarioid($select=cr321_nombre,cr321_correo,cr321_idusuario)"

print(f"URL: {url}\n")

response = requests.get(url, headers=headers)

print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    registros = data.get("value", [])
    
    print(f"\n✅ {len(registros)} grupo(s) encontrado(s)\n")
    
    for i, reg in enumerate(registros, 1):
        print(f"\n=== GRUPO {i} ===")
        print(f"ID Relación: {reg.get('cr321_usuariogrupoid')}")
        print(f"Grupo (texto): {reg.get('cr321_usuariogrupo1')}")
        
        usuario_data = reg.get("cr321_usuarioid", {})
        if usuario_data:
            print(f"\nUsuario expandido:")
            print(f"   ID Usuario: {usuario_data.get('cr321_idusuario')}")
            print(f"   Nombre: {usuario_data.get('cr321_nombre')}")
            print(f"   Correo: {usuario_data.get('cr321_correo')}")
else:
    print(f"\n❌ Error: {response.text[:500]}")
