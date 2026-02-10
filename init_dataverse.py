"""
Script de inicialización de datos para Dataverse
Crea grupos y estados iniciales del sistema

Ejecutar: python init_dataverse.py
"""
import sys
import os

# Cargar variables de entorno desde backend/.env
from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend', '.env')
load_dotenv(env_path)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
DATAVERSE_URL = os.getenv("DATAVERSE_URL")

from msal import ConfidentialClientApplication
import requests


def get_token():
    """Obtener token de autenticación de Dataverse"""
    try:
        authority = f"https://login.microsoftonline.com/{TENANT_ID}"
        app = ConfidentialClientApplication(
            CLIENT_ID,
            authority=authority,
            client_credential=CLIENT_SECRET
        )
        result = app.acquire_token_for_client(scopes=[f"{DATAVERSE_URL}/.default"])
        
        if "access_token" in result:
            return result["access_token"]
        else:
            print(f"❌ Error al obtener token: {result.get('error_description', 'Unknown')}")
            return None
    except Exception as e:
        print(f"❌ Excepción al obtener token: {e}")
        return None


def create_initial_grupos():
    """Crear grupos iniciales tipo A (opciones de menú)"""
    token = get_token()
    if not token:
        print("❌ No se pudo obtener token de autenticación")
        return False
    
    grupos_iniciales = [
        {
            "cr321_idgrupo": 1,
            "cr321_nombre": "Solicitud Ticket",
            "cr321_tipo": 462410000,  # Tipo A
            "cr321_descripcion": "Grupo para solicitudes de soporte técnico"
        },
        {
            "cr321_idgrupo": 2,
            "cr321_nombre": "Cotizaciones",
            "cr321_tipo": 462410000,  # Tipo A
            "cr321_descripcion": "Grupo para solicitudes de cotización"
        },
        {
            "cr321_idgrupo": 3,
            "cr321_nombre": "Información",
            "cr321_tipo": 462410000,  # Tipo A
            "cr321_descripcion": "Grupo para consultas de información general"
        },
        {
            "cr321_idgrupo": 4,
            "cr321_nombre": "Atención de Agente",
            "cr321_tipo": 462410000,  # Tipo A
            "cr321_descripcion": "Grupo para solicitar atención directa de un agente"
        }
    ]
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_grups"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    print("\n📋 Creando grupos iniciales...")
    print("-" * 50)
    
    for grupo in grupos_iniciales:
        # Verificar si ya existe
        check_url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_grups?$filter=cr321_idgrupo eq {grupo['cr321_idgrupo']}"
        check_response = requests.get(check_url, headers={"Authorization": f"Bearer {token}", "Accept": "application/json"})
        
        if check_response.status_code == 200:
            existing = check_response.json().get("value", [])
            if existing:
                print(f"⏭️  Grupo '{grupo['cr321_nombre']}' ya existe (ID: {grupo['cr321_idgrupo']})")
                continue
        
        try:
            response = requests.post(url, json=grupo, headers=headers)
            if response.status_code == 204:
                print(f"✅ Grupo '{grupo['cr321_nombre']}' creado (ID: {grupo['cr321_idgrupo']})")
            else:
                print(f"❌ Error creando grupo '{grupo['cr321_nombre']}': {response.status_code}")
                print(f"   Detalles: {response.text}")
        except Exception as e:
            print(f"❌ Excepción creando grupo '{grupo['cr321_nombre']}': {e}")
    
    return True


def create_initial_estados():
    """Crear estados iniciales para tickets"""
    token = get_token()
    if not token:
        print("❌ No se pudo obtener token de autenticación")
        return False
    
    estados_iniciales = [
        {
            "cr321_idestado": 1,
            "cr321_nombre": "Nuevo",
            "cr321_descripcion": "Ticket recién creado, pendiente de asignación"
        },
        {
            "cr321_idestado": 2,
            "cr321_nombre": "En Proceso",
            "cr321_descripcion": "Ticket asignado y en proceso de resolución"
        },
        {
            "cr321_idestado": 3,
            "cr321_nombre": "Pendiente Cliente",
            "cr321_descripcion": "Esperando respuesta o información del cliente"
        },
        {
            "cr321_idestado": 4,
            "cr321_nombre": "Resuelto",
            "cr321_descripcion": "Ticket resuelto exitosamente"
        },
        {
            "cr321_idestado": 5,
            "cr321_nombre": "Cerrado",
            "cr321_descripcion": "Ticket cerrado y archivado"
        },
        {
            "cr321_idestado": 6,
            "cr321_nombre": "Cancelado",
            "cr321_descripcion": "Ticket cancelado por el cliente o por política interna"
        }
    ]
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_estados"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    print("\n📊 Creando estados iniciales...")
    print("-" * 50)
    
    for estado in estados_iniciales:
        # Verificar si ya existe
        check_url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_estados?$filter=cr321_idestado eq {estado['cr321_idestado']}"
        check_response = requests.get(check_url, headers={"Authorization": f"Bearer {token}", "Accept": "application/json"})
        
        if check_response.status_code == 200:
            existing = check_response.json().get("value", [])
            if existing:
                print(f"⏭️  Estado '{estado['cr321_nombre']}' ya existe (ID: {estado['cr321_idestado']})")
                continue
        
        try:
            response = requests.post(url, json=estado, headers=headers)
            if response.status_code == 204:
                print(f"✅ Estado '{estado['cr321_nombre']}' creado (ID: {estado['cr321_idestado']})")
            else:
                print(f"❌ Error creando estado '{estado['cr321_nombre']}': {response.status_code}")
                print(f"   Detalles: {response.text}")
        except Exception as e:
            print(f"❌ Excepción creando estado '{estado['cr321_nombre']}': {e}")
    
    return True


def main():
    print("\n" + "=" * 50)
    print("🚀 INICIALIZACIÓN DE DATAVERSE")
    print("=" * 50)
    
    # Crear grupos
    if not create_initial_grupos():
        print("\n❌ Error al crear grupos")
        return
    
    # Crear estados
    if not create_initial_estados():
        print("\n❌ Error al crear estados")
        return
    
    print("\n" + "=" * 50)
    print("✅ INICIALIZACIÓN COMPLETADA")
    print("=" * 50)
    print("\nResumen:")
    print("  - 4 grupos tipo A creados (opciones de menú)")
    print("  - 6 estados de ticket creados")
    print("\nPróximos pasos:")
    print("  1. Asignar usuarios a grupos usando API: POST /api/usuario-grupos")
    print("  2. Configurar webhook de WhatsApp para recibir mensajes")
    print("  3. Iniciar el backend: python backend/back.py")
    print()


if __name__ == "__main__":
    main()
