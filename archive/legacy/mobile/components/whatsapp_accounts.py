# WhatsApp Accounts component for Flet app
import flet as ft
import requests


def WhatsAppAccountsView(
    on_back=None, api_base_url="http://localhost:5000", token=None
):
    """Vista para gestión de cuentas de WhatsApp"""

    # Estado local
    accounts_list = []
    selected_account = {"value": None}
    edit_mode = {"value": False}
    page_ref = {"value": None}

    # Campos del formulario
    nombre_field = ft.TextField(label="Nombre de la Cuenta", width=300)
    phone_field = ft.TextField(label="Número de Teléfono", width=300)
    phone_id_field = ft.TextField(
        label="Phone Number ID (WhatsApp Business)", width=300
    )
    access_token_field = ft.TextField(
        label="Access Token", password=True, can_reveal_password=True, width=300
    )
    activo_switch = ft.Switch(label="Activo", value=True)

    def load_accounts():
        """Cargar cuentas desde la API"""
        try:
            url = f"{api_base_url}/api/whatsapp-accounts"
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                accounts_list.clear()
                accounts_list.extend(data.get("accounts", []))
                print(f"[WHATSAPP_ACCOUNTS] Cargadas {len(accounts_list)} cuentas")
                return True
            else:
                print(f"[WHATSAPP_ACCOUNTS] Error al cargar: {response.status_code}")
                return False
        except Exception as e:
            print(f"[WHATSAPP_ACCOUNTS] Excepción al cargar: {e}")
            return False

    def save_account(e):
        """Guardar cuenta (crear o actualizar)"""
        nombre = nombre_field.value
        phone = phone_field.value
        phone_id = phone_id_field.value
        access_token = access_token_field.value
        activo = activo_switch.value

        if not nombre or not phone or not phone_id:
            show_snackbar("Nombre, teléfono y Phone ID son requeridos")
            return

        try:
            headers = (
                {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
                if token
                else {"Content-Type": "application/json"}
            )

            data = {
                "nombre": nombre,
                "phone": phone,
                "phone_id": phone_id,
                "activo": activo,
            }

            if access_token:
                data["access_token"] = access_token

            if edit_mode["value"] and selected_account["value"]:
                # Actualizar
                url = f"{api_base_url}/api/whatsapp-accounts/{selected_account['value']['id']}"
                response = requests.patch(url, json=data, headers=headers, timeout=10)
            else:
                # Crear
                url = f"{api_base_url}/api/whatsapp-accounts"
                response = requests.post(url, json=data, headers=headers, timeout=10)

            if response.status_code in [200, 201]:
                show_snackbar("Cuenta guardada exitosamente")
                cancel_edit(None)
                load_accounts()
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
            print(f"[WHATSAPP_ACCOUNTS] Error al guardar: {ex}")
            show_snackbar(f"Error: {str(ex)}")

    def edit_account(account):
        """Editar cuenta existente"""
        selected_account["value"] = account
        edit_mode["value"] = True
        nombre_field.value = account["nombre"]
        phone_field.value = account["phone"]
        phone_id_field.value = account.get("phone_id", "")
        access_token_field.value = ""  # No mostrar token por seguridad
        activo_switch.value = account["activo"]

        render_form()

        # Actualizar la interfaz
        if "column" in page_ref and hasattr(page_ref["column"], "update"):
            try:
                page_ref["column"].update()
            except:
                pass

    def delete_account(account):
        """Eliminar cuenta"""
        try:
            url = f"{api_base_url}/api/whatsapp-accounts/{account['id']}"
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            response = requests.delete(url, headers=headers, timeout=10)

            if response.status_code in [200, 204]:
                show_snackbar("Cuenta eliminada")
                load_accounts()
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
            print(f"[WHATSAPP_ACCOUNTS] Error al eliminar: {ex}")
            show_snackbar(f"Error: {str(ex)}")

    def cancel_edit(e):
        """Cancelar edición"""
        selected_account["value"] = None
        edit_mode["value"] = False
        nombre_field.value = ""
        phone_field.value = ""
        phone_id_field.value = ""
        access_token_field.value = ""
        activo_switch.value = True
        render_form()

        # Actualizar la interfaz
        if "column" in page_ref and hasattr(page_ref["column"], "update"):
            try:
                page_ref["column"].update()
            except:
                pass

    def show_snackbar(message):
        """Mostrar mensaje temporal"""
        print(f"[WHATSAPP_ACCOUNTS] {message}")

    def new_account_click(e):
        """Manejar clic en nueva cuenta"""
        cancel_edit(None)

    def render_list():
        """Renderizar lista de cuentas"""
        list_container.controls.clear()

        if not accounts_list:
            list_container.controls.append(
                ft.Container(
                    ft.Column(
                        [
                            ft.Icon(
                                ft.icons.INFO_OUTLINE, size=50, color=ft.colors.BLUE_400
                            ),
                            ft.Text("No hay cuentas configuradas", size=16),
                            ft.Text(
                                "Haz clic en 'Nueva Cuenta' para crear una",
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
            for account in accounts_list:
                list_container.controls.append(
                    ft.Container(
                        ft.Row(
                            [
                                ft.Icon(
                                    ft.icons.PHONE,
                                    size=40,
                                    color=(
                                        ft.colors.GREEN
                                        if account["activo"]
                                        else ft.colors.GREY
                                    ),
                                ),
                                ft.Column(
                                    [
                                        ft.Text(
                                            account["nombre"],
                                            size=16,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Text(
                                            f"Teléfono: {account['phone']}",
                                            size=12,
                                            color=ft.colors.GREY_700,
                                        ),
                                        ft.Text(
                                            (
                                                "Activo"
                                                if account["activo"]
                                                else "Inactivo"
                                            ),
                                            size=12,
                                            color=(
                                                ft.colors.GREEN
                                                if account["activo"]
                                                else ft.colors.RED
                                            ),
                                        ),
                                    ],
                                    spacing=2,
                                    expand=True,
                                ),
                                ft.IconButton(
                                    icon=ft.icons.EDIT,
                                    tooltip="Editar",
                                    on_click=lambda e, a=account: edit_account(a),
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    tooltip="Eliminar",
                                    icon_color=ft.colors.RED,
                                    on_click=lambda e, a=account: delete_account(a),
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

    def render_form():
        """Renderizar formulario"""
        form_container.controls.clear()

        # Construir botones
        buttons = [
            ft.ElevatedButton("Guardar", icon=ft.icons.SAVE, on_click=save_account)
        ]
        if edit_mode["value"]:
            buttons.append(ft.OutlinedButton("Cancelar", on_click=cancel_edit))

        form_controls = [
            ft.Text(
                "Editar Cuenta" if edit_mode["value"] else "Nueva Cuenta",
                size=18,
                weight=ft.FontWeight.BOLD,
            ),
            ft.Divider(),
            nombre_field,
            phone_field,
            phone_id_field,
            access_token_field,
            activo_switch,
            ft.Row(buttons, spacing=10),
        ]

        form_container.controls.extend(form_controls)

    # Containers principales
    list_container = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)
    form_container = ft.Column(spacing=15)

    # Cargar cuentas inicialmente
    load_accounts()
    render_list()
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
                    ft.Text(
                        "Gestión de Cuentas WhatsApp",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            )
        )
    else:
        controls.append(
            ft.Text("Gestión de Cuentas WhatsApp", size=22, weight=ft.FontWeight.BOLD)
        )

    controls.append(ft.Divider())

    # Información
    controls.append(
        ft.Container(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.icons.PHONE, size=40, color=ft.colors.GREEN),
                            ft.Column(
                                [
                                    ft.Text(
                                        "Cuentas WhatsApp Business",
                                        size=18,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Text(
                                        "Gestiona las cuentas de WhatsApp Business API",
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
            bgcolor=ft.colors.GREEN_50,
            border_radius=12,
        )
    )

    # Botón nueva cuenta
    controls.append(
        ft.Container(
            ft.ElevatedButton(
                "Nueva Cuenta", icon=ft.icons.ADD, on_click=new_account_click
            ),
            margin=ft.margin.only(top=20, bottom=10),
        )
    )

    # Lista de cuentas
    controls.append(
        ft.Container(
            ft.Text("Cuentas Disponibles", size=18, weight=ft.FontWeight.BOLD),
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
