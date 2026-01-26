# Settings component for Flet app
import flet as ft

def SettingsView(on_back=None):
    controls = []
    if on_back:
        controls.append(ft.Row([
            ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=on_back),
            ft.Text("Ajustes", size=20, weight=ft.FontWeight.BOLD),
        ]))
    else:
        controls.append(ft.Text("Ajustes", size=20, weight=ft.FontWeight.BOLD))
    
    controls.append(ft.Text("Configuraciones de la aplicación."))
    
    return ft.Container(
        ft.Column(controls, scroll=ft.ScrollMode.AUTO),
        expand=True,
        padding=10
    )
