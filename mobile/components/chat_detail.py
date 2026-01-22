# ChatDetailView: muestra los mensajes de una conversación y permite responder
import flet as ft

def ChatDetailView(conversation, messages, on_back, on_send):
    name = conversation.get("name", "Desconocido")
    phone = conversation.get("phone", "")
    # Campo de entrada para el mensaje
    message_input = ft.TextField(hint_text="Escribe un mensaje...", expand=True)
    def send_click(e):
        if message_input.value.strip():
            on_send(message_input.value)
            message_input.value = ""
            message_input.update()
    return ft.Column([
        ft.Row([
            ft.IconButton(ft.icons.ARROW_BACK, on_click=on_back),
            ft.Text(f"{name} ({phone})", weight=ft.FontWeight.BOLD, size=18),
        ], alignment=ft.MainAxisAlignment.START),
        ft.Divider(),
        ft.Container(
            ft.ListView([
                ft.Container(
                    ft.Text(f"{msg['body']}", size=15, color=ft.colors.BLACK if msg['direction']=='incoming' else ft.colors.BLUE_900),
                    alignment=ft.alignment.center_left if msg['direction']=='incoming' else ft.alignment.center_right,
                    padding=ft.padding.only(left=8, right=8, top=4, bottom=4),
                    margin=ft.margin.only(bottom=4),
                    bgcolor=ft.colors.GREY_100 if msg['direction']=='incoming' else ft.colors.BLUE_50,
                    border_radius=8,
                ) for msg in messages
            ], expand=True, auto_scroll=True),
            expand=True, height=350
        ),
        ft.Row([
            message_input,
            ft.IconButton(ft.icons.SEND, on_click=send_click)
        ], alignment=ft.MainAxisAlignment.END)
    ], expand=True)
