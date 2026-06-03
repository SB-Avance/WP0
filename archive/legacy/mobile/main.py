import time
from datetime import datetime

import flet as ft
import requests
from assets import styles
from components.chat_detail import ChatDetailView
from components.chatbots import ChatbotsView
from components.chats import ChatsView
from components.dashboard import DashboardView
from components.login import LoginView
from components.settings import SettingsView
from components.sidebar import SidebarView
from components.templates import TemplatesView
from components.users import UsersView
from components.whatsapp_accounts import WhatsAppAccountsView
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

    def get_user_groups(self, user_id):
        """Obtener grupos permitidos para un usuario específico"""
        try:
            url = f"{self.base_url}/api/usuario-grupos/usuario/{user_id}"
            headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
            print(f"[API] GET {url}")
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                grupos = data.get("grupos", [])
                print(
                    f"[API] Grupos del usuario {user_id}: {[g.get('nombre') for g in grupos]}"
                )
                return grupos
            else:
                print(f"[API] Error al obtener grupos: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error al obtener grupos del usuario: {e}")
            return []

    def get_all_groups(self):
        """Obtener todos los grupos disponibles"""
        try:
            url = f"{self.base_url}/api/grupos"
            headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
            print(f"[API] GET {url}")
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                # Extraer solo los nombres de los grupos
                return [g.get("nombre", "") for g in data.get("grupos", [])]
            else:
                return []
        except Exception as e:
            print(f"Error al obtener todos los grupos: {e}")
            return []

    def get_conversations(self, group_filter=None):
        try:
            url = f"{self.base_url}/api/conversations"
            if group_filter and group_filter != "TODOS":
                url += f"?group={group_filter}"
            headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
            print(f"[API] GET {url}")
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get("conversations", []), data.get("groups", [])
            else:
                return [], []
        except Exception as e:
            print(f"Error al obtener conversaciones: {e}")
            return [], []

    def get_messages(self, phone, group_filter=None):
        try:
            url = f"{self.base_url}/api/messages/{phone}"
            if group_filter and group_filter != "TODOS":
                url += f"?group={group_filter}"
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
            response = requests.post(
                url,
                json={"phone": phone, "message": text, "group": group},
                headers=headers,
                timeout=10,
            )
            print(
                f"[DEBUG] Enviando mensaje a {phone} [Grupo: {group}]: {response.status_code}"
            )
            if response.status_code == 200:
                print(f"[DEBUG] Mensaje enviado exitosamente")
                return True
            else:
                print(f"[DEBUG] Error al enviar: {response.text}")
                return False
        except Exception as e:
            print(f"Error al enviar mensaje: {e}")
            return False

    def get_users(self):
        """Obtener lista de usuarios"""
        try:
            url = f"{self.base_url}/api/users"
            headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
            print(f"[API] GET {url}")
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error {response.status_code}: {response.text}")
        except Exception as e:
            print(f"Error al obtener usuarios: {e}")
            raise e

    def create_user(self, user_data):
        """Crear nuevo usuario"""
        try:
            url = f"{self.base_url}/api/users"
            headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
            print(f"[API] POST {url}")
            response = requests.post(url, json=user_data, headers=headers, timeout=10)
            if response.status_code in [200, 201]:
                return response.json()
            else:
                raise Exception(f"Error {response.status_code}: {response.text}")
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            raise e

    def update_user(self, user_id, user_data):
        """Actualizar usuario existente"""
        try:
            url = f"{self.base_url}/api/users/{user_id}"
            headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
            print(f"[API] PATCH {url}")
            response = requests.patch(url, json=user_data, headers=headers, timeout=10)
            if response.status_code in [200, 204]:
                return response.json() if response.text else {"success": True}
            else:
                raise Exception(f"Error {response.status_code}: {response.text}")
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
            raise e

    def delete_user(self, user_id):
        """Eliminar usuario"""
        try:
            url = f"{self.base_url}/api/users/{user_id}"
            headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
            print(f"[API] DELETE {url}")
            response = requests.delete(url, headers=headers, timeout=10)
            if response.status_code in [200, 204]:
                return {"success": True}
            else:
                raise Exception(f"Error {response.status_code}: {response.text}")
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
            raise e


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
        print(f"[FRONTEND DEBUG] Enviando login - Correo: '{correo}' .Clave: '{clave}'")
        response = requests.post(
            url, json={"correo": correo, "clave": clave}, timeout=30
        )
        print(f"[FRONTEND DEBUG] Status code: {response.status_code}")
        #        print(f"[FRONTEND DEBUG] Response: {response.text}")
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        elif response.status_code == 503:
            return {
                "success": False,
                "error": "service_unavailable",
                "message": "El servidor no está disponible. Por favor, intente más tarde.",
            }
        elif response.status_code in [401, 403]:
            return {
                "success": False,
                "error": "invalid_credentials",
                "message": "Credenciales incorrectas",
            }
        else:
            return {
                "success": False,
                "error": "unknown",
                "message": f"Error del servidor ({response.status_code})",
            }
    except requests.exceptions.Timeout:
        print("Error: Timeout al conectar con el servidor")
        return {
            "success": False,
            "error": "timeout",
            "message": "Tiempo de espera agotado. Verifique su conexión.",
        }
    except requests.exceptions.ConnectionError as e:
        print("Error de conexión:", e)
        return {
            "success": False,
            "error": "connection",
            "message": "No se puede conectar con el servidor. Verifique su conexión.",
        }
    except Exception as e:
        print("Error inesperado:", e)
        return {
            "success": False,
            "error": "unknown",
            "message": "Error inesperado al conectar",
        }


def register_api(nombre, correo, clave, rol):
    try:
        url = f"{API_BASE_URL}/register"
        print(f"[FRONTEND DEBUG] POST {url}")
        response = requests.post(
            url, json={"nombre": nombre, "correo": correo, "clave": clave, "rol": rol}
        )
        return response.status_code == 200 and response.json().get("success")
    except Exception as e:
        print("Error de conexión:", e)
        return False


def get_users_api(token):
    try:
        url = f"{API_BASE_URL}/api/users"
        print(f"[FRONTEND DEBUG] GET {url}")
        response = requests.get(
            url, headers={"Authorization": f"Bearer {token}"}, timeout=10
        )
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
    page.title = "WhatsApp CRM/ERP"

    # Configurar para modo móvil
    page.padding = 0
    page.spacing = 0
    page.scroll = ft.ScrollMode.AUTO

    # Configurar tamaño de ventana para móvil (iPhone X) - solo funciona en FLET_APP
    page.window.width = 375
    page.window.height = 812
    page.window.min_width = 375
    page.window.min_height = 667
    page.window.max_width = 375
    page.window.max_height = 812
    page.window.max_height = 812

    api = WhatsAppAPI(API_BASE_URL)
    user = {"id": None, "nombre": None, "rol": None, "correo": None, "token": None}
    current_view = {
        "value": "login"
    }  # login, dashboard, chats, chatbots, users, settings, chat_detail
    conversations = []
    users_list = []
    selected_conversation = {"value": None}
    chat_messages = []
    current_group = {"value": "GENERAL"}  # Grupo por defecto
    user_groups_cache = {"value": None}  # Cache de grupos del usuario

    # Campos de entrada para login
    correo_input = ft.TextField(label="Correo")
    clave_input = ft.TextField(label="Clave", password=True)

    def on_login(e=None):
        correo = correo_input.value
        clave = clave_input.value
        result = login_api(correo, clave)
        if result and result.get("success") and "data" in result:
            data = result["data"]
            user_data = data.get("user", {})
            token = data.get("token")
            user.update(
                {
                    "id": user_data.get("id"),
                    "nombre": user_data.get("nombre"),
                    "correo": user_data.get("correo"),
                    "rol": user_data.get("rol"),
                    "token": token,
                }
            )
            api.set_token(token)
            current_view["value"] = "chats"
            render()
        else:
            # Mostrar mensaje de error específico
            error_msg = (
                result.get("message", "Error desconocido")
                if result
                else "Error de conexión"
            )
            error_color = (
                ft.Colors.ORANGE
                if result and result.get("error") == "service_unavailable"
                else ft.Colors.RED
            )
            snack = ft.SnackBar(ft.Text(error_msg), bgcolor=error_color)
            page.overlay.append(snack)
            snack.open = True
            page.update()

    def on_nav_change(e):
        """Navegación simplificada con menú fijo"""
        idx = e.control.selected_index
        user_rol = user.get("rol")

        print(f"[NAV] Índice seleccionado: {idx}, Rol: {user_rol}")

        # Menú fijo:
        # - 0: Chats (todos)
        # Si administrador:
        #   - 1: Chatbots
        #   - 2: Usuarios
        #   - 3: Templates
        #   - 4: Cuentas WA
        #   - 5: Salir
        # Si usuario:
        #   - 1: Salir

        if idx == 0:
            # Chats (visible para todos)
            current_view["value"] = "chats"
        elif user_rol == "administrador":
            if idx == 1:
                current_view["value"] = "chatbots"
            elif idx == 2:
                current_view["value"] = "users"
            elif idx == 3:
                current_view["value"] = "templates"
            elif idx == 4:
                current_view["value"] = "whatsapp_accounts"
            elif idx == 5:
                # Salir
                on_logout()
                return
        else:
            # Usuario normal
            if idx == 1:
                # Salir
                on_logout()
                return

        render()

    def on_logout(e=None):
        # Limpiar datos del usuario
        user.update(
            {"id": None, "nombre": None, "correo": None, "rol": None, "token": None}
        )
        api.set_token(None)
        current_view["value"] = "login"
        # Limpiar cache de grupos
        user_groups_cache["value"] = None
        # Limpiar campos de entrada
        correo_input.value = ""
        clave_input.value = ""
        render()

    def on_group_change(e):
        current_group["value"] = e.control.value
        print(f"[GRUPO] Grupo cambiado a: {current_group['value']}")
        # Mostrar notificación
        snack = ft.SnackBar(
            ft.Text(f"Grupo cambiado a: {current_group['value']}"),
            bgcolor=ft.Colors.BLUE,
        )
        page.overlay.append(snack)
        snack.open = True
        page.update()

    def back_to_dashboard(e=None):
        """Volver a la vista principal de chats"""
        current_view["value"] = "chats"
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
            # Esperar un momento para que el mensaje se guarde en Dataverse
            time.sleep(1)
            # Recargar mensajes después de enviar
            nonlocal chat_messages
            chat_messages = api.get_messages(phone)
            render()
            # Mostrar confirmación
            snack = ft.SnackBar(
                ft.Text(f"Mensaje enviado [Grupo: {group}]"), bgcolor=ft.Colors.GREEN
            )
            page.overlay.append(snack)
            snack.open = True
            page.update()
        else:
            # Mostrar error
            snack = ft.SnackBar(
                ft.Text("Error al enviar mensaje"), bgcolor=ft.Colors.RED
            )
            page.overlay.append(snack)
            snack.open = True
            page.update()

    def refresh_chat_messages(e=None):
        conv = selected_conversation["value"]
        if conv:
            phone = conv.get("phone")
            group = conv.get("group", current_group["value"])
            nonlocal chat_messages
            chat_messages = api.get_messages(phone, group)
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
            page.add(
                ChatDetailView(
                    conv,
                    chat_messages,
                    back_to_chats,
                    send_message_to_chat,
                    refresh_chat_messages,
                    current_group["value"],
                )
            )
        else:
            # Layout con sidebar siempre a la izquierda (modo iPhone)
            sidebar = SidebarView(
                on_nav_change, on_logout, user.get("nombre"), user.get("rol")
            )

            content = None

            if current_view["value"] == "chats":
                # Obtener conversaciones
                conversations, available_groups = api.get_conversations(
                    current_group["value"]
                )

                # Filtrar conversaciones según grupos permitidos del usuario
                if user.get("rol") != "administrador":
                    user_id = user.get("id")
                    if user_id:
                        # Usar cache si existe, sino consultar API
                        if user_groups_cache["value"] is None:
                            print(
                                f"[FILTRO] Cargando grupos del usuario {user.get('nombre')}..."
                            )
                            user_groups = api.get_user_groups(user_id)
                            user_groups_cache["value"] = user_groups
                        else:
                            print(f"[FILTRO] Usando cache de grupos")
                            user_groups = user_groups_cache["value"]

                        # Extraer nombres de grupos directamente desde backend (con lookups)
                        user_group_names = [
                            g.get("nombre") for g in user_groups if g.get("nombre")
                        ]

                        # Si el usuario tiene grupos asignados, filtrar
                        if user_group_names:
                            print(
                                f"[FILTRO] Filtrando {len(conversations)} conversaciones para grupos: {user_group_names}"
                            )
                            conversations = [
                                c
                                for c in conversations
                                if c.get("group") in user_group_names
                            ]
                            print(
                                f"[FILTRO] Resultado: {len(conversations)} conversaciones visibles"
                            )
                        else:
                            print(
                                f"[FILTRO] Usuario sin grupos - mostrando todas las conversaciones"
                            )
                else:
                    print(
                        f"[FILTRO] Administrador - mostrando todas las conversaciones"
                    )

                content = ChatsView(
                    conversations,
                    open_chat,
                    current_group["value"],
                    available_groups,
                    on_group_change,
                )
            elif current_view["value"] == "users":
                # Solo administradores pueden ver usuarios
                if user.get("rol") == "administrador":
                    content = UsersView(
                        back_to_dashboard, API_BASE_URL, user.get("token", "")
                    )
                else:
                    content = ft.Container(
                        ft.Text(
                            "No tienes permisos para acceder a esta sección",
                            size=18,
                            color=ft.colors.RED,
                        ),
                        padding=20,
                    )
            elif current_view["value"] == "chatbots":
                # Solo administradores pueden ver chatbots
                if user.get("rol") == "administrador":
                    content = ChatbotsView(
                        back_to_dashboard, API_BASE_URL, user.get("token", "")
                    )
                else:
                    content = ft.Container(
                        ft.Text(
                            "No tienes permisos para acceder a esta sección",
                            size=18,
                            color=ft.colors.RED,
                        ),
                        padding=20,
                    )
            elif current_view["value"] == "templates":
                # Solo administradores pueden ver templates
                if user.get("rol") == "administrador":
                    content = TemplatesView(
                        back_to_dashboard, API_BASE_URL, user.get("token", "")
                    )
                else:
                    content = ft.Container(
                        ft.Text(
                            "No tienes permisos para acceder a esta sección",
                            size=18,
                            color=ft.colors.RED,
                        ),
                        padding=20,
                    )
            elif current_view["value"] == "whatsapp_accounts":
                # Solo administradores pueden ver cuentas WhatsApp
                if user.get("rol") == "administrador":
                    content = WhatsAppAccountsView(
                        back_to_dashboard, API_BASE_URL, user.get("token", "")
                    )
                else:
                    content = ft.Container(
                        ft.Text(
                            "No tienes permisos para acceder a esta sección",
                            size=18,
                            color=ft.colors.RED,
                        ),
                        padding=20,
                    )
            elif current_view["value"] == "settings":
                content = SettingsView(back_to_dashboard)

            # Siempre usar layout horizontal (sidebar + content)
            page.add(
                ft.Row(
                    [
                        sidebar,
                        ft.Container(
                            content, expand=True, alignment=ft.alignment.top_left
                        ),
                    ],
                    expand=True,
                    spacing=0,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                )
            )
        page.update()

    page.on_resized = lambda e: render()
    render()


if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, host="192.168.22.144", port=8501)
