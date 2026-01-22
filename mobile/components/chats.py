# Chats component for Flet app
import flet as ft

def ChatsView(conversations, on_select):
    def conversation_card(conv):
        name = conv.get("name", "Desconocido")
        phone = conv.get("phone", "")
        last_message = conv.get("last_message", "")
        timestamp = conv.get("timestamp", "")
        avatar_letter = name[0].upper() if name else "?"
        return ft.Container(
            content=ft.Row([
                ft.CircleAvatar(content=ft.Text(avatar_letter), color=ft.colors.WHITE, bgcolor=ft.colors.BLUE, radius=22),
                ft.Column([
                    ft.Text(name, weight=ft.FontWeight.BOLD, size=16),
                    ft.Text(last_message, size=13, color=ft.colors.GREY_700, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=2),
                ft.Column([
                    ft.Text(timestamp[:16].replace("T", " "), size=11, color=ft.colors.GREY_500),
                    ft.Text(phone, size=11, color=ft.colors.GREY_500),
                ], alignment=ft.MainAxisAlignment.END, horizontal_alignment=ft.CrossAxisAlignment.END),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=12,
            margin=ft.margin.only(bottom=8, left=8, right=8),
            bgcolor=ft.colors.WHITE,
            border_radius=12,
            ink=True,
            on_click=lambda e, c=conv: on_select(c),
            shadow=ft.BoxShadow(blur_radius=8, color=ft.colors.GREY_200),
        )
    return ft.ListView([
        conversation_card(conv) for conv in conversations
    ], expand=True, spacing=0, padding=0)
