# Dashboard component for Flet app
import flet as ft

def DashboardView():
    return ft.Column([
        ft.Text("Dashboard", size=22, weight=ft.FontWeight.BOLD),
        ft.Text("Bienvenido al panel principal."),
    ], alignment=ft.MainAxisAlignment.START)
