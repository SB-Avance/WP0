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
from config import API_BASE_URL

# API_BASE_URL se carga automáticamente desde config.py
# Para cambiar entre LOCAL/AZURE, editar variable ENVIRONMENT en config.py
# o establecer variable de entorno: set ENVIRONMENT=AZURE

class WhatsAppAPI:
    def __init__(self, base_url, token=None):
        self.base_url = base_url
        self.token = token
        print(f"[API] Inicializado con base URL: {base_url}")
    
    def set_token(self, token):
        self.token = token
    
    def get_conversations(self):
        try:
            url = f"{self.base_url}/api/conversations"
            headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
            print(f"[API] GET {url}")
            response = requests.get(url, headers=headers, timeout=10)
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
            url = f"{self.base_url}/api/messages/{phone}"
            headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
            print(f"[API] GET {url}")
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get("messages", [])
            else:
                return []
        except Exception as e:
            print(f"Error al obtener mensajes: {e}")
            return []
    def send_message(self, phone, text, group="GENERAL"):
        try:
            url = f"{self.base_url}/api/send_message"
            headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
            print(f"[API] POST {url}")
            response = requests.post(url, json={"phone": phone, "message": text, "group": group}, headers=headers, timeout=10)
            print(f"[DEBUG] Enviando mensaje a {phone} [Grupo: {group}]: {response.status_code}")
            if response.status_code == 200:
                print(f"[DEBUG] Mensaje enviado exitosamente")
                return True
            else:
                print(f"[DEBUG] Error al enviar: {response.text}")
                return False
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
        url = f"{API_BASE_URL}/api/login"
        print(f"[FRONTEND DEBUG] POST {url}")
        print(f"[FRONTEND DEBUG] Enviando login - Correo: '{correo}', Clave: '{clave}'")
        response = requests.post(url, json={"correo": correo, "clave": clave})
        print(f"[FRONTEND DEBUG] Status code: {response.status_code}")
        print(f"[FRONTEND DEBUG] Response: {response.text}")
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print("Error de conexión:", e)
        return None
def register_api(nombre, correo, clave, rol):
    try:
        url = f"{API_BASE_URL}/register"
        print(f"[FRONTEND DEBUG] POST {url}")
        response = requests.post(url, json={
            "nombre": nombre,
            "correo": correo,
            "clave": clave,
            "rol": rol
        })
        return response.status_code == 200 and response.json().get("success")
    except Exception as e:
        print("Error de conexión:", e)
        return False

def get_users_api(token):
    try:
        url = f"{API_BASE_URL}/api/users"
        print(f"[FRONTEND DEBUG] GET {url}")
        response = requests.get(url, 
                                headers={"Authorization": f"Bearer {token}"},
                                timeout=10)
        if response.status_code == 200:
            return response.json().get("users", [])
        else:
            print(f"Error al obtener usuarios: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        return []


def main(page: ft.Page):
    page.bgcolor = styles.BACKGROUND_COLOR
    page.window.min_width = 320
    page.window.min_height = 480
    page.window.width = 400
    page.window.height = 700
    page.title = "WhatsApp CRM/ERP"

    api = WhatsAppAPI(API_BASE_URL)
    user = {"nombre": None, "rol": None, "correo": None, "token": None}
    current_view = {"value": "login"}  # login, dashboard, chats, users, settings, chat_detail
    conversations = []
    users_list = []
    selected_conversation = {"value": None}
    chat_messages = []
    current_group = {"value": "GENERAL"}  # Grupo por defecto

    # Campos de entrada para login
    correo_input = ft.TextField(label="Correo")
    clave_input = ft.TextField(label="Clave", password=True)

    def on_login(e=None):
        correo = correo_input.value
        clave = clave_input.value
        result = login_api(correo, clave)
        if result and 'token' in result:
            user_data = result.get('user', {})
            token = result.get('token')
            user.update({
                'nombre': user_data.get('nombre'),
                'correo': user_data.get('correo'),
                'rol': user_data.get('rol'),
                'token': token
            })
            api.set_token(token)
            current_view["value"] = "dashboard"
            render()
        else:
            snack = ft.SnackBar(ft.Text("Credenciales incorrectas"), bgcolor=ft.Colors.RED)
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

    def on_logout(e=None):
        # Limpiar datos del usuario
        user.update({
            'nombre': None,
            'correo': None,
            'rol': None,
            'token': None
        })
        api.set_token(None)
        current_view["value"] = "login"
        # Limpiar campos de entrada
        correo_input.value = ""
        clave_input.value = ""
        render()

    def on_group_change(e):
        current_group["value"] = e.control.value
        print(f"[GRUPO] Grupo cambiado a: {current_group['value']}")
        # Mostrar notificación
        snack = ft.SnackBar(ft.Text(f"Grupo cambiado a: {current_group['value']}"), bgcolor=ft.Colors.BLUE)
        page.overlay.append(snack)
        snack.open = True
        page.update()

    def back_to_dashboard(e=None):
        current_view["value"] = "dashboard"
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
        group = current_group["value"]
        success = api.send_message(phone, text, group)
        
        if success:
            # Recargar mensajes después de enviar
            nonlocal chat_messages
            chat_messages = api.get_messages(phone)
            render()
            # Mostrar confirmación
            snack = ft.SnackBar(ft.Text(f"Mensaje enviado [Grupo: {group}]"), bgcolor=ft.Colors.GREEN)
            page.overlay.append(snack)
            snack.open = True
            page.update()
        else:
            # Mostrar error
            snack = ft.SnackBar(ft.Text("Error al enviar mensaje"), bgcolor=ft.Colors.RED)
            page.overlay.append(snack)
            snack.open = True
            page.update()

    def refresh_chat_messages(e=None):
        conv = selected_conversation["value"]
        if conv:
            phone = conv.get("phone")
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
            page.add(ChatDetailView(conv, chat_messages, back_to_chats, send_message_to_chat, refresh_chat_messages, current_group["value"]))
        else:
            # Layout responsivo: sidebar a la izquierda en escritorio, arriba en móvil
            is_mobile = page.width < styles.RESPONSIVE_BREAKPOINT
            sidebar = SidebarView(on_nav_change, on_logout, user.get('nombre'))
            content = None
            if current_view["value"] == "dashboard":
                content = DashboardView(None, on_group_change, current_group["value"])
            elif current_view["value"] == "chats":
                conversations = api.get_conversations()
                content = ChatsView(conversations, open_chat)
            elif current_view["value"] == "users":
                # Obtener lista de usuarios real del backend
                nonlocal users_list
                users_list = get_users_api(user.get('token', ''))
                content = UsersView(users_list, back_to_dashboard)
            elif current_view["value"] == "settings":
                content = SettingsView(back_to_dashboard)
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