# Sidebar component for Flet app
import flet as ft


def SidebarView(on_nav, on_logout=None, user_name=None, user_rol=None):
    """
    Sidebar con navegación fija basada en el rol del usuario

    Args:
        on_nav: Callback para navegación entre vistas
        on_logout: Callback para cerrar sesión
        user_name: Nombre del usuario actual
        user_rol: Rol del usuario ('administrador' o 'usuario')
    """
    # Botón de usuario
    user_button = None
    if user_name:
        user_button = ft.Container(
            ft.Column(
                [
                    ft.Icon(ft.icons.ACCOUNT_CIRCLE, size=35, color=ft.colors.BLUE),
                    ft.Text(
                        user_name,
                        size=9,
                        text_align=ft.TextAlign.CENTER,
                        weight=ft.FontWeight.BOLD,
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            padding=ft.padding.symmetric(vertical=5, horizontal=2),
        )

    # Construir destinos del menú
    destinations = []

    # 1. Chats (visible para todos, filtrado por grupo internamente)
    destinations.append(
        ft.NavigationRailDestination(
            icon_content=ft.Icon(
                ft.icons.CHAT, tooltip="Ver conversaciones de WhatsApp"
            ),
            label="Chats",
        )
    )

    # 2. Opciones administrativas (solo para administradores)
    if user_rol == "administrador":
        destinations.extend(
            [
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(
                        ft.icons.SMART_TOY, tooltip="Gestionar chatbots (CRUD)"
                    ),
                    label="Chatbots",
                ),
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(
                        ft.icons.PEOPLE, tooltip="Gestionar usuarios (CRUD)"
                    ),
                    label="Usuarios",
                ),
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(
                        ft.icons.ARTICLE, tooltip="Gestionar templates (CRUD)"
                    ),
                    label="Templates",
                ),
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(
                        ft.icons.PHONE, tooltip="Gestionar cuentas WhatsApp (CRUD)"
                    ),
                    label="Cuentas WA",
                ),
            ]
        )

    # 3. Salir (visible para todos)
    destinations.append(
        ft.NavigationRailDestination(
            icon_content=ft.Icon(ft.icons.LOGOUT, tooltip="Cerrar sesión"),
            label="Salir",
        )
    )

    nav_rail = ft.NavigationRail(
        destinations=destinations,
        selected_index=0,
        on_change=on_nav,
        label_type=ft.NavigationRailLabelType.SELECTED,
        extended=False,
        min_width=60,
    )

    # Construir el layout
    content_items = []

    if user_button:
        content_items.append(user_button)
        content_items.append(ft.Divider(height=1, color=ft.colors.OUTLINE_VARIANT))

    content_items.append(ft.Container(nav_rail, height=750))

    return ft.Container(
        ft.Column(content_items, spacing=0), width=60, bgcolor=ft.colors.SURFACE_VARIANT
    )
