# ChatDetailView: muestra los mensajes de una conversación y permite responder
from datetime import datetime

import flet as ft


def format_message_time(timestamp):
    """Formatea el timestamp para mostrar fecha y hora"""
    try:
        if isinstance(timestamp, str):
            # Intentar parsear ISO format
            if "T" in timestamp:
                dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            else:
                dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        elif isinstance(timestamp, (int, float)):
            dt = datetime.fromtimestamp(timestamp)
        else:
            return ""

        # Formato: "25/01/2026 14:30"
        return dt.strftime("%d/%m/%Y %H:%M")
    except:
        return timestamp if timestamp else ""


def ChatDetailView(
    conversation, messages, on_back, on_send, on_refresh=None, current_group=None
):
    name = conversation.get("name", "Desconocido")
    phone = conversation.get("phone", "")
    # Campo de entrada para el mensaje
    message_input = ft.TextField(hint_text="Escribe un mensaje...", expand=True)

    def send_click(e):
        if message_input.value.strip():
            on_send(message_input.value)
            message_input.value = ""
            message_input.update()

    # Crear header con botón de refrescar
    header_items = [
        ft.IconButton(ft.icons.ARROW_BACK, on_click=on_back),
        ft.Column(
            [
                ft.Text(f"{name} ({phone})", weight=ft.FontWeight.BOLD, size=18),
                (
                    ft.Text(f"Grupo: {current_group}", size=12, color=ft.colors.BLUE)
                    if current_group
                    else None
                ),
            ],
            spacing=0,
            expand=True,
        ),
    ]
    if on_refresh:
        header_items.append(
            ft.IconButton(
                ft.icons.REFRESH, on_click=on_refresh, tooltip="Actualizar mensajes"
            )
        )

    return ft.Column(
        [
            ft.Row(header_items, alignment=ft.MainAxisAlignment.START),
            ft.Divider(),
            ft.Container(
                ft.ListView(
                    [
                        ft.Container(
                            ft.Column(
                                [
                                    ft.Text(
                                        msg["body"],
                                        size=15,
                                        color=(
                                            ft.colors.BLACK
                                            if msg["direction"] == "incoming"
                                            else ft.colors.BLUE_900
                                        ),
                                    ),
                                    ft.Text(
                                        format_message_time(msg.get("timestamp", "")),
                                        size=10,
                                        color=ft.colors.GREY_600,
                                        italic=True,
                                    ),
                                ],
                                spacing=2,
                            ),
                            alignment=(
                                ft.alignment.center_left
                                if msg["direction"] == "incoming"
                                else ft.alignment.center_right
                            ),
                            padding=ft.padding.all(8),
                            margin=ft.margin.only(
                                bottom=6,
                                left=8 if msg["direction"] == "incoming" else 40,
                                right=40 if msg["direction"] == "incoming" else 8,
                            ),
                            bgcolor=(
                                ft.colors.GREY_100
                                if msg["direction"] == "incoming"
                                else ft.colors.BLUE_50
                            ),
                            border_radius=12,
                        )
                        for msg in messages
                    ],
                    expand=True,
                    auto_scroll=True,
                ),
                expand=True,
                height=350,
            ),
            ft.Row(
                [message_input, ft.IconButton(ft.icons.SEND, on_click=send_click)],
                alignment=ft.MainAxisAlignment.END,
            ),
        ],
        expand=True,
    )
