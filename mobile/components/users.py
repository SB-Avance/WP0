# Users component for Flet app
import flet as ft

def UsersView(users):
    return ft.Column([
        ft.Text("Usuarios", size=20, weight=ft.FontWeight.BOLD),
        *(ft.Text(user["correo"]) for user in users)
    ])
