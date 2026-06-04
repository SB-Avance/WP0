"""
Ver el menu que se esta cargando actualmente
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


def ver_menu():
    """Ver el menu actual"""
    token = get_token()
    if not token:
        print("Error: No se pudo obtener token")
        return

    # Consultar chatbots activos
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_chatbots"
    url += "?$select=cr321_chatbotid,cr321_name,cr321_active,cr321_elemento1,cr321_elemento2,cr321_elemento3,cr321_elemento4,cr321_elemento5"
    url += "&$filter=cr321_active eq true"
    url += "&$orderby=cr321_name asc"

    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    print("\n" + "=" * 70)
    print("MENU ACTUAL DE WHATSAPP (desde cr321_chatbots)")
    print("=" * 70)

    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 200:
        data = response.json()
        chatbots = data.get("value", [])

        if not chatbots:
            print("\nNO HAY CHATBOTS ACTIVOS")
            print("El sistema usara el menu por defecto hardcodeado")
            return

        # El primer chatbot es el que se usa
        chatbot = chatbots[0]

        print(f"\nChatbot activo: {chatbot.get('cr321_name')}")
        print(f"ID: {chatbot.get('cr321_chatbotid')}")
        print("\nMENU QUE SE ENVIA A WHATSAPP:")
        print("-" * 70)
        print("Bienvenido! Por favor seleccione una opcion:\n")

        idx = 1
        elementos = [
            chatbot.get("cr321_elemento1"),
            chatbot.get("cr321_elemento2"),
            chatbot.get("cr321_elemento3"),
            chatbot.get("cr321_elemento4"),
            chatbot.get("cr321_elemento5"),
        ]

        for elemento in elementos:
            if elemento and elemento.strip():
                print(f"{idx}. {elemento}")
                idx += 1

        print("-" * 70)
        print(f"\nTotal de opciones: {idx - 1}")

        if len(chatbots) > 1:
            print(f"\nNOTA: Hay {len(chatbots)} chatbots activos.")
            print("Actualmente se usa el primero (orden alfabetico por nombre):")
            for i, cb in enumerate(chatbots, 1):
                print(f"  [{i}] {cb.get('cr321_name')}")
            print("\nPara usar otro chatbot:")
            print("  1. Desactiva el actual en Dataverse (cr321_active = false)")
            print(
                "  2. O cambia el nombre del que quieres usar (para que quede primero)"
            )

    else:
        print(f"Error HTTP: {response.status_code}")
        print(response.text)


if __name__ == "__main__":
    ver_menu()
