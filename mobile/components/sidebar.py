# Sidebar component for Flet app
import flet as ft

def SidebarView(on_nav, on_logout=None, user_name=None):
    # Botón de usuario con dropdown/logout
    user_button = None
    if user_name and on_logout:
        user_button = ft.Container(
            ft.Column([
                ft.IconButton(
                    icon=ft.icons.ACCOUNT_CIRCLE,
                    icon_size=35,
                    icon_color=ft.colors.BLUE,
                    on_click=on_logout,
                    tooltip="Cambiar usuario"
                ),
                ft.Text(user_name, size=9, text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
            padding=ft.padding.symmetric(vertical=5, horizontal=2)
        )
    
    nav_rail = ft.NavigationRail(
        destinations=[
            ft.NavigationRailDestination(icon=ft.icons.CHAT, label="Chats"),
            ft.NavigationRailDestination(icon=ft.icons.PEOPLE, label="Usuarios"),
            ft.NavigationRailDestination(icon=ft.icons.SETTINGS, label="Ajustes"),
        ],
        selected_index=0,
        on_change=on_nav,
        label_type=ft.NavigationRailLabelType.SELECTED,
        extended=False,
        min_width=60,
    )
    
    # Construir el layout
    if user_button:
        return ft.Container(
            ft.Column([
                user_button,
                ft.Divider(height=1, color=ft.colors.OUTLINE_VARIANT),
                ft.Container(
                    nav_rail,
                    height=700  # Altura fija para iPhone
                )
            ], spacing=0),
            width=60,
            bgcolor=ft.colors.SURFACE_VARIANT
        )
    else:
        return ft.Container(
            ft.Column([
                ft.Container(
                    nav_rail,
                    height=800  # Altura fija para iPhone
                )
            ], spacing=0),
            width=60,
            bgcolor=ft.colors.SURFACE_VARIANT
        )
