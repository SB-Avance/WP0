"""
Asignar conversaciones al grupo Contabilidad para pruebas
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

import requests
from goot import DATAVERSE_URL, get_token

token = get_token()
headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

print("\n=== ASIGNANDO CONVERSACIONES AL GRUPO CONTABILIDAD ===\n")

# Obtener algunas conversaciones
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s"
url += "?$select=cr321_conversationid,cr321_grupo,cr321_adatawp0id"
url += "&$orderby=cr321_conversationid"

response = requests.get(url, headers=headers)

if response.status_code != 200:
    print(f"❌ Error al obtener conversaciones: {response.status_code}")
    exit(1)

data = response.json()
mensajes = data.get("value", [])

# Agrupar por conversación
conversaciones = {}
for msg in mensajes:
    conv_id = msg.get("cr321_conversationid")
    if conv_id not in conversaciones:
        conversaciones[conv_id] = {
            "conv_id": conv_id,
            "grupo_actual": msg.get("cr321_grupo"),
            "mensaje_ids": [],
        }
    conversaciones[conv_id]["mensaje_ids"].append(msg.get("cr321_adatawp0id"))

# Seleccionar 2-3 conversaciones para asignar a Contabilidad
conversaciones_list = list(conversaciones.values())
print(f"Total conversaciones encontradas: {len(conversaciones_list)}\n")

# Asignar las primeras 2 conversaciones al grupo 4 (Contabilidad)
cantidad_asignar = min(2, len(conversaciones_list))

print(f"Asignando {cantidad_asignar} conversación(es) al grupo 4 (Contabilidad)...\n")

headers_update = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "If-Match": "*",
}

for i in range(cantidad_asignar):
    conv = conversaciones_list[i]
    conv_id = conv["conv_id"]
    mensaje_ids = conv["mensaje_ids"]

    print(f"Conversación {i+1}: {conv_id}")
    print(f"   {len(mensaje_ids)} mensaje(s) a actualizar")

    # Actualizar todos los mensajes de esta conversación
    actualizados = 0
    for msg_id in mensaje_ids:
        url_update = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s({msg_id})"
        payload = {"cr321_grupo": 4}

        response_update = requests.patch(
            url_update, json=payload, headers=headers_update
        )
        if response_update.status_code == 204:
            actualizados += 1

    print(f"   ✅ {actualizados} mensaje(s) actualizados\n")

print(f"\n✅ Proceso completado")
print(
    f"\nAhora el usuario 0006 (Contabilidad) verá {cantidad_asignar} conversación(es)"
)
