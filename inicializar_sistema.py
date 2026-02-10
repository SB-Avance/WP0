"""
Script de inicialización del sistema WhatsApp CRM
Crea los grupos tipo "A" y el chatbot principal

Este script debe ejecutarse UNA SOLA VEZ después de crear las tablas en Dataverse
"""
import requests
import os
from dotenv import load_dotenv
from msal import ConfidentialClientApplication

# Cargar .env desde el directorio backend
env_path = os.path.join(os.path.dirname(__file__), 'backend', '.env')
load_dotenv(env_path)

# Variables de entorno
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
DATAVERSE_URL = os.getenv("DATAVERSE_URL")


def get_token():
    """Obtiene token de autenticación de Dataverse"""
    authority = f"https://login.microsoftonline.com/{TENANT_ID}"
    scope = [f"{DATAVERSE_URL}/.default"]
    
    app = ConfidentialClientApplication(
        CLIENT_ID,
        authority=authority,
        client_credential=CLIENT_SECRET
    )
    
    result = app.acquire_token_for_client(scopes=scope)
    
    if "access_token" in result:
        return result["access_token"]
    else:
        print(f"Error obteniendo token: {result.get('error_description')}")
        return None


def check_grupos_exist(token):
    """Verifica cuáles grupos tipo A ya existen"""
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_grups?$filter=cr321_tipo eq 462410000&$select=cr321_nombre"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            grupos_existentes = [g.get("cr321_nombre") for g in data.get("value", [])]
            return grupos_existentes
        return []
    except Exception as e:
        print(f"Error verificando grupos: {e}")
        return []


def create_grupos_iniciales(token):
    """Crea solo los grupos tipo A que faltan para el menú de WhatsApp"""
    # Obtener grupos existentes
    grupos_existentes = check_grupos_exist(token)
    print(f"  Grupos existentes: {len(grupos_existentes)}")
    for g in grupos_existentes:
        print(f"    - {g}")
    
    grupos = [
        {
            "cr321_nombre": "Solicitud Ticket",
            "cr321_tipo": 462410000,  # Tipo A
            "cr321_descripcion": "Crear ticket de solicitud de soporte técnico"
        },
        {
            "cr321_nombre": "Cotizaciones",
            "cr321_tipo": 462410000,  # Tipo A
            "cr321_descripcion": "Solicitar cotización de productos o servicios"
        },
        {
            "cr321_nombre": "Información",
            "cr321_tipo": 462410000,  # Tipo A
            "cr321_descripcion": "Obtener información general de la empresa"
        },
        {
            "cr321_nombre": "Solicitar atención de agente",
            "cr321_tipo": 462410000,  # Tipo A
            "cr321_descripcion": "Conectarse con un agente humano"
        }
    ]
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_grups"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    created = 0
    skipped = 0
    for grupo in grupos:
        # Verificar si el grupo ya existe
        if grupo["cr321_nombre"] in grupos_existentes:
            print(f"[SALTAR] Grupo ya existe: {grupo['cr321_nombre']}")
            skipped += 1
            continue
            
        try:
            response = requests.post(url, json=grupo, headers=headers, timeout=10)
            if response.status_code in [200, 201, 204]:
                print(f"[OK] Grupo creado: {grupo['cr321_nombre']}")
                created += 1
            else:
                print(f"[ERROR] No se pudo crear '{grupo['cr321_nombre']}': {response.status_code}")
                print(f"  Detalle: {response.text}")
        except Exception as e:
            print(f"[ERROR] Excepción al crear '{grupo['cr321_nombre']}': {e}")
    
    print(f"\n  Resumen: {created} creados, {skipped} ya existían")
    return created > 0


def check_chatbot_exist(token):
    """Verifica si ya existe el chatbot principal"""
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_chatbots?$filter=contains(cr321_name, 'Menu Principal')&$top=1"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return len(data.get("value", [])) > 0
        return False
    except Exception as e:
        print(f"Error verificando chatbot: {e}")
        return False


def create_chatbot_principal(token):
    """Crea el chatbot principal del menú de WhatsApp"""
    # Config simplificado para caber en 100 caracteres
    chatbot_config = '{"menu_dinamico":true,"fuente":"cr321_grup","tipo":"A"}'
    
    chatbot = {
        "cr321_name": "Menu Principal WhatsApp",
        "cr321_type": 462410000,  # FlowBot
        "cr321_config": chatbot_config,
        "cr321_active": True
    }
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_chatbots"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    try:
        response = requests.post(url, json=chatbot, headers=headers, timeout=10)
        if response.status_code in [200, 201, 204]:
            print(f"[OK] Chatbot 'Menu Principal WhatsApp' creado exitosamente")
            return True
        else:
            print(f"[ERROR] No se pudo crear el chatbot: {response.status_code}")
            print(f"  Detalle: {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Excepción al crear chatbot: {e}")
        return False


def main():
    print("=" * 60)
    print("   INICIALIZACION DEL SISTEMA WHATSAPP CRM")
    print("=" * 60)
    print()
    
    # Obtener token
    print("[1/4] Obteniendo token de autenticación...")
    token = get_token()
    if not token:
        print("[ERROR] No se pudo obtener token de autenticación")
        print("  Verifica las variables de entorno en .env:")
        print("    - CLIENT_ID")
        print("    - CLIENT_SECRET")
        print("    - TENANT_ID")
        print("    - DATAVERSE_URL")
        return
    print("[OK] Token obtenido exitosamente")
    print()
    
    # Verificar y crear grupos
    print("[2/4] Verificando grupos tipo A...")
    create_grupos_iniciales(token)
    print()
    
    # Verificar y crear chatbot
    print("[3/4] Verificando chatbot principal...")
    if check_chatbot_exist(token):
        print("[AVISO] Ya existe un chatbot principal. No se creara duplicado.")
        print("  Si desea recrearlo, elimine el chatbot existente primero.")
    else:
        print("[INFO] No se encontro chatbot principal. Creando...")
        if create_chatbot_principal(token):
            print("[OK] Chatbot principal creado exitosamente")
        else:
            print("[ERROR] No se pudo crear el chatbot principal")
    print()
    
    # Resumen
    print("[4/4] Inicialización completada")
    print()
    print("SIGUIENTE PASO:")
    print("  1. Verifica los grupos en make.powerapps.com -> Dataverse -> Tablas -> Grupos")
    print("  2. Verifica el chatbot en la interfaz de administración")
    print("  3. Reinicia el backend: .\\iniciar_backend.ps1")
    print("  4. El menú de WhatsApp ahora se cargará dinámicamente")
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
