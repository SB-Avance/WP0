# Users component for Flet app
import flet as ft

def UsersView(users, on_back):
    return ft.Container(
        ft.Column([
        ft.Row([
            ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=on_back, tooltip="Volver"),
            ft.Text("Usuarios", size=20, weight=ft.FontWeight.BOLD),
        ]),
        ft.Divider(height=1),
        ft.ListView(
            controls=[
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.icons.PERSON, size=16, color=ft.colors.BLUE_400),
                        ft.Column([
                            ft.Text(user.get("nombre", "Sin nombre"), size=13, weight=ft.FontWeight.W_500),
                            ft.Text(user.get("correo", ""), size=11, color=ft.colors.GREY_600),
                        ], spacing=2, expand=True),
                        ft.Container(
                            content=ft.Text(user.get('rol', 'usuario')[:5].upper(), size=10, color=ft.colors.WHITE),
                            bgcolor=ft.colors.BLUE_400 if user.get('rol') == 'administrador' else ft.colors.GREY_400,
                            padding=ft.padding.symmetric(horizontal=6, vertical=3),
                            border_radius=3,
                        ),
                    ], spacing=10),
                    padding=10,
                    border=ft.border.only(bottom=ft.border.BorderSide(1, ft.colors.GREY_200)),
                )
                for user in users
            ],
            expand=True,
        ) if users else ft.Text("No hay usuarios disponibles", color=ft.colors.GREY_500)
        ], expand=True, spacing=0),
        expand=True,
        padding=10
    )
