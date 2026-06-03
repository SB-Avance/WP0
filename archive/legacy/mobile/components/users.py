# Users component for Flet app - CRUD completo
import flet as ft
import requests


def UsersView(on_back=None, api_base_url="http://localhost:5000", token=None):
    """Vista para gestión de usuarios (solo admin)"""

    # Estado local
    users_list = []
    selected_user = {"value": None}
    edit_mode = {"value": False}
    page_ref = {"value": None}

    # Campos del formulario
    nombre_field = ft.TextField(label="Nombre Completo", width=300)
    correo_field = ft.TextField(label="Correo Electrónico", width=300)
    clave_field = ft.TextField(
        label="Contraseña", password=True, can_reveal_password=True, width=300
    )
    rol_dropdown = ft.Dropdown(
        label="Rol",
        width=300,
        options=[
            ft.dropdown.Option(key="usuario", text="Usuario"),
            ft.dropdown.Option(key="administrador", text="Administrador"),
        ],
        value="usuario",
    )

    def load_users():
        """Cargar usuarios desde la API"""
        try:
            url = f"{api_base_url}/api/users"
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            print(f"[USERS] Cargando desde: {url}")
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                users_list.clear()
                users_list.extend(data.get("users", []))
                print(f"[USERS] Cargados {len(users_list)} usuarios")
                render_list()
                return True
            else:
                print(f"[USERS] Error al cargar: {response.status_code}")
                render_list()
                return False
        except Exception as e:
            print(f"[USERS] Excepción al cargar: {e}")
            render_list()
            return False

    def save_user(e):
        """Guardar usuario (crear o actualizar)"""
        nombre = nombre_field.value
        correo = correo_field.value
        clave = clave_field.value
        rol = rol_dropdown.value

        if not nombre or not correo:
            show_snackbar("Nombre y correo son requeridos")
            return

        try:
            headers = (
                {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
                if token
                else {"Content-Type": "application/json"}
            )

            data = {"nombre": nombre, "correo": correo, "rol": rol}

            # Solo incluir clave si se proporciona
            if clave:
                data["clave"] = clave
            elif not edit_mode["value"]:
                # Clave requerida para nuevo usuario
                show_snackbar("La contraseña es requerida para nuevos usuarios")
                return

            if edit_mode["value"] and selected_user["value"]:
                # Actualizar
                url = f"{api_base_url}/api/users/{selected_user['value']['id']}"
                response = requests.patch(url, json=data, headers=headers, timeout=10)
            else:
                # Crear
                url = f"{api_base_url}/api/users"
                response = requests.post(url, json=data, headers=headers, timeout=10)

            if response.status_code in [200, 201]:
                show_snackbar("Usuario guardado exitosamente")
                cancel_edit(None)
                load_users()
                render_list()

                # Actualizar la interfaz
                if "column" in page_ref and hasattr(page_ref["column"], "update"):
                    try:
                        page_ref["column"].update()
                    except:
                        pass
            else:
                show_snackbar(f"Error al guardar: {response.status_code}")

        except Exception as ex:
            print(f"[USERS] Error al guardar: {ex}")
            show_snackbar(f"Error: {str(ex)}")

    def edit_user(user):
        """Editar usuario existente"""
        selected_user["value"] = user
        edit_mode["value"] = True
        nombre_field.value = user["nombre"]
        correo_field.value = user["correo"]
        clave_field.value = ""  # No mostrar clave existente
        rol_dropdown.value = user["rol"]

        render_form()

        # Actualizar la interfaz
        if "column" in page_ref and hasattr(page_ref["column"], "update"):
            try:
                page_ref["column"].update()
            except:
                pass

    def delete_user(user):
        """Eliminar usuario"""
        try:
            url = f"{api_base_url}/api/users/{user['id']}"
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            response = requests.delete(url, headers=headers, timeout=10)

            if response.status_code in [200, 204]:
                show_snackbar("Usuario eliminado")
                load_users()
                render_list()

                # Actualizar la interfaz
                if "column" in page_ref and hasattr(page_ref["column"], "update"):
                    try:
                        page_ref["column"].update()
                    except:
                        pass
            else:
                show_snackbar(f"Error al eliminar: {response.status_code}")
        except Exception as ex:
            print(f"[USERS] Error al eliminar: {ex}")
            show_snackbar(f"Error: {str(ex)}")

    def cancel_edit(e):
        """Cancelar edición"""
        selected_user["value"] = None
        edit_mode["value"] = False
        nombre_field.value = ""
        correo_field.value = ""
        clave_field.value = ""
        rol_dropdown.value = "usuario"
        render_form()

        # Actualizar la interfaz
        if "column" in page_ref and hasattr(page_ref["column"], "update"):
            try:
                page_ref["column"].update()
            except:
                pass

    def show_snackbar(message):
        """Mostrar mensaje temporal"""
        print(f"[USERS] {message}")

    def new_user_click(e):
        """Manejar clic en nuevo usuario"""
        cancel_edit(None)

    def render_list():
        """Renderizar lista de usuarios"""
        list_container.controls.clear()

        if not users_list:
            list_container.controls.append(
                ft.Container(
                    ft.Column(
                        [
                            ft.Icon(
                                ft.icons.INFO_OUTLINE, size=50, color=ft.colors.BLUE_400
                            ),
                            ft.Text("No hay usuarios registrados", size=16),
                            ft.Text(
                                "Haz clic en 'Nuevo Usuario' para crear uno",
                                size=12,
                                color=ft.colors.GREY,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    padding=40,
                    alignment=ft.alignment.center,
                )
            )
        else:
            for user in users_list:
                list_container.controls.append(
                    ft.Container(
                        ft.Row(
                            [
                                ft.Icon(
                                    ft.icons.PERSON,
                                    size=40,
                                    color=(
                                        ft.colors.BLUE
                                        if user.get("rol") == "administrador"
                                        else ft.colors.GREY
                                    ),
                                ),
                                ft.Column(
                                    [
                                        ft.Text(
                                            user.get("nombre", "Sin nombre"),
                                            size=16,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Text(
                                            user.get("correo", ""),
                                            size=12,
                                            color=ft.colors.GREY_700,
                                        ),
                                        ft.Text(
                                            user.get("rol", "usuario").capitalize(),
                                            size=12,
                                            color=(
                                                ft.colors.BLUE
                                                if user.get("rol") == "administrador"
                                                else ft.colors.GREEN
                                            ),
                                        ),
                                    ],
                                    spacing=2,
                                    expand=True,
                                ),
                                ft.IconButton(
                                    icon=ft.icons.EDIT,
                                    tooltip="Editar usuario",
                                    on_click=lambda e, u=user: edit_user(u),
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    tooltip="Eliminar usuario",
                                    icon_color=ft.colors.RED,
                                    on_click=lambda e, u=user: delete_user(u),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        padding=15,
                        bgcolor=ft.colors.WHITE,
                        border=ft.border.all(1, ft.colors.GREY_300),
                        border_radius=8,
                        margin=ft.margin.only(bottom=10),
                    )
                )

        # Intentar actualizar si hay referencia
        if page_ref.get("column"):
            try:
                page_ref["column"].update()
            except:
                pass

    def render_form():
        """Renderizar formulario"""
        form_container.controls.clear()

        # Construir botones
        buttons = [ft.ElevatedButton("Guardar", icon=ft.icons.SAVE, on_click=save_user)]
        if edit_mode["value"]:
            buttons.append(ft.OutlinedButton("Cancelar", on_click=cancel_edit))

        form_controls = [
            ft.Text(
                "Editar Usuario" if edit_mode["value"] else "Nuevo Usuario",
                size=18,
                weight=ft.FontWeight.BOLD,
            ),
            ft.Divider(),
            nombre_field,
            correo_field,
            clave_field,
            ft.Text(
                (
                    "Deja la contraseña vacía para mantener la actual"
                    if edit_mode["value"]
                    else "La contraseña es requerida"
                ),
                size=11,
                color=ft.colors.GREY_600,
                italic=True,
            ),
            rol_dropdown,
            ft.Row(buttons, spacing=10),
        ]

        form_container.controls.extend(form_controls)

    # Containers principales
    list_container = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)
    form_container = ft.Column(spacing=15)

    # Agregar mensaje de cargando inicial
    list_container.controls.append(
        ft.Container(
            ft.Column(
                [
                    ft.ProgressRing(),
                    ft.Text("Cargando usuarios...", size=16),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            padding=40,
            alignment=ft.alignment.center,
        )
    )

    # Cargar usuarios inicialmente
    load_users()
    render_form()

    # Layout principal
    controls = []

    # Header
    if on_back:
        controls.append(
            ft.Row(
                [
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK, on_click=on_back, tooltip="Regresar"
                    ),
                    ft.Text("Gestión de Usuarios", size=22, weight=ft.FontWeight.BOLD),
                ],
                alignment=ft.MainAxisAlignment.START,
            )
        )
    else:
        controls.append(
            ft.Text("Gestión de Usuarios", size=22, weight=ft.FontWeight.BOLD)
        )

    controls.append(ft.Divider())

    # Información
    controls.append(
        ft.Container(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.icons.PEOPLE, size=40, color=ft.colors.BLUE),
                            ft.Column(
                                [
                                    ft.Text(
                                        "Editor de Usuarios",
                                        size=18,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Text(
                                        "Gestiona los usuarios del sistema",
                                        size=14,
                                        color=ft.colors.GREY_700,
                                    ),
                                ],
                                spacing=2,
                            ),
                        ],
                        spacing=15,
                    ),
                ],
                spacing=15,
            ),
            padding=20,
            bgcolor=ft.colors.BLUE_50,
            border_radius=12,
        )
    )

    # Botón nuevo usuario
    controls.append(
        ft.Container(
            ft.ElevatedButton(
                "Nuevo Usuario", icon=ft.icons.ADD, on_click=new_user_click
            ),
            margin=ft.margin.only(top=20, bottom=10),
        )
    )

    # Lista de usuarios
    controls.append(
        ft.Container(
            ft.Text("Usuarios Registrados", size=18, weight=ft.FontWeight.BOLD),
            margin=ft.margin.only(top=10, bottom=5),
        )
    )
    controls.append(list_container)

    # Formulario
    controls.append(ft.Divider())
    controls.append(form_container)

    # Crear la columna principal
    main_column = ft.Column(
        controls,
        alignment=ft.MainAxisAlignment.START,
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
    )

    # Guardar referencia para actualización
    page_ref["column"] = main_column

    main_container = ft.Container(main_column, expand=True, padding=10)

    return main_container
