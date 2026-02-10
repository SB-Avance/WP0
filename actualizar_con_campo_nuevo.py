"""
Verificar campo cr321_grupo y actualizar conversaciones al grupo 4 (Contabilidad)
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

import requests
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), 'backend', '.env'))

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
    "grant_type": "client_credentials"
}

print("\n=== ACTUALIZANDO GRUPOS ===\n")
print("1. Obteniendo token...", end=" ")
auth_response = requests.post(auth_url, data=auth_data)
token = auth_response.json().get("access_token")
print("✅")

headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

# Verificar que el campo existe
print("2. Verificando campo cr321_grupo...", end=" ")
url_test = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$top=1"
response_test = requests.get(url_test, headers=headers)

if response_test.status_code != 200:
    print(f"❌ Error {response_test.status_code}")
    exit(1)

mensaje_test = response_test.json().get("value", [])[0]
if "cr321_grupo" in mensaje_test:
    print(f"✅ Campo existe (valor actual: {mensaje_test.get('cr321_grupo')})")
else:
    print("❌ Campo aún no existe")
    print("\n💡 Espera unos segundos para que Dataverse sincronice el nuevo campo")
    exit(1)

# Obtener mensajes
print("3. Obteniendo mensajes...", end=" ")
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$top=100"
response = requests.get(url, headers=headers)

if response.status_code != 200:
    print(f"❌ Error {response.status_code}")
    exit(1)

mensajes = response.json().get("value", [])
print(f"✅ {len(mensajes)} mensajes")

# Agrupar por teléfono
conversaciones = {}
for msg in mensajes:
    phone = msg.get("cr321_phone")
    if not phone:
        continue
    if phone not in conversaciones:
        conversaciones[phone] = []
    conversaciones[phone].append(msg["cr321_adatawp0id"])

# Seleccionar 2 conversaciones
conv_list = list(conversaciones.items())[:2]

print(f"4. Actualizando {len(conv_list)} conversaciones al grupo 4 (Contabilidad)...\n")

headers_update = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "If-Match": "*"
}

total_actualizados = 0
total_mensajes = 0

for phone, mensaje_ids in conv_list:
    print(f"   Conversación {phone}: {len(mensaje_ids)} mensajes...", end=" ")
    
    actualizados = 0
    for msg_id in mensaje_ids:
        url_update = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s({msg_id})"
        payload = {"cr321_grupo": 4}
        
        resp = requests.patch(url_update, json=payload, headers=headers_update)
        if resp.status_code in [200, 204]:
            actualizados += 1
        elif actualizados == 0:  # Solo mostrar primer error
            print(f"\n      ⚠️ Error {resp.status_code}: {resp.text[:100]}")
    
    total_actualizados += actualizados
    total_mensajes += len(mensaje_ids)
    print(f"✅ {actualizados} actualizados")

print(f"\n✅ Completado: {total_actualizados}/{total_mensajes} mensajes actualizados")

if total_actualizados > 0:
    print(f"\n🎉 Usuario 0006 (Contabilidad) ahora verá {len(conv_list)} conversaciones")
else:
    print("\n⚠️  No se pudo actualizar ningún mensaje. Verifica permisos en Dataverse")
