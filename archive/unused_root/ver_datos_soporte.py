"""
Script para ver los datos completos del chatbot de Soporte
"""

import json
import sys

import requests

sys.path.append("backend")
from goot import CLIENT_ID, CLIENT_SECRET, DATAVERSE_URL, TENANT_ID


def get_token():
    """Obtener token de autenticación"""
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": f"{DATAVERSE_URL}/.default",
        "grant_type": "client_credentials",
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    return None


def main():
    """Ver detalles del chatbot de Soporte"""
    token = get_token()
    if not token:
        print("❌ Error: No se pudo obtener token")
        return

    # Buscar el chatbot "Soporte"
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_chatbots"
    url += "?$filter=cr321_name eq 'Soporte'"
    url += "&$select=cr321_chatbotid,cr321_name,cr321_active,cr321_elemento1,cr321_elemento2,cr321_elemento3,cr321_config,cr321_type,cr321_grupoid"

    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code != 200:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return

    data = response.json()
    chatbots = data.get("value", [])

    if not chatbots:
        print("❌ No se encontró el chatbot 'Soporte'")
        return

    chatbot = chatbots[0]

    print("\n" + "=" * 70)
    print("📍 UBICACIÓN DEL MENÚ DE SOPORTE")
    print("=" * 70)
    print()
    print(f"🗄️  Base de datos:    Microsoft Dataverse")
    print(f"📊 Tabla:            cr321_chatbot")
    print(f"🔑 ID (GUID):        {chatbot.get('cr321_chatbotid')}")
    print(f"📝 Nombre:           {chatbot.get('cr321_name')}")
    print(
        f"✅ Estado:           {'ACTIVO' if chatbot.get('cr321_active') else 'INACTIVO'}"
    )
    print()
    print("=" * 70)
    print("📋 OPCIONES DEL MENÚ (Campos de la tabla)")
    print("=" * 70)
    print()
    print(f"cr321_elemento1:     {chatbot.get('cr321_elemento1')}")
    print(f"cr321_elemento2:     {chatbot.get('cr321_elemento2')}")
    print(f"cr321_elemento3:     {chatbot.get('cr321_elemento3')}")
    print()

    if chatbot.get("cr321_config"):
        print("=" * 70)
        print("⚙️  CONFIGURACIÓN ADICIONAL (cr321_config)")
        print("=" * 70)
        print()
        try:
            config = json.loads(chatbot.get("cr321_config"))
            print(json.dumps(config, indent=2, ensure_ascii=False))
        except:
            print(chatbot.get("cr321_config"))
        print()

    print("=" * 70)
    print("🌐 ACCESO DIRECTO")
    print("=" * 70)
    print()
    print(f"URL de Dataverse:")
    print(f"  {DATAVERSE_URL}")
    print()
    print(f"Para editar este chatbot:")
    print(f"  1. Ir a Power Apps (make.powerapps.com)")
    print(f"  2. Seleccionar tu entorno")
    print(f"  3. Ir a Tablas > cr321_chatbot")
    print(f"  4. Buscar el registro 'Soporte'")
    print(f"  5. Editar los campos cr321_elemento1, cr321_elemento2, cr321_elemento3")
    print()
    print("=" * 70)
    print("🔄 APLICAR CAMBIOS")
    print("=" * 70)
    print()
    print("Después de editar en Dataverse:")
    print("  - Los cambios se aplican automáticamente en 5 minutos")
    print("  - O reinicia el backend: .\\iniciar_backend.ps1")
    print()


if __name__ == "__main__":
    main()
