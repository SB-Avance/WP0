# Dashboard component for Flet app
import flet as ft

def DashboardView(on_back=None, on_group_change=None, current_group=None):
    controls = []
    if on_back:
        controls.append(ft.Row([
            ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=on_back),
            ft.Text("Dashboard", size=22, weight=ft.FontWeight.BOLD),
        ]))
    else:
        controls.append(ft.Text("Dashboard", size=22, weight=ft.FontWeight.BOLD))
    
    controls.append(ft.Text("Bienvenido al panel principal."))
    controls.append(ft.Divider())
    
    # Selector de grupo
    if on_group_change:
        group_dropdown = ft.Dropdown(
            label="Grupo Actual",
            hint_text="Selecciona un grupo",
            value=current_group,
            options=[
                ft.dropdown.Option("SERVICIOS", "Servicios"),
                ft.dropdown.Option("COTIZACIONES", "Cotizaciones"),
                ft.dropdown.Option("SOPORTE", "Soporte"),
                ft.dropdown.Option("VENTAS", "Ventas"),
                ft.dropdown.Option("GENERAL", "General"),
            ],
            on_change=on_group_change,
            width=300
        )
        
        controls.append(ft.Text("Categoría de Conversaciones", size=16, weight=ft.FontWeight.BOLD))
        controls.append(ft.Text("Selecciona el grupo para categorizar los chats:", size=12))
        controls.append(group_dropdown)
        
        if current_group:
            controls.append(ft.Container(
                ft.Row([
                    ft.Icon(ft.icons.INFO_OUTLINE, color=ft.colors.BLUE),
                    ft.Text(f"Grupo activo: {current_group}", size=14, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE)
                ]),
                padding=10,
                bgcolor=ft.colors.BLUE_50,
                border_radius=8,
                margin=ft.margin.only(top=10)
            ))
    
    return ft.Column(controls, alignment=ft.MainAxisAlignment.START, spacing=10)
