import os

import requests
from dotenv import load_dotenv

load_dotenv()  # Cargar .env

# Variables de entorno
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
AZURE_REGION = os.getenv("AZURE_REGION")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
ENTITY_SET = os.getenv("ENTITY_SET")
ENTITY_SET_USR = os.getenv("ENTITY_SET_USR")
DATAVERSE_URL = os.getenv("DATAVERSE_URL")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
PHONE_NUMBER_ID0 = os.getenv("PHONE_NUMBER_ID0")
PHONE_NUMBER_ID1 = os.getenv("PHONE_NUMBER_ID1")
PHONE_NUMBER_ID2 = os.getenv("PHONE_NUMBER_ID2")
TENANT_ID = os.getenv("TENANT_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
Z_URL_ENTORNO = os.getenv("Z_URL_ENTORNO")
Z_ZPRUEBA = os.getenv("Z_PRUEBA")


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def mostrar_variables():
    return f"""
ACCESS_TOKEN:       {ACCESS_TOKEN[:10]}... (oculto)
AZURE_REGION:       {AZURE_REGION}
CLIENT_ID:          {CLIENT_ID}
CLIENT_SECRET:      {CLIENT_SECRET[:6]}... (oculto)
ENTITY_SET:         {ENTITY_SET}
DATAVERSE_URL:      {DATAVERSE_URL}
PHONE_NUMBER_ID:    {PHONE_NUMBER_ID}
PHONE_NUMBER_ID0:   {PHONE_NUMBER_ID0}
PHONE_NUMBER_ID1:   {PHONE_NUMBER_ID1}
PHONE_NUMBER_ID2:   {PHONE_NUMBER_ID2}
TENANT_ID:          {TENANT_ID}
VERIFY_TOKEN:       {VERIFY_TOKEN}
Z_URL_ENTORNO:      {Z_URL_ENTORNO}
Z_ZPRUEBA:          {Z_ZPRUEBA}
    """


def get_token():
    from back import get_token as get_token_app

    return get_token_app()


def get_user_by_email(email):
    token = get_token()
    if not token:
        print("No se pudo obtener token de acceso.")
        return None

    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuarioses?$filter=cr321_correo eq '{email}'"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    print("[DEBUG] URL get_user_by_email:", url)
    print("[DEBUG] Token (primeros 20):", token[:20])
    print(f"[DEBUG] Email buscado: {email}")
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            users = data.get("value", [])
            print(f"[DEBUG] Usuarios encontrados: {users}")
            if users:
                user = users[0]
                # Mapeo automático de rol numérico a string
                rol_val = user.get("cr321_rol")
                if isinstance(rol_val, int):
                    if rol_val == 462410001:
                        user["cr321_rol"] = "administrador"
                    elif rol_val == 462410000:
                        user["cr321_rol"] = "usuario"
                return user
        else:
            print(f"Error Dataverse: {response.status_code} - {response.text}")
        return None
    except Exception as e:
        print(f"Error al consultar usuario por email: {e}")
        return None


def create_user(nombre, correo, rol, clave):
    token = get_token()
    if not token:
        print("No se pudo obtener token de acceso.")
        return None

    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuarioses"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    # Mapeo inverso: string a int para Dataverse
    rol_map = {"administrador": 462410001, "usuario": 462410000}
    rol_val = rol_map.get(str(rol).lower(), rol)

    # Obtener el máximo cr321_idusuario actual
    max_id = 0
    try:
        url_get = (
            f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuarioses?$select=cr321_idusuario"
        )
        response = requests.get(
            url_get,
            headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
        )
        if response.status_code == 200:
            data = response.json()
            for user in data.get("value", []):
                try:
                    val = int(user.get("cr321_idusuario", 0))
                    if val > max_id:
                        max_id = val
                except Exception:
                    pass
    except Exception as e:
        print(f"[WARN] No se pudo obtener el máximo cr321_idusuario: {e}")
    nuevo_id = str(max_id + 1)

    user_data = {
        "cr321_nombre": nombre,
        "cr321_correo": correo,
        "cr321_rol": rol_val,
        "cr321_clave": clave,
        "cr321_idusuario": nuevo_id,
    }
    try:
        response = requests.post(url, headers=headers, json=user_data)
        if response.status_code in (200, 201, 204):
            return response.headers.get("OData-EntityId", None)
        else:
            print(f"Error al crear usuario: {response.status_code} - {response.text}")
        return None
    except Exception as e:
        print(f"Error al crear usuario: {e}")
        return None


def get_user_by_id(user_id):
    token = get_token()
    if not token:
        print("No se pudo obtener token de acceso.")
        return None

    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuarioses({user_id})"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error Dataverse: {response.status_code} - {response.text}")
        return None
    except Exception as e:
        print(f"Error al obtener usuario por ID: {e}")
        return None


def get_all_users():
    """Obtiene todos los usuarios de Dataverse"""
    token = get_token()
    if not token:
        print("No se pudo obtener token de acceso.")
        return []
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuarioses"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            users = data.get("value", [])
            # Mapear roles numéricos a strings
            for user in users:
                rol_val = user.get("cr321_rol")
                if isinstance(rol_val, int):
                    if rol_val == 462410001:
                        user["cr321_rol"] = "administrador"
                    elif rol_val == 462410000:
                        user["cr321_rol"] = "usuario"
            return users
        else:
            print(f"Error Dataverse: {response.status_code} - {response.text}")
        return []
    except Exception as e:
        print(f"Error al consultar todos los usuarios: {e}")
        return []


def print_all_users():
    """Imprime todos los usuarios en consola"""
    users = get_all_users()
    print(f"Usuarios encontrados: {len(users)}")
    for user in users:
        print(user)


def get_messages_by_phone(phone):
    token = get_token()
    if not token:
        print("No se pudo obtener token de acceso.")
        return []
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$filter=cr321_phone eq '{phone}'&$orderby=cr321_timestamp asc"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get("value", [])
        else:
            print(f"Error Dataverse: {response.status_code} - {response.text}")
        return []
    except Exception as e:
        print(f"Error al consultar mensajes: {e}")
        return []


def delete_message_by_id(msg_id):
    token = get_token()
    if not token:
        print("No se pudo obtener token de acceso.")
        return False
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s({msg_id})"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    try:
        response = requests.delete(url, headers=headers)
        return response.status_code in (200, 204)
    except Exception as e:
        print(f"Error al eliminar mensaje: {e}")
        return False


def get_conversations_for_user(user):
    """Obtiene las conversaciones. Admin ve todas, usuarios ven sus conversaciones asignadas"""
    token = get_token()
    if not token:
        print("No se pudo obtener token de acceso.")
        return []

    rol = user.get("cr321_rol", "").lower()

    print(f"[DEBUG USUARIO] Rol del usuario: '{rol}' (tipo: {type(rol)})")
    print(f"[DEBUG USUARIO] Es administrador: {rol == 'administrador'}")
    print(f"[DEBUG USUARIO] Correo: {user.get('cr321_correo', 'N/A')}")

    # Si es administrador, obtener todas las conversaciones
    if rol == "administrador":
        url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$orderby=cr321_timestamp desc"
        # Expandir categoría del chatbot si existe el campo
        url += "&$expand=cr321_categoria_chatbot($select=cr321_nombre,cr321_tipo)"
        print(f"[DEBUG USUARIO] URL para ADMIN (sin filtro de correo)")
    else:
        # Usuarios normales solo ven sus conversaciones
        correo = user.get("cr321_correo")
        url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$filter=cr321_correo eq '{correo}'&$orderby=cr321_timestamp desc"
        # Expandir categoría del chatbot si existe el campo
        url += "&$expand=cr321_categoria_chatbot($select=cr321_nombre,cr321_tipo)"
        print(f"[DEBUG USUARIO] URL con filtro de correo: {correo}")

    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # Agrupar por teléfono
            conversations = {}
            for record in data.get("value", []):
                phone = record.get("cr321_phone")
                grupo = record.get("cr321_grupo", "Sin grupo")
                print(
                    f"[DEBUG REGISTRO] Teléfono: {phone}, Grupo: '{grupo}' (tipo: {type(grupo)})"
                )
                if phone and phone not in conversations:
                    conversations[phone] = {
                        "phone": phone,
                        "name": record.get("cr321_fromname", "Desconocido"),
                        "last_message": record.get("cr321_body", ""),
                        "timestamp": record.get("cr321_timestamp"),
                        "grupo": grupo,
                        "unread": 0,
                    }
                    print(
                        f"[DEBUG REGISTRO] Conversación agregada: {phone} - Grupo: {grupo}"
                    )
            return list(conversations.values())
        else:
            print(f"Error Dataverse: {response.status_code} - {response.text}")
        return []
    except Exception as e:
        print(f"Error al consultar conversaciones: {e}")
        return []


def save_incoming_message(data):
    token = get_token()
    if not token:
        print("No se pudo obtener token de acceso.")
        return False
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    try:
        response = requests.post(url, headers=headers, json=data)
        return response.status_code in (200, 201, 204)
    except Exception as e:
        print(f"Error al guardar mensaje: {e}")
        return False


def update_user_settings(user, data):
    token = get_token()
    if not token:
        print("No se pudo obtener token de acceso.")
        return False
    user_id = user.get("cr321_usuariosid")
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuarioses({user_id})"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    try:
        response = requests.patch(url, headers=headers, json=data)
        return response.status_code in (200, 204)
    except Exception as e:
        print(f"Error al actualizar usuario: {e}")
        return False


# Debug temporal: imprimir todos los usuarios si se ejecuta directamente
if __name__ == "__main__":
    print_all_users()
