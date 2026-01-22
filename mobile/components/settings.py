# Settings component for Flet app
import flet as ft

def SettingsView():
    return ft.Column([
        ft.Text("Ajustes", size=20, weight=ft.FontWeight.BOLD),
        ft.Text("Configuraciones de la aplicación."),
    ])
