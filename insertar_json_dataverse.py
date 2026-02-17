"""
Script para Insertar JSON en Dataverse
=====================================

Inserta el contenido de ejemplo_json_dataverse.json 
en el campo cr321_config de un registro en cr321_chatbots.
"""

import requests
import json
import os
from pathlib import Path


# ============================================================================
# CONFIGURACIÓN
# ============================================================================

DATAVERSE_URL = os.getenv("DATAVERSE_URL", "https://tu-org.crm.dynamics.com/api/data/v9.2")
CLIENT_ID = os.getenv("CLIENT_ID", "tu-client-id")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "tu-client-secret")
TENANT_ID = os.getenv("TENANT_ID", "tu-tenant-id")

NOMBRE_CHATBOT = "Chatbot1"


# ============================================================================
# FUNCIONES
# ============================================================================

def obtener_token() -> str:
    """Obtiene token OAuth de Microsoft"""
    
    token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": f"{DATAVERSE_URL}/.default",
        "grant_type": "client_credentials"
    }
    
    response = requests.post(token_url, data=data)
    
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"Error obteniendo token: {response.text}")


def cargar_json_ejemplo() -> str:
    """Carga el archivo ejemplo_json_dataverse.json"""
    
    ruta_json = Path(__file__).parent / "ejemplo_json_dataverse.json"
    
    if not ruta_json.exists():
        raise FileNotFoundError(f"No se encontró: {ruta_json}")
    
    with open(ruta_json, 'r', encoding='utf-8') as f:
        return f.read()


def chatbot_existe(headers: dict, nombre: str) -> tuple[bool, str, bool]:
    """
    Verifica si el chatbot ya existe.
    
    Returns:
        (existe: bool, guid: str, activo: bool)
    """
    
    response = requests.get(
        f"{DATAVERSE_URL}/cr321_chatbots",
        headers=headers,
        params={
            "$filter": f"cr321_name eq '{nombre}'",
            "$select": "cr321_chatbotid,cr321_active"
        }
    )
    
    if response.status_code == 200:
        data = response.json()["value"]
        if data:
            return True, data[0]['cr321_chatbotid'], data[0].get('cr321_active', False)
    
    return False, "", False


def crear_chatbot(headers: dict, nombre: str, config_json: str) -> str:
    """
    Crea un nuevo registro de chatbot.
    
    Returns:
        GUID del chatbot creado
    """
    
    data = {
        "cr321_name": nombre,
        "cr321_config": config_json,
        "cr321_active": True  # Activar el chatbot al crearlo
    }
    
    response = requests.post(
        f"{DATAVERSE_URL}/cr321_chatbots",
        headers=headers,
        json=data
    )
    
    if response.status_code == 201:
        return response.json()['cr321_chatbotid']
    else:
        raise Exception(f"Error creando chatbot: {response.text}")


def actualizar_chatbot(headers: dict, guid: str, config_json: str):
    """Actualiza el campo cr321_config de un chatbot existente"""
    
    data = {
        "cr321_config": config_json
    }
    
    response = requests.patch(
        f"{DATAVERSE_URL}/cr321_chatbots({guid})",
        headers=headers,
        json=data
    )
    
    if response.status_code != 204:
        raise Exception(f"Error actualizando chatbot: {response.text}")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Función principal"""
    
    print("="*60)
    print("INSERTAR JSON EN DATAVERSE")
    print("="*60)
    print()
    
    try:
        # 1. Obtener token
        print("→ Obteniendo token...")
        token = obtener_token()
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
        print("  ✓ Token obtenido")
        
        # 2. Cargar JSON de ejemplo
        print("\n→ Cargando JSON de ejemplo...")
        config_json = cargar_json_ejemplo()
        
        # Validar que es JSON válido
        json.loads(config_json)
        
        print(f"  ✓ JSON cargado ({len(config_json)} caracteres)")
        
        # 3. Verificar si chatbot ya existe
        print(f"\n→ Verificando si '{NOMBRE_CHATBOT}' existe...")
        existe, guid, activo = chatbot_existe(headers, NOMBRE_CHATBOT)
        
        if existe:
            estado = "ACTIVO" if activo else "INACTIVO"
            print(f"  ⚠️ Chatbot '{NOMBRE_CHATBOT}' ya existe (GUID: {guid}) - Estado: {estado}")
            print(f"  → ¿Deseas actualizar el campo cr321_config?")
            
            respuesta = input("     Escribe 'si' para continuar: ").strip().lower()
            
            if respuesta != 'si':
                print("\n  ❌ Operación cancelada")
                return
            
            # Actualizar
            print(f"\n→ Actualizando cr321_config...")
            actualizar_chatbot(headers, guid, config_json)
            print(f"  ✓ Campo cr321_config actualizado")
            
        else:
            print(f"  → Chatbot no existe, creando nuevo...")
            
            # Crear nuevo
            print(f"\n→ Creando '{NOMBRE_CHATBOT}'...")
            guid = crear_chatbot(headers, NOMBRE_CHATBOT, config_json)
            print(f"  ✓ Chatbot creado (GUID: {guid})")
        
        # 4. Resumen
        print("\n" + "="*60)
        print("✅ OPERACIÓN EXITOSA")
        print("="*60)
        print(f"\nChatbot: {NOMBRE_CHATBOT}")
        print(f"GUID: {guid}")
        print(f"\nEl JSON se ha insertado en el campo cr321_config")
        print("\nPróximos pasos:")
        print("1. Actualizar los GUIDs de grupos en el JSON")
        print("2. Verificar configuración en Power Apps")
        print("3. Ejecutar: python sistema_menu_json.py")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\nAsegúrate de que existe el archivo:")
        print("  C:\\VS\\BIN\\ejemplo_json_dataverse.json")
    
    except json.JSONDecodeError as e:
        print(f"\n❌ Error: JSON inválido")
        print(f"  {e}")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
