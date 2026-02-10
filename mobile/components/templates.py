# Templates component for Flet app
import flet as ft
import requests

def TemplatesView(on_back=None, api_base_url="http://localhost:5000", token=None):
    """Vista para gestión de templates de WhatsApp"""
    
    # Estado local
    templates_list = []
    selected_template = {"value": None}
    edit_mode = {"value": False}
    page_ref = {"value": None}
    
    # Campos del formulario
    nombre_field = ft.TextField(label="Nombre del Template", width=300)
    categoria_dropdown = ft.Dropdown(
        label="Categoría",
        width=300,
        options=[
            ft.dropdown.Option(key="462410000", text="Marketing"),
            ft.dropdown.Option(key="462410001", text="Utilidad"),
            ft.dropdown.Option(key="462410002", text="Autenticación"),
        ],
        value="462410001"
    )
    contenido_field = ft.TextField(
        label="Contenido del Template",
        multiline=True,
        min_lines=5,
        max_lines=10,
        width=300
    )
    activo_switch = ft.Switch(label="Activo", value=True)
    
    def load_templates():
        """Cargar templates desde la API"""
        try:
            url = f"{api_base_url}/api/templates"
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                templates_list.clear()
                templates_list.extend(data.get("templates", []))
                print(f"[TEMPLATES] Cargados {len(templates_list)} templates")
                return True
            else:
                print(f"[TEMPLATES] Error al cargar: {response.status_code}")
                return False
        except Exception as e:
            print(f"[TEMPLATES] Excepción al cargar: {e}")
            return False
    
    def save_template(e):
        """Guardar template (crear o actualizar)"""
        nombre = nombre_field.value
        categoria = int(categoria_dropdown.value)
        contenido = contenido_field.value
        activo = activo_switch.value
        
        if not nombre or not contenido:
            show_snackbar("El nombre y contenido son requeridos")
            return
        
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            } if token else {"Content-Type": "application/json"}
            
            data = {
                "nombre": nombre,
                "categoria": categoria,
                "contenido": contenido,
                "activo": activo
            }
            
            if edit_mode["value"] and selected_template["value"]:
                # Actualizar
                url = f"{api_base_url}/api/templates/{selected_template['value']['id']}"
                response = requests.patch(url, json=data, headers=headers, timeout=10)
            else:
                # Crear
                url = f"{api_base_url}/api/templates"
                response = requests.post(url, json=data, headers=headers, timeout=10)
            
            if response.status_code in [200, 201]:
                show_snackbar("Template guardado exitosamente")
                cancel_edit(None)
                load_templates()
                render_list()
                
                # Actualizar la interfaz
                if "column" in page_ref and hasattr(page_ref["column"], 'update'):
                    try:
                        page_ref["column"].update()
                    except:
                        pass
            else:
                show_snackbar(f"Error al guardar: {response.status_code}")
        
        except Exception as ex:
            print(f"[TEMPLATES] Error al guardar: {ex}")
            show_snackbar(f"Error: {str(ex)}")
    
    def edit_template(template):
        """Editar template existente"""
        selected_template["value"] = template
        edit_mode["value"] = True
        nombre_field.value = template["nombre"]
        categoria_dropdown.value = str(template["categoria_valor"])
        contenido_field.value = template["contenido"]
        activo_switch.value = template["activo"]
        
        render_form()
        
        # Actualizar la interfaz
        if "column" in page_ref and hasattr(page_ref["column"], 'update'):
            try:
                page_ref["column"].update()
            except:
                pass
    
    def delete_template(template):
        """Eliminar template"""
        try:
            url = f"{api_base_url}/api/templates/{template['id']}"
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            response = requests.delete(url, headers=headers, timeout=10)
            
            if response.status_code in [200, 204]:
                show_snackbar("Template eliminado")
                load_templates()
                render_list()
                
                # Actualizar la interfaz
                if "column" in page_ref and hasattr(page_ref["column"], 'update'):
                    try:
                        page_ref["column"].update()
                    except:
                        pass
            else:
                show_snackbar(f"Error al eliminar: {response.status_code}")
        except Exception as ex:
            print(f"[TEMPLATES] Error al eliminar: {ex}")
            show_snackbar(f"Error: {str(ex)}")
    
    def cancel_edit(e):
        """Cancelar edición"""
        selected_template["value"] = None
        edit_mode["value"] = False
        nombre_field.value = ""
        categoria_dropdown.value = "462410001"
        contenido_field.value = ""
        activo_switch.value = True
        render_form()
        
        # Actualizar la interfaz
        if "column" in page_ref and hasattr(page_ref["column"], 'update'):
            try:
                page_ref["column"].update()
            except:
                pass
    
    def show_snackbar(message):
        """Mostrar mensaje temporal"""
        print(f"[TEMPLATES] {message}")
    
    def new_template_click(e):
        """Manejar clic en nuevo template"""
        cancel_edit(None)
    
    def render_list():
        """Renderizar lista de templates"""
        list_container.controls.clear()
        
        if not templates_list:
            list_container.controls.append(
                ft.Container(
                    ft.Column([
                        ft.Icon(ft.icons.INFO_OUTLINE, size=50, color=ft.colors.BLUE_400),
                        ft.Text("No hay templates configurados", size=16),
                        ft.Text("Haz clic en 'Nuevo Template' para crear uno", size=12, color=ft.colors.GREY),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                    padding=40,
                    alignment=ft.alignment.center
                )
            )
        else:
            for template in templates_list:
                list_container.controls.append(
                    ft.Container(
                        ft.Row([
                            ft.Icon(
                                ft.icons.ARTICLE,
                                size=40,
                                color=ft.colors.GREEN if template["activo"] else ft.colors.GREY
                            ),
                            ft.Column([
                                ft.Text(template["nombre"], size=16, weight=ft.FontWeight.BOLD),
                                ft.Text(f"Categoría: {template['categoria']}", size=12, color=ft.colors.GREY_700),
                                ft.Text(
                                    "Activo" if template["activo"] else "Inactivo",
                                    size=12,
                                    color=ft.colors.GREEN if template["activo"] else ft.colors.RED
                                ),
                            ], spacing=2, expand=True),
                            ft.IconButton(
                                icon=ft.icons.EDIT,
                                tooltip="Editar",
                                on_click=lambda e, t=template: edit_template(t)
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                tooltip="Eliminar",
                                icon_color=ft.colors.RED,
                                on_click=lambda e, t=template: delete_template(t)
                            ),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=15,
                        bgcolor=ft.colors.WHITE,
                        border=ft.border.all(1, ft.colors.GREY_300),
                        border_radius=8,
                        margin=ft.margin.only(bottom=10)
                    )
                )
    
    def render_form():
        """Renderizar formulario"""
        form_container.controls.clear()
        
        # Construir botones
        buttons = [
            ft.ElevatedButton(
                "Guardar",
                icon=ft.icons.SAVE,
                on_click=save_template
            )
        ]
        if edit_mode["value"]:
            buttons.append(
                ft.OutlinedButton(
                    "Cancelar",
                    on_click=cancel_edit
                )
            )
        
        form_controls = [
            ft.Text(
                "Editar Template" if edit_mode["value"] else "Nuevo Template",
                size=18,
                weight=ft.FontWeight.BOLD
            ),
            ft.Divider(),
            nombre_field,
            categoria_dropdown,
            contenido_field,
            activo_switch,
            ft.Row(buttons, spacing=10)
        ]
        
        form_container.controls.extend(form_controls)
    
    # Containers principales
    list_container = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)
    form_container = ft.Column(spacing=15)
    
    # Cargar templates inicialmente
    load_templates()
    render_list()
    render_form()
    
    # Layout principal
    controls = []
    
    # Header
    if on_back:
        controls.append(ft.Row([
            ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=on_back, tooltip="Regresar"),
            ft.Text("Gestión de Templates", size=22, weight=ft.FontWeight.BOLD),
        ], alignment=ft.MainAxisAlignment.START))
    else:
        controls.append(ft.Text("Gestión de Templates", size=22, weight=ft.FontWeight.BOLD))
    
    controls.append(ft.Divider())
    
    # Información
    controls.append(
        ft.Container(
            ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.ARTICLE, size=40, color=ft.colors.BLUE),
                    ft.Column([
                        ft.Text("Templates de WhatsApp", size=18, weight=ft.FontWeight.BOLD),
                        ft.Text("Gestiona plantillas de mensajes", size=14, color=ft.colors.GREY_700),
                    ], spacing=2),
                ], spacing=15),
            ], spacing=15),
            padding=20,
            bgcolor=ft.colors.BLUE_50,
            border_radius=12,
        )
    )
    
    # Botón nuevo template
    controls.append(ft.Container(
        ft.ElevatedButton(
            "Nuevo Template",
            icon=ft.icons.ADD,
            on_click=new_template_click
        ),
        margin=ft.margin.only(top=20, bottom=10)
    ))
    
    # Lista de templates
    controls.append(ft.Container(
        ft.Text("Templates Disponibles", size=18, weight=ft.FontWeight.BOLD),
        margin=ft.margin.only(top=10, bottom=5)
    ))
    controls.append(list_container)
    
    # Formulario
    controls.append(ft.Divider())
    controls.append(form_container)
    
    # Crear la columna principal
    main_column = ft.Column(controls, alignment=ft.MainAxisAlignment.START, spacing=10, scroll=ft.ScrollMode.AUTO)
    
    # Guardar referencia para actualización
    page_ref["column"] = main_column
    
    main_container = ft.Container(
        main_column,
        expand=True,
        padding=10
    )
    
    return main_container
