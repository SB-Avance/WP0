# Sidebar component for Flet app
import flet as ft

def SidebarView(on_nav, on_logout=None, user_name=None):
    user_info = None
    if user_name:
        user_info = ft.Container(
            ft.Column([
                ft.Icon(ft.icons.ACCOUNT_CIRCLE, size=40, color=ft.colors.BLUE),
                ft.Text(user_name, size=12, text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
            padding=ft.padding.all(10)
        )
    
    nav_rail = ft.NavigationRail(
        destinations=[
            ft.NavigationRailDestination(icon=ft.icons.CHAT, label="Chats"),
            ft.NavigationRailDestination(icon=ft.icons.PEOPLE, label="Usuarios"),
            ft.NavigationRailDestination(icon=ft.icons.SETTINGS, label="Ajustes"),
        ],
        selected_index=0,
        on_change=on_nav,
        label_type=ft.NavigationRailLabelType.SELECTED,  # Solo mostrar label del seleccionado
        extended=False,  # Modo compacto
        min_width=60,  # Ancho mínimo para móvil
    )
    
    logout_button = None
    if on_logout:
        logout_button = ft.Container(
            ft.IconButton(
                icon=ft.icons.LOGOUT,
                on_click=on_logout,
                icon_color=ft.colors.RED_400,
                tooltip="Cerrar Sesión"
            ),
            padding=ft.padding.all(5),
            alignment=ft.alignment.center
        )
    
    # Construir el layout
    if user_info and logout_button:
        return ft.Container(
            ft.Column([
                ft.Container(
                    ft.Icon(ft.icons.ACCOUNT_CIRCLE, size=30, color=ft.colors.BLUE),
                    padding=5
                ),
                ft.Container(nav_rail, expand=True),
                logout_button
            ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=60,  # Ancho fijo para móvil
            bgcolor=ft.colors.SURFACE_VARIANT
        )
    elif user_info:
        return ft.Container(
            ft.Column([
                user_info,
                ft.Divider(height=1),
                ft.Container(nav_rail, expand=True)
            ], spacing=0),
            expand=True
        )
    elif logout_button:
        return ft.Container(
            ft.Column([
                ft.Container(nav_rail, expand=True),
                logout_button
            ], spacing=0),
            expand=True
        )
    else:
        return ft.Container(nav_rail, expand=True)
