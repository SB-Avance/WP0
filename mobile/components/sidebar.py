# Sidebar component for Flet app
import flet as ft

def SidebarView(on_nav):
    return ft.NavigationRail(
        destinations=[
            ft.NavigationRailDestination(icon=ft.icons.CHAT, label="Chats"),
            ft.NavigationRailDestination(icon=ft.icons.PEOPLE, label="Usuarios"),
            ft.NavigationRailDestination(icon=ft.icons.SETTINGS, label="Ajustes"),
        ],
        selected_index=0,
        on_change=on_nav,
        label_type=ft.NavigationRailLabelType.ALL,
        extended=True,
        expand=True,
    )
