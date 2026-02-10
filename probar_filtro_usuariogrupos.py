"""
Probar consulta directa a cr321_usuariogrupos con el filtro
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from goot import get_token, DATAVERSE_URL
import requests

token = get_token()
headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

usuario_id = "e45580f3-59fa-f011-8406-002248df122f"

# Probar diferentes variantes del nombre del campo
variantes = [
    "_cr321_usuarioId_value",  # Con mayúscula
    "_cr321_usuarioid_value",  # Todo minúsculas  
    "_cr321_Usuarioid_value",  # Otra variante
]

print(f"\n🧪 Probando filtros para usuario {usuario_id[:8]}...\n")

for campo in variantes:
    print(f"Probando filtro: {campo}...", end=" ")
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuariogrupos"
    url += f"?$filter={campo} eq {usuario_id}"
    url += "&$select=cr321_usuariogrupoid,cr321_usuariogrupo1"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        count = len(data.get("value", []))
        print(f"✅ {count} registro(s)")
        
        if count > 0:
            print(f"\n   Campo correcto: {campo}\n")
            for i, reg in enumerate(data.get("value", []), 1):
                print(f"   Registro {i}:")
                print(f"      ID: {reg.get('cr321_usuariogrupoid')}")
                print(f"      Código grupo: {reg.get('cr321_usuariogrupo1')}")
            break
    else:
        error = response.json().get("error", {}).get("message", "")[:100]
        print(f"❌ {error}")
