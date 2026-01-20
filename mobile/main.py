import flet as ft
import requests
from datetime import datetime
import time

# ============ CONFIGURACIÓN ============
API_BASE_URL = "http://localhost:5000/api"

# ============ SERVICIO API ============
class WhatsAppAPI:
    def __init__(self, base_url):
        self.base_url = base_url
    
    def get_conversations(self):
        """Obtiene lista de conversaciones"""
        try:
            url = f"{self.base_url}/conversations"
            print(f"🔍 Conectando a: {url}")
            
            response = requests.get(url, timeout=10)
            print(f"📊 Status code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                convs = data.get("conversations", [])
                print(f"✅ Conversaciones recibidas: {len(convs)}")
                return convs
            else:
                print(f"❌ Error: {response.text}")
                return []
        except Exception as e:
            print(f"❌ Error al obtener conversaciones: {type(e).__name__}: {e}")
            return []
    
    def get_messages(self, phone):
        """Obtiene mensajes de una conversación"""
        try:
            url = f"{self.base_url}/messages/{phone}"
            print(f"🔍 Obteniendo mensajes para: {phone}")
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                msgs = data.get("messages", [])
                print(f"✅ Mensajes recibidos: {len(msgs)}")
                return msgs
            return []
        except Exception as e:
            print(f"❌ Error al obtener mensajes: {e}")
            return []
    
    def send_message(self, phone, message):
        """Envía un mensaje"""
        try:
            url = f"{self.base_url}/send_message"
            response = requests.post(
                url,
                json={"phone": phone, "message": message},
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Error al enviar mensaje: {e}")
            return False

# ============ APLICACIÓN PRINCIPAL ============
def main(page: ft.Page):
    print("🚀 Iniciando aplicación...")
    
    # 📱 Configuración tamaño celular
    page.window_width = 375
    page.window_height = 812
    page.window_resizable = False
    page.title = "WhatsApp Manager"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    
    # Instancia de API
    api = WhatsAppAPI(API_BASE_URL)
    
    # Estado
    current_conversation = {"phone": "", "name": ""}
    
    # ============ FUNCIONES AUXILIARES ============
    
    def format_timestamp(timestamp):
        """Formatea timestamp"""
        if not timestamp:
            return ""
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return dt.strftime("%H:%M")
        except:
            return ""
    
    # ============ COMPONENTES UI ============
    
    def create_conversation_card(conv):
        """Crea una tarjeta de conversación"""
        def on_click(e):
            open_conversation(conv)
        
        return ft.Container(
            content=ft.Row(
                [
                    ft.CircleAvatar(
                        content=ft.Text(conv["name"][0].upper() if conv["name"] else "?"),
                        bgcolor=ft.Colors.TEAL_400,
                        color=ft.Colors.WHITE,
                        radius=25
                    ),
                    ft.Column(
                        [
                            ft.Text(
                                conv["name"] or "Desconocido",
                                weight=ft.FontWeight.BOLD,
                                size=16
                            ),
                            ft.Text(
                                (conv["last_message"][:50] + "...") if len(conv.get("last_message", "")) > 50 else conv.get("last_message", ""),
                                color=ft.Colors.GREY_700,
                                size=14
                            ),
                            ft.Text(
                                format_timestamp(conv.get("timestamp")),
                                color=ft.Colors.GREY_500,
                                size=12
                            )
                        ],
                        spacing=2,
                        expand=True
                    ),
                    ft.Icon(ft.Icons.CHEVRON_RIGHT, color=ft.Colors.GREY_400)
                ],
                spacing=15
            ),
            padding=15,
            border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.GREY_300)),
            on_click=on_click,
            ink=True
        )
    
    def create_message_bubble(msg):
        """Crea una burbuja de mensaje"""
        is_outgoing = msg.get("direction") == "outgoing"
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        msg.get("body", ""),
                        color=ft.Colors.WHITE if is_outgoing else ft.Colors.BLACK,
                        selectable=True
                    ),
                    ft.Text(
                        format_timestamp(msg.get("timestamp")),
                        size=10,
                        color=ft.Colors.WHITE70 if is_outgoing else ft.Colors.GREY_600
                    )
                ],
                spacing=5,
                tight=True
            ),
            bgcolor=ft.Colors.TEAL_700 if is_outgoing else ft.Colors.GREY_200,
            border_radius=15,
            padding=10,
            margin=ft.margin.only(
                left=50 if is_outgoing else 0,
                right=0 if is_outgoing else 50,
                bottom=5
            ),
            alignment=ft.Alignment(1, 0) if is_outgoing else ft.Alignment(-1, 0)
        )
    
    # ============ VISTAS ============
    
    conversations_list = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=0
    )
    
    messages_list = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=0
    )
    
    message_input = ft.TextField(
        hint_text="Escribe un mensaje...",
        expand=True,
        border_color=ft.Colors.TEAL_700,
        multiline=True,
        max_lines=3
    )
    
    # ============ FUNCIONES DE NAVEGACIÓN ============
    
    def refresh_conversations(e=None):
        """Refresca conversaciones"""
        print("🔄 Refrescando conversaciones...")
        
        conversations_list.controls.clear()
        conversations_list.controls.append(
            ft.Container(
                content=ft.ProgressRing(color=ft.Colors.TEAL_700),
                alignment=ft.Alignment(0, 0),
                padding=20
            )
        )
        page.update()
        print("⏳ Mostrando spinner...")
        
        convs = api.get_conversations()
        print(f"📊 Conversaciones obtenidas: {len(convs)}")
        
        conversations_list.controls.clear()
        
        if convs:
            print(f"✅ Agregando {len(convs)} conversaciones...")
            for i, conv in enumerate(convs):
                print(f"  [{i+1}] {conv.get('name')} - {conv.get('phone')}")
                card = create_conversation_card(conv)
                conversations_list.controls.append(card)
            print("✅ Todas las conversaciones agregadas")
        else:
            print("⚠️ No hay conversaciones")
            conversations_list.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(ft.Icons.CHAT_BUBBLE_OUTLINE, size=60, color=ft.Colors.GREY_400),
                            ft.Text(
                                "No hay conversaciones",
                                color=ft.Colors.GREY_600,
                                size=16
                            ),
                            ft.Text(
                                "El backend está conectado pero no hay datos",
                                color=ft.Colors.GREY_500,
                                size=12
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10
                    ),
                    padding=40,
                    alignment=ft.Alignment(0, 0)
                )
            )
        
        print("🎨 Actualizando página...")
        page.update()
        time.sleep(0.1)
        page.update()
        print("✅ Actualización completa")
    
    def open_conversation(conv):
        """Abre una conversación"""
        print(f"💬 Abriendo conversación con {conv['name']}")
        
        current_conversation["phone"] = conv["phone"]
        current_conversation["name"] = conv["name"]
        
        messages_list.controls.clear()
        messages_list.controls.append(
            ft.Container(
                content=ft.ProgressRing(color=ft.Colors.TEAL_700),
                alignment=ft.Alignment(0, 0),
                padding=20
            )
        )
        
        page.views.clear()
        page.views.append(
            ft.View(
                "/chat",
                [
                    ft.AppBar(
                        leading=ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            icon_color=ft.Colors.WHITE,
                            on_click=lambda _: go_back()
                        ),
                        title=ft.Text(conv["name"] or "Conversación", color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.TEAL_700
                    ),
                    ft.Container(
                        content=messages_list,
                        expand=True,
                        padding=10,
                        bgcolor=ft.Colors.GREY_50
                    ),
                    ft.Container(
                        content=ft.Row(
                            [
                                message_input,
                                ft.IconButton(
                                    icon=ft.Icons.SEND,
                                    icon_color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.TEAL_700,
                                    on_click=lambda _: send_message()
                                )
                            ]
                        ),
                        padding=10,
                        bgcolor=ft.Colors.WHITE,
                        border=ft.border.only(top=ft.BorderSide(1, ft.Colors.GREY_300))
                    )
                ]
            )
        )
        page.update()
        
        msgs = api.get_messages(conv["phone"])
        messages_list.controls.clear()
        
        if msgs:
            for msg in msgs:
                messages_list.controls.append(create_message_bubble(msg))
        else:
            messages_list.controls.append(
                ft.Container(
                    content=ft.Text(
                        "No hay mensajes",
                        color=ft.Colors.GREY_600
                    ),
                    alignment=ft.Alignment(0, 0),
                    padding=20
                )
            )
        
        page.update()
    
    def send_message():
        """Envía un mensaje"""
        if not message_input.value or not current_conversation["phone"]:
            return
        
        text = message_input.value
        message_input.value = ""
        page.update()
        
        success = api.send_message(current_conversation["phone"], text)
        
        if success:
            messages_list.controls.append(create_message_bubble({
                "body": text,
                "direction": "outgoing",
                "timestamp": datetime.now().isoformat()
            }))
            page.update()
            messages_list.scroll_to(offset=-1, duration=100)
            
            snack = ft.SnackBar(
                content=ft.Text("✅ Mensaje enviado"),
                bgcolor=ft.Colors.GREEN_700
            )
            page.overlay.append(snack)
            snack.open = True
            page.update()
        else:
            snack = ft.SnackBar(
                content=ft.Text("❌ Error al enviar mensaje"),
                bgcolor=ft.Colors.RED_700
            )
            page.overlay.append(snack)
            snack.open = True
            message_input.value = text
            page.update()
    
    def go_back():
        """Vuelve a la lista de conversaciones"""
        print("🔙 Volviendo a la lista")
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(
                        title=ft.Text("WhatsApp Manager", color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.TEAL_700,
                        actions=[
                            ft.IconButton(
                                icon=ft.Icons.REFRESH,
                                icon_color=ft.Colors.WHITE,
                                on_click=refresh_conversations
                            )
                        ]
                    ),
                    conversations_list
                ]
            )
        )
        page.update()
    
    # ============ INICIALIZACIÓN ============
    
    print("🎨 Configurando interfaz inicial...")
    
    page.views.append(
        ft.View(
            "/",
            [
                ft.AppBar(
                    title=ft.Text("WhatsApp Manager", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.TEAL_700,
                    actions=[
                        ft.IconButton(
                            icon=ft.Icons.REFRESH,
                            icon_color=ft.Colors.WHITE,
                            on_click=refresh_conversations
                        )
                    ]
                ),
                conversations_list
            ]
        )
    )
    
    print("✅ Interfaz configurada")
    page.update()
    
    print("📲 Cargando conversaciones iniciales...")
    time.sleep(0.2)
    
    refresh_conversations()
    
    print("✅ Aplicación iniciada completamente")

# ============ EJECUTAR APP ============
if __name__ == "__main__":
    print("=" * 50)
    print("🎯 WhatsApp Manager - Iniciando...")
    print("=" * 50)
    ft.app(target=main)