# Chatbots component for Flet app
import flet as ft
import requests

def ChatbotsView(on_back=None, api_base_url="http://localhost:5000", token=None):
    """Vista para gestión de chatbots"""
    
    # Estado local
    chatbots_list = []
    selected_chatbot = {"value": None}
    edit_mode = {"value": False}
    
    # Campos del formulario
    nombre_field = ft.TextField(label="Nombre del Chatbot", width=300)
    tipo_dropdown = ft.Dropdown(
        label="Tipo de Chatbot",
        width=300,
        options=[
            ft.dropdown.Option(key="462410000", text="FlowBot"),
            ft.dropdown.Option(key="462410001", text="Simple"),
            ft.dropdown.Option(key="462410002", text="AI Assistant"),
        ],
        value="462410000"
    )
    activo_switch = ft.Switch(label="Activo", value=True)
    config_field = ft.TextField(
        label="Configuración JSON (opcional)",
        multiline=True,
        min_lines=3,
        max_lines=5,
        width=300
    )
    
    def load_chatbots():
        """Cargar chatbots desde la API"""
        try:
            url = f"{api_base_url}/api/chatbots"
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                chatbots_list.clear()
                chatbots_list.extend(data.get("chatbots", []))
                print(f"[CHATBOTS] Cargados {len(chatbots_list)} chatbots")
                return True
            else:
                print(f"[CHATBOTS] Error al cargar: {response.status_code}")
                return False
        except Exception as e:
            print(f"[CHATBOTS] Excepción al cargar: {e}")
            return False
    
    def save_chatbot(e):
        """Guardar chatbot (crear o actualizar)"""
        nombre = nombre_field.value
        tipo = int(tipo_dropdown.value)
        activo = activo_switch.value
        config = config_field.value or "{}"
        
        if not nombre:
            show_snackbar("El nombre es requerido")
            return
        
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            } if token else {"Content-Type": "application/json"}
            
            data = {
                "nombre": nombre,
                "tipo": tipo,
                "activo": activo,
                "config": config
            }
            
            if edit_mode["value"] and selected_chatbot["value"]:
                # Actualizar
                url = f"{api_base_url}/api/chatbots/{selected_chatbot['value']['id']}"
                response = requests.patch(url, json=data, headers=headers, timeout=10)
            else:
                # Crear
                url = f"{api_base_url}/api/chatbots"
                response = requests.post(url, json=data, headers=headers, timeout=10)
            
            if response.status_code in [200, 201]:
                show_snackbar("Chatbot guardado exitosamente")
                cancel_edit(None)
                load_chatbots()
                render_list()
            else:
                show_snackbar(f"Error al guardar: {response.status_code}")
        
        except Exception as ex:
            print(f"[CHATBOTS] Error al guardar: {ex}")
            show_snackbar(f"Error: {str(ex)}")
    
    def edit_chatbot(chatbot):
        """Editar chatbot existente"""
        selected_chatbot["value"] = chatbot
        edit_mode["value"] = True
        nombre_field.value = chatbot["nombre"]
        tipo_dropdown.value = str(chatbot["tipo_valor"])
        activo_switch.value = chatbot["activo"]
        config_field.value = chatbot["config"]
        render_form()
    
    def delete_chatbot(chatbot):
        """Eliminar chatbot"""
        try:
            url = f"{api_base_url}/api/chatbots/{chatbot['id']}"
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            response = requests.delete(url, headers=headers, timeout=10)
            
            if response.status_code in [200, 204]:
                show_snackbar("Chatbot eliminado")
                load_chatbots()
                render_list()
            else:
                show_snackbar(f"Error al eliminar: {response.status_code}")
        except Exception as ex:
            print(f"[CHATBOTS] Error al eliminar: {ex}")
            show_snackbar(f"Error: {str(ex)}")
    
    def cancel_edit(e):
        """Cancelar edición"""
        selected_chatbot["value"] = None
        edit_mode["value"] = False
        nombre_field.value = ""
        tipo_dropdown.value = "462410000"
        activo_switch.value = True
        config_field.value = ""
        render_form()
    
    def show_snackbar(message):
        """Mostrar mensaje temporal"""
        if hasattr(main_container, 'page') and main_container.page:
            main_container.page.snack_bar = ft.SnackBar(ft.Text(message))
            main_container.page.snack_bar.open = True
            main_container.page.update()
    
    def render_list():
        """Renderizar lista de chatbots"""
        list_container.controls.clear()
        
        if not chatbots_list:
            list_container.controls.append(
                ft.Container(
                    ft.Column([
                        ft.Icon(ft.icons.INFO_OUTLINE, size=50, color=ft.colors.BLUE_400),
                        ft.Text("No hay chatbots configurados", size=16),
                        ft.Text("Haz clic en 'Nuevo Chatbot' para crear uno", size=12, color=ft.colors.GREY),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                    padding=40,
                    alignment=ft.alignment.center
                )
            )
        else:
            for chatbot in chatbots_list:
                list_container.controls.append(
                    ft.Container(
                        ft.Row([
                            ft.Icon(
                                ft.icons.SMART_TOY,
                                size=40,
                                color=ft.colors.GREEN if chatbot["activo"] else ft.colors.GREY
                            ),
                            ft.Column([
                                ft.Text(chatbot["nombre"], size=16, weight=ft.FontWeight.BOLD),
                                ft.Text(f"Tipo: {chatbot['tipo']}", size=12, color=ft.colors.GREY_700),
                                ft.Text(
                                    "Activo" if chatbot["activo"] else "Inactivo",
                                    size=12,
                                    color=ft.colors.GREEN if chatbot["activo"] else ft.colors.RED
                                ),
                            ], spacing=2, expand=True),
                            ft.IconButton(
                                icon=ft.icons.EDIT,
                                tooltip="Editar",
                                on_click=lambda e, c=chatbot: edit_chatbot(c)
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                tooltip="Eliminar",
                                icon_color=ft.colors.RED,
                                on_click=lambda e, c=chatbot: delete_chatbot(c)
                            ),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=15,
                        bgcolor=ft.colors.WHITE,
                        border=ft.border.all(1, ft.colors.GREY_300),
                        border_radius=8,
                        margin=ft.margin.only(bottom=10)
                    )
                )
        
        if hasattr(main_container, 'page') and main_container.page:
            main_container.page.update()
    
    def render_form():
        """Renderizar formulario"""
        form_container.controls.clear()
        
        form_controls = [
            ft.Text(
                "Editar Chatbot" if edit_mode["value"] else "Nuevo Chatbot",
                size=18,
                weight=ft.FontWeight.BOLD
            ),
            ft.Divider(),
            nombre_field,
            tipo_dropdown,
            activo_switch,
            config_field,
            ft.Row([
                ft.ElevatedButton(
                    "Guardar",
                    icon=ft.icons.SAVE,
                    on_click=save_chatbot
                ),
                ft.OutlinedButton(
                    "Cancelar",
                    on_click=cancel_edit
                ) if edit_mode["value"] else None,
            ], spacing=10)
        ]
        
        form_container.controls.extend([c for c in form_controls if c is not None])
        
        if hasattr(main_container, 'page') and main_container.page:
            main_container.page.update()
    
    # Containers principales
    list_container = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)
    form_container = ft.Column(spacing=15)
    
    # Cargar chatbots inicialmente
    load_chatbots()
    render_list()
    render_form()
    
    # Layout principal
    controls = []
    
    # Header
    if on_back:
        controls.append(ft.Row([
            ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=on_back, tooltip="Regresar"),
            ft.Text("Gestión de Chatbots", size=22, weight=ft.FontWeight.BOLD),
        ], alignment=ft.MainAxisAlignment.START))
    else:
        controls.append(ft.Text("Gestión de Chatbots", size=22, weight=ft.FontWeight.BOLD))
    
    controls.append(ft.Divider())
    
    # Información
    controls.append(
        ft.Container(
            ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.SMART_TOY, size=40, color=ft.colors.BLUE),
                    ft.Column([
                        ft.Text("Editor de Chatbots", size=18, weight=ft.FontWeight.BOLD),
                        ft.Text("Gestiona los chatbots de WhatsApp", size=14, color=ft.colors.GREY_700),
                    ], spacing=2),
                ], spacing=15),
            ], spacing=15),
            padding=20,
            bgcolor=ft.colors.BLUE_50,
            border_radius=12,
        )
    )
    
    # Botón nuevo chatbot
    controls.append(ft.Container(
        ft.ElevatedButton(
            "Nuevo Chatbot",
            icon=ft.icons.ADD,
            on_click=lambda e: (cancel_edit(None), render_form())
        ),
        margin=ft.margin.only(top=20, bottom=10)
    ))
    
    # Lista de chatbots
    controls.append(ft.Container(
        ft.Text("Chatbots Disponibles", size=18, weight=ft.FontWeight.BOLD),
        margin=ft.margin.only(top=10, bottom=5)
    ))
    controls.append(list_container)
    
    # Formulario
    controls.append(ft.Divider())
    controls.append(form_container)
    
    main_container = ft.Container(
        ft.Column(controls, alignment=ft.MainAxisAlignment.START, spacing=10, scroll=ft.ScrollMode.AUTO),
        expand=True,
        padding=10
    )
    
    return main_container
    """Vista para gestión de chatbots"""
    
    controls = []
    
    # Header con botón de regreso
    if on_back:
        controls.append(ft.Row([
            ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=on_back, tooltip="Regresar"),
            ft.Text("Gestión de Chatbots", size=22, weight=ft.FontWeight.BOLD),
        ], alignment=ft.MainAxisAlignment.START))
    else:
        controls.append(ft.Text("Gestión de Chatbots", size=22, weight=ft.FontWeight.BOLD))
    
    controls.append(ft.Divider())
    
    # Información
    controls.append(
        ft.Container(
            ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.SMART_TOY, size=40, color=ft.colors.BLUE),
                    ft.Column([
                        ft.Text("Editor de Chatbots", size=18, weight=ft.FontWeight.BOLD),
                        ft.Text("Gestiona los chatbots de WhatsApp", size=14, color=ft.colors.GREY_700),
                    ], spacing=2),
                ], spacing=15),
                ft.Divider(),
                ft.Text("Funcionalidades:", size=16, weight=ft.FontWeight.BOLD),
                ft.Column([
                    ft.Row([ft.Icon(ft.icons.CHECK_CIRCLE, size=16, color=ft.colors.GREEN), 
                            ft.Text("Crear nuevos chatbots con flujos personalizados", size=14)]),
                    ft.Row([ft.Icon(ft.icons.CHECK_CIRCLE, size=16, color=ft.colors.GREEN), 
                            ft.Text("Configurar respuestas automáticas", size=14)]),
                    ft.Row([ft.Icon(ft.icons.CHECK_CIRCLE, size=16, color=ft.colors.GREEN), 
                            ft.Text("Asignar chatbots a cuentas de WhatsApp", size=14)]),
                    ft.Row([ft.Icon(ft.icons.CHECK_CIRCLE, size=16, color=ft.colors.GREEN), 
                            ft.Text("Activar/desactivar chatbots", size=14)]),
                ], spacing=8),
            ], spacing=15),
            padding=20,
            bgcolor=ft.colors.BLUE_50,
            border_radius=12,
        )
    )
    
    # Placeholder para lista de chatbots
    controls.append(ft.Container(
        ft.Text("Chatbots Disponibles", size=18, weight=ft.FontWeight.BOLD),
        margin=ft.margin.only(top=20)
    ))
    
    # Nota: Aquí se cargarían los chatbots desde la API
    # Por ahora, mostramos un mensaje informativo
    controls.append(
        ft.Container(
            ft.Column([
                ft.Icon(ft.icons.INFO_OUTLINE, size=50, color=ft.colors.BLUE_400),
                ft.Text("Próximamente", size=16, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Esta funcionalidad permitirá crear y editar chatbots directamente desde la aplicación.",
                    size=14,
                    text_align=ft.TextAlign.CENTER,
                    color=ft.colors.GREY_700,
                ),
                ft.Divider(),
                ft.Text("Para configurar chatbots actualmente:", size=14, weight=ft.FontWeight.BOLD),
                ft.Text("1. Acceder a Dataverse → tabla cr321_chatbot", size=12),
                ft.Text("2. Crear nuevo registro con tipo, nombre y configuración", size=12),
                ft.Text("3. Asignar a cuenta de WhatsApp", size=12),
                ft.Text("4. Activar el chatbot", size=12),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
            padding=30,
            margin=ft.margin.symmetric(horizontal=20, vertical=10),
            bgcolor=ft.colors.SURFACE_VARIANT,
            border_radius=12,
        )
    )
    
    # Botón para crear nuevo chatbot (placeholder)
    controls.append(
        ft.Container(
            ft.ElevatedButton(
                "Crear Nuevo Chatbot",
                icon=ft.icons.ADD_CIRCLE,
                on_click=lambda e: None,  # Placeholder
                disabled=True,
            ),
            margin=ft.margin.only(top=10),
            alignment=ft.alignment.center,
        )
    )
    
    return ft.Container(
        ft.Column(controls, alignment=ft.MainAxisAlignment.START, spacing=10, scroll=ft.ScrollMode.AUTO),
        expand=True,
        padding=10
    )
