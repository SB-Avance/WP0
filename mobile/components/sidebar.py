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
        label_type=ft.NavigationRailLabelType.ALL,
        extended=True,
    )
    
    logout_button = None
    if on_logout:
        logout_button = ft.Container(
            ft.ElevatedButton(
                text="Cerrar Sesión",
                icon=ft.icons.LOGOUT,
                on_click=on_logout,
                color=ft.colors.RED_400,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8)
                )
            ),
            padding=ft.padding.all(10),
            alignment=ft.alignment.center
        )
    
    # Construir el layout
    if user_info and logout_button:
        return ft.Container(
            ft.Column([
                user_info,
                ft.Divider(height=1),
                ft.Container(nav_rail, expand=True),
                logout_button
            ], spacing=0),
            expand=True
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
