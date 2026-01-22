


import flet as ft
from components.login import LoginView
from components.dashboard import DashboardView
from components.sidebar import SidebarView
from components.chats import ChatsView
from components.chat_detail import ChatDetailView
from components.users import UsersView
from components.settings import SettingsView
from assets import styles
import requests
from datetime import datetime

API_BASE_URL = "https://whatsapp-flask-app-f4gsb7dhhybcg6f6.scm.eastus-01.azurewebsites.net/api"

class WhatsAppAPI:
    def __init__(self, base_url):
        self.base_url = base_url
    def get_conversations(self):
        try:
            url = f"{self.base_url}/conversations"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get("conversations", [])
            else:
                return []
        except Exception as e:
            print(f"Error al obtener conversaciones: {e}")
            return []
    def get_messages(self, phone):
        try:
            url = f"{self.base_url}/messages/{phone}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get("messages", [])
            else:
                return []
        except Exception as e:
            print(f"Error al obtener mensajes: {e}")
            return []
    def send_message(self, phone, text):
        try:
            url = f"{self.base_url}/messages/{phone}"
            response = requests.post(url, json={"body": text}, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"Error al enviar mensaje: {e}")
            return False

def format_timestamp(ts):
    try:
        dt = datetime.fromisoformat(ts)
        return dt.strftime("%d/%m/%Y %H:%M")
    except Exception:
        return ts

def login_api(correo, clave):
    try:
        response = requests.post("https://whatsapp-flask-app-f4gsb7dhhybcg6f6.scm.eastus-01.azurewebsites.net/login", json={"correo": correo, "clave": clave})
        if response.status_code == 200 and response.json().get("success"):
            return response.json()
        else:
            return None
    except Exception as e:
        print("Error de conexión:", e)
        return None

def register_api(nombre, correo, clave, rol):
    try:
        response = requests.post("https://whatsapp-flask-app-f4gsb7dhhybcg6f6.scm.eastus-01.azurewebsites.net/register", json={
            "nombre": nombre,
            "correo": correo,
            "clave": clave,
            "rol": rol
        })
        return response.status_code == 200 and response.json().get("success")
    except Exception as e:
        print("Error de conexión:", e)
        return False


def main(page: ft.Page):
    page.bgcolor = styles.BACKGROUND_COLOR
    page.window.min_width = 320
    page.window.min_height = 480
    page.window.width = 400
    page.window.height = 700
    page.title = "WhatsApp CRM/ERP"

    api = WhatsAppAPI(API_BASE_URL)
    user = {"nombre": None, "rol": None, "correo": None}
    current_view = {"value": "login"}  # login, dashboard, chats, users, settings, chat_detail
    conversations = []
    users_list = []
    selected_conversation = {"value": None}
    chat_messages = []

    # Campos de entrada para login
    correo_input = ft.TextField(label="Correo")
    clave_input = ft.TextField(label="Clave", password=True)

    def on_login(e=None):
        correo = correo_input.value
        clave = clave_input.value
        u = login_api(correo, clave)
        if u:
            user.update(u)
            current_view["value"] = "dashboard"
            render()
        else:
            snack = ft.SnackBar(ft.Text("Credenciales incorrectas"), bgcolor=ft.colors.RED)
            page.overlay.append(snack)
            snack.open = True
            page.update()

    def on_nav_change(e):
        idx = e.control.selected_index
        if idx == 0:
            current_view["value"] = "chats"
        elif idx == 1:
            current_view["value"] = "users"
        elif idx == 2:
            current_view["value"] = "settings"
        render()

    def open_chat(conv):
        selected_conversation["value"] = conv
        # Obtener mensajes del chat seleccionado
        phone = conv.get("phone")
        nonlocal chat_messages
        chat_messages = api.get_messages(phone)
        current_view["value"] = "chat_detail"
        render()

    def send_message_to_chat(text):
        conv = selected_conversation["value"]
        phone = conv.get("phone")
        api.send_message(phone, text)
        # Recargar mensajes después de enviar
        nonlocal chat_messages
        chat_messages = api.get_messages(phone)
        render()

    def back_to_chats(e=None):
        current_view["value"] = "chats"
        render()

    def render():
        page.clean()
        if current_view["value"] == "login":
            page.add(LoginView(correo_input, clave_input, on_login))
        elif current_view["value"] == "chat_detail":
            conv = selected_conversation["value"]
            page.add(ChatDetailView(conv, chat_messages, back_to_chats, send_message_to_chat))
        else:
            # Layout responsivo: sidebar a la izquierda en escritorio, arriba en móvil
            is_mobile = page.width < styles.RESPONSIVE_BREAKPOINT
            sidebar = SidebarView(on_nav_change)
            content = None
            if current_view["value"] == "dashboard":
                content = DashboardView()
            elif current_view["value"] == "chats":
                conversations = api.get_conversations()
                content = ChatsView(conversations, open_chat)
            elif current_view["value"] == "users":
                # Aquí deberías obtener la lista de usuarios real
                users_list = [{"correo": "demo@demo.com"}]
                content = UsersView(users_list)
            elif current_view["value"] == "settings":
                content = SettingsView()
            if is_mobile:
                page.add(sidebar)
                page.add(content)
            else:
                page.add(
                    ft.Row([
                        sidebar,
                        ft.VerticalDivider(width=1),
                        ft.Container(content, expand=True)
                    ], expand=True)
                )
        page.update()

    page.on_resized = lambda e: render()
    render()
if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, host="0.0.0.0", port=8501)