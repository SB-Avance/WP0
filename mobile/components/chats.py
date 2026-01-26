# Chats component for Flet app
import flet as ft

def ChatsView(conversations, on_select, current_group="TODOS", available_groups=None, on_group_change=None):
    if available_groups is None or len(available_groups) == 0:
        available_groups = ["TODOS"]
    else:
        # Filtrar valores None o vacíos
        available_groups = [g for g in available_groups if g and str(g).strip()]
    
    def conversation_card(conv):
        name = conv.get("name", "Desconocido")
        phone = conv.get("phone", "")
        last_message = conv.get("last_message", "")
        timestamp = conv.get("timestamp", "")
        group = conv.get("group", "GENERAL")
        avatar_letter = name[0].upper() if name else "?"
        
        return ft.Container(
            content=ft.Row([
                ft.CircleAvatar(content=ft.Text(avatar_letter), color=ft.colors.WHITE, bgcolor=ft.colors.BLUE, radius=22),
                ft.Column([
                    ft.Text(name, weight=ft.FontWeight.BOLD, size=16),
                    ft.Text(last_message, size=13, color=ft.colors.GREY_700, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                    ft.Row([
                        ft.Icon(ft.icons.GROUP, size=12, color=ft.colors.BLUE_400),
                        ft.Text(group, size=11, color=ft.colors.BLUE_600, weight=ft.FontWeight.W_500),
                    ], spacing=4),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=2, expand=True),
                ft.Column([
                    ft.Text(timestamp[:16].replace("T", " ") if timestamp else "", size=11, color=ft.colors.GREY_500),
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
    
    # Filtro de grupos
    group_filter = None
    if on_group_change and len(available_groups) > 1:
        group_filter = ft.Container(
            content=ft.Row([
                ft.Icon(ft.icons.FILTER_LIST, size=20, color=ft.colors.BLUE),
                ft.Text("Filtrar por grupo:", size=14, weight=ft.FontWeight.BOLD),
                ft.Dropdown(
                    options=[ft.dropdown.Option(key=g, text=g) for g in available_groups],
                    value=current_group,
                    on_change=on_group_change,
                    width=150,
                    height=40,
                    text_size=12,
                    dense=True
                ),
            ], spacing=10, alignment=ft.MainAxisAlignment.START),
            padding=ft.padding.symmetric(horizontal=10, vertical=8),
            bgcolor=ft.colors.BLUE_50,
            border_radius=8,
            margin=ft.margin.only(left=8, right=8, bottom=10, top=5)
        )
    
    content_list = []
    if group_filter:
        content_list.append(group_filter)
    
    content_list.extend([conversation_card(conv) for conv in conversations])
    
    return ft.Container(
        ft.ListView(content_list, expand=True, spacing=0, padding=ft.padding.only(top=10)),
        expand=True
    )
