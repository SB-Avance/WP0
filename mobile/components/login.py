# Login component for Flet app (responsive)
import flet as ft

def LoginView(correo_input, clave_input, on_login):
    return ft.Container(
        content=ft.Column([
            ft.Text("Iniciar sesión", size=24, weight=ft.FontWeight.BOLD),
            correo_input,
            clave_input,
            ft.ElevatedButton("Entrar", on_click=on_login),
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        alignment=ft.alignment.center,
        padding=40,
        width=400,
        height=400,
        bgcolor=ft.colors.WHITE,
        border_radius=20,
        shadow=ft.BoxShadow(blur_radius=12, color=ft.colors.GREY_300),
        expand=True,
    )
