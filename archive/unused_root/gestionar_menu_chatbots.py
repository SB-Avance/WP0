"""
Script para gestionar qué chatbot se muestra en el menú de WhatsApp
Permite activar/desactivar chatbots fácilmente
"""

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


def listar_chatbots():
    """Lista todos los chatbots"""
    token = get_token()
    if not token:
        print("❌ Error: No se pudo obtener token")
        return None

    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_chatbots"
    url += "?$select=cr321_chatbotid,cr321_name,cr321_active,cr321_elemento1,cr321_elemento2,cr321_elemento3"
    url += "&$orderby=cr321_name asc"

    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 200:
        data = response.json()
        chatbots = data.get("value", [])
        return chatbots
    else:
        print(f"❌ Error HTTP: {response.status_code}")
        return None


def activar_chatbot(chatbot_id):
    """Activa un chatbot específico"""
    token = get_token()
    if not token:
        print("❌ Error: No se pudo obtener token")
        return False

    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_chatbots({chatbot_id})"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    payload = {"cr321_active": True}

    response = requests.patch(url, json=payload, headers=headers, timeout=10)

    if response.status_code == 204:
        return True
    else:
        print(f"❌ Error HTTP: {response.status_code}")
        return False


def desactivar_chatbot(chatbot_id):
    """Desactiva un chatbot específico"""
    token = get_token()
    if not token:
        print("❌ Error: No se pudo obtener token")
        return False

    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_chatbots({chatbot_id})"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    payload = {"cr321_active": False}

    response = requests.patch(url, json=payload, headers=headers, timeout=10)

    if response.status_code == 204:
        return True
    else:
        print(f"❌ Error HTTP: {response.status_code}")
        return False


def mostrar_menu():
    """Muestra el menú interactivo"""
    print("\n" + "=" * 70)
    print("     GESTIÓN DE MENÚ DE CHATBOTS")
    print("=" * 70)

    chatbots = listar_chatbots()
    if not chatbots:
        return

    activos = [cb for cb in chatbots if cb.get("cr321_active")]
    inactivos = [cb for cb in chatbots if not cb.get("cr321_active")]

    print(f"\n📊 ESTADO ACTUAL:")
    print(f"   Total: {len(chatbots)} chatbots")
    print(f"   ✅ Activos: {len(activos)}")
    print(f"   ⛔ Inactivos: {len(inactivos)}")

    if activos:
        print(f"\n✅ CHATBOTS ACTIVOS (SE MUESTRAN EN EL MENÚ):")
        for i, cb in enumerate(activos, 1):
            print(f"\n  [{i}] {cb.get('cr321_name')}")
            elementos = [
                cb.get("cr321_elemento1"),
                cb.get("cr321_elemento2"),
                cb.get("cr321_elemento3"),
            ]
            opciones = [e for e in elementos if e and e.strip()]
            for idx, elem in enumerate(opciones, 1):
                print(f"      {idx}. {elem}")

    if inactivos:
        print(f"\n⛔ CHATBOTS INACTIVOS (NO SE MUESTRAN):")
        for i, cb in enumerate(inactivos, 1):
            print(f"  [{i}] {cb.get('cr321_name')}")

    print("\n" + "=" * 70)
    print("OPCIONES:")
    print("=" * 70)
    print("1. Activar solo 'Soporte' (Solicitud Ticket)")
    print("2. Activar solo 'Ventas' (Cotizaciones)")
    print("3. Activar solo 'Informacion'")
    print("4. Activar TODOS")
    print("5. Gestión manual (activar/desactivar específicos)")
    print("0. Salir")
    print("=" * 70)

    return chatbots


def main():
    """Función principal"""
    while True:
        chatbots = mostrar_menu()
        if not chatbots:
            break

        try:
            opcion = input("\n👉 Elige una opción: ").strip()

            if opcion == "0":
                print("\n✅ ¡Hasta luego!")
                break
            elif opcion == "1":
                # Activar solo Soporte
                print("\n🔄 Configurando: Solo 'Soporte' activo...")
                for cb in chatbots:
                    if cb.get("cr321_name") == "Soporte":
                        if activar_chatbot(cb["cr321_chatbotid"]):
                            print(f"  ✅ Activado: Soporte")
                    else:
                        if desactivar_chatbot(cb["cr321_chatbotid"]):
                            print(f"  ⛔ Desactivado: {cb.get('cr321_name')}")
                print("\n✅ ¡Configuración completada!")
                print("💡 El menú ahora mostrará solo las opciones de Soporte:")
                print("   1. Solicitud Ticket")
                print("   2. Estado Ticket")
                print("   3. Solicitar atención de agente")

            elif opcion == "2":
                # Activar solo Ventas
                print("\n🔄 Configurando: Solo 'Ventas' activo...")
                for cb in chatbots:
                    if cb.get("cr321_name") == "Ventas":
                        if activar_chatbot(cb["cr321_chatbotid"]):
                            print(f"  ✅ Activado: Ventas")
                    else:
                        if desactivar_chatbot(cb["cr321_chatbotid"]):
                            print(f"  ⛔ Desactivado: {cb.get('cr321_name')}")
                print("\n✅ ¡Configuración completada!")

            elif opcion == "3":
                # Activar solo Informacion
                print("\n🔄 Configurando: Solo 'Informacion' activo...")
                for cb in chatbots:
                    if cb.get("cr321_name") == "Informacion":
                        if activar_chatbot(cb["cr321_chatbotid"]):
                            print(f"  ✅ Activado: Informacion")
                    else:
                        if desactivar_chatbot(cb["cr321_chatbotid"]):
                            print(f"  ⛔ Desactivado: {cb.get('cr321_name')}")
                print("\n✅ ¡Configuración completada!")

            elif opcion == "4":
                # Activar todos
                print("\n🔄 Activando TODOS los chatbots...")
                for cb in chatbots:
                    if activar_chatbot(cb["cr321_chatbotid"]):
                        print(f"  ✅ Activado: {cb.get('cr321_name')}")
                print("\n✅ ¡Todos los chatbots activados!")

            elif opcion == "5":
                # Gestión manual
                print("\n" + "=" * 70)
                print("GESTIÓN MANUAL")
                print("=" * 70)
                for i, cb in enumerate(chatbots, 1):
                    estado = "✅ ACTIVO" if cb.get("cr321_active") else "⛔ INACTIVO"
                    print(f"{i}. {cb.get('cr321_name')} - {estado}")

                num = input(
                    "\n👉 Número de chatbot a cambiar (0 para cancelar): "
                ).strip()
                try:
                    num_int = int(num)
                    if num_int == 0:
                        continue
                    if 1 <= num_int <= len(chatbots):
                        cb = chatbots[num_int - 1]
                        if cb.get("cr321_active"):
                            if desactivar_chatbot(cb["cr321_chatbotid"]):
                                print(f"\n⛔ Desactivado: {cb.get('cr321_name')}")
                        else:
                            if activar_chatbot(cb["cr321_chatbotid"]):
                                print(f"\n✅ Activado: {cb.get('cr321_name')}")
                    else:
                        print("\n❌ Número inválido")
                except ValueError:
                    print("\n❌ Opción inválida")

            else:
                print("\n❌ Opción inválida")

            input("\n📌 Presiona Enter para continuar...")

        except KeyboardInterrupt:
            print("\n\n✅ ¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("\n📌 Presiona Enter para continuar...")


if __name__ == "__main__":
    main()
