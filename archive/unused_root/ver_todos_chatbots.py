"""
Ver TODOS los chatbots y sus opciones
"""

import json
import os
import sys

import requests

sys.path.append("backend")
from goot import CLIENT_ID, CLIENT_SECRET, DATAVERSE_URL, TENANT_ID


def get_token():
    """Obtener token de autenticacion"""
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


def ver_todos_chatbots():
    """Ver todos los chatbots"""
    token = get_token()
    if not token:
        print("Error: No se pudo obtener token")
        return

    # Consultar TODOS los chatbots (activos e inactivos)
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_chatbots"
    url += "?$select=cr321_chatbotid,cr321_name,cr321_active,cr321_elemento1,cr321_elemento2,cr321_elemento3,cr321_grupoid"
    url += "&$orderby=cr321_name asc"

    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    print("\n" + "=" * 70)
    print("TODOS LOS CHATBOTS EN DATAVERSE")
    print("=" * 70)

    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 200:
        data = response.json()
        chatbots = data.get("value", [])

        if not chatbots:
            print("\nNO HAY CHATBOTS EN LA TABLA")
            return

        activos = [cb for cb in chatbots if cb.get("cr321_active")]
        inactivos = [cb for cb in chatbots if not cb.get("cr321_active")]

        print(f"\nTotal: {len(chatbots)} chatbots")
        print(f"  - Activos: {len(activos)}")
        print(f"  - Inactivos: {len(inactivos)}")

        if activos:
            print("\n" + "=" * 70)
            print("CHATBOTS ACTIVOS:")
            print("=" * 70)

            for i, chatbot in enumerate(activos, 1):
                es_primero = i == 1
                print(f"\n[{i}] {chatbot.get('cr321_name')}")
                if es_primero:
                    print("    >>> ESTE ES EL QUE SE USA ACTUALMENTE <<<")
                print(f"    ID: {chatbot.get('cr321_chatbotid')}")
                print(f"    Estado: ACTIVO")

                elementos = [
                    chatbot.get("cr321_elemento1"),
                    chatbot.get("cr321_elemento2"),
                    chatbot.get("cr321_elemento3"),
                ]

                opciones = [e for e in elementos if e and e.strip()]
                print(f"    Opciones configuradas: {len(opciones)}")

                for idx, elem in enumerate(opciones, 1):
                    print(f"      {idx}. {elem}")

        if inactivos:
            print("\n" + "=" * 70)
            print("CHATBOTS INACTIVOS:")
            print("=" * 70)

            for i, chatbot in enumerate(inactivos, 1):
                print(f"\n[{i}] {chatbot.get('cr321_name')}")
                print(f"    ID: {chatbot.get('cr321_chatbotid')}")
                print(f"    Estado: INACTIVO")

                elementos = [
                    chatbot.get("cr321_elemento1"),
                    chatbot.get("cr321_elemento2"),
                    chatbot.get("cr321_elemento3"),
                ]

                opciones = [e for e in elementos if e and e.strip()]
                print(f"    Opciones configuradas: {len(opciones)}")

                for idx, elem in enumerate(opciones, 1):
                    print(f"      {idx}. {elem}")

        print("\n" + "=" * 70)
        print("COMO CAMBIAR EL MENU:")
        print("=" * 70)
        print("\n1. Para usar otro chatbot:")
        print("   - Desactivar el actual (BOT1 -> cr321_active = false)")
        print("   - O renombrar el deseado para que quede primero alfabeticamente")
        print("\n2. Para editar opciones de un chatbot:")
        print("   - Ir a Dataverse -> cr321_chatbots")
        print("   - Editar campos cr321_elemento1 hasta cr321_elemento5")
        print("   - Los cambios se aplican en maximo 5 minutos")
        print("   - O reiniciar el backend para aplicar inmediatamente")

    else:
        print(f"Error HTTP: {response.status_code}")
        print(response.text)


if __name__ == "__main__":
    ver_todos_chatbots()
