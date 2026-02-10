# Sidebar component for Flet app
import flet as ft

def SidebarView(on_nav, on_logout=None, user_name=None, current_groups=None, on_group_change=None):
    """
    Sidebar con navegación y selector de grupos
    
    Args:
        on_nav: Callback para navegación entre vistas
        on_logout: Callback para cambio de usuario
        user_name: Nombre del usuario actual
        current_groups: Lista de grupos disponibles para el usuario
        on_group_change: Callback cuando se cambia el grupo seleccionado
    """
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
                ft.Text(
                    user_name, 
                    size=9, 
                    text_align=ft.TextAlign.CENTER, 
                    weight=ft.FontWeight.BOLD, 
                    max_lines=1, 
                    overflow=ft.TextOverflow.ELLIPSIS
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
            padding=ft.padding.symmetric(vertical=5, horizontal=2)
        )
    
    # Selector de grupos (si está disponible)
    group_selector = None
    if current_groups and on_group_change and len(current_groups) > 0:
        # Filtrar valores None o vacíos
        valid_groups = [g for g in current_groups if g and str(g).strip()]
        
        if len(valid_groups) > 0:
            group_selector = ft.Container(
                ft.Column([
                    ft.Icon(ft.icons.FILTER_LIST, size=18, color=ft.colors.BLUE_700),
                    ft.Dropdown(
                        options=[ft.dropdown.Option(key=g, text=g[:10]) for g in valid_groups],
                        value=valid_groups[0] if valid_groups else None,
                        on_change=on_group_change,
                        width=55,
                        height=35,
                        text_size=8,
                        dense=True,
                        content_padding=ft.padding.all(2),
                        tooltip="Filtrar por grupo"
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                padding=ft.padding.symmetric(vertical=5, horizontal=2),
                bgcolor=ft.colors.BLUE_50,
                border_radius=5
            )
    
    nav_rail = ft.NavigationRail(
        destinations=[
            ft.NavigationRailDestination(icon=ft.icons.CHAT, label="Chats"),
            ft.NavigationRailDestination(icon=ft.icons.SMART_TOY, label="Chatbots"),
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
    content_items = []
    
    if user_button:
        content_items.append(user_button)
        content_items.append(ft.Divider(height=1, color=ft.colors.OUTLINE_VARIANT))
    
    if group_selector:
        content_items.append(group_selector)
        content_items.append(ft.Divider(height=1, color=ft.colors.OUTLINE_VARIANT))
    
    content_items.append(
        ft.Container(
            nav_rail,
            height=650 if (user_button or group_selector) else 800
        )
    )
    
    return ft.Container(
        ft.Column(content_items, spacing=0),
        width=60,
        bgcolor=ft.colors.SURFACE_VARIANT
    )
