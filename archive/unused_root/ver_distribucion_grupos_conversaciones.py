"""
Ver distribución de grupos en conversaciones
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

import requests
from goot import DATAVERSE_URL, get_token

token = get_token()
headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

print("\n=== DISTRIBUCIÓN DE GRUPOS EN CONVERSACIONES ===\n")

# Consultar todas las conversaciones
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s"
url += "?$select=cr321_conversationid,cr321_grupo"
url += "&$orderby=cr321_conversationid"

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    conversaciones = data.get("value", [])

    # Agrupar por conversationid
    conv_map = {}
    for msg in conversaciones:
        conv_id = msg.get("cr321_conversationid")
        grupo = msg.get("cr321_grupo")

        if conv_id not in conv_map:
            conv_map[conv_id] = grupo

    # Mapeo de grupos
    GRUPO_MAP = {
        1: "Soporte",
        2: "Ventas",
        3: "Administracion",
        4: "Contabilidad",
        None: "GENERAL",
    }

    # Contar por grupo
    grupo_count = {}
    for grupo in conv_map.values():
        nombre = GRUPO_MAP.get(grupo, f"Desconocido ({grupo})")
        grupo_count[nombre] = grupo_count.get(nombre, 0) + 1

    print(f"Total conversaciones únicas: {len(conv_map)}\n")
    print("Distribución por grupo:")
    for nombre, count in sorted(grupo_count.items()):
        print(f"  {nombre}: {count} conversación(es)")

    print("\n" + "=" * 50)
    print("\n⚠️  Usuario 0006 pertenece a: Contabilidad")
    contab_count = grupo_count.get("Contabilidad", 0)
    if contab_count == 0:
        print("❌ NO hay conversaciones de Contabilidad")
        print("   El usuario NO verá ninguna conversación")
        print("\n💡 Solución:")
        print("   - Asignar algunas conversaciones al grupo 4 (Contabilidad)")
        print("   - O asignar al usuario a un grupo con conversaciones (ej: GENERAL)")
    else:
        print(f"✅ Hay {contab_count} conversación(es) de Contabilidad")
        print("   El usuario verá estas conversaciones")
else:
    print(f"❌ Error: {response.status_code}")
