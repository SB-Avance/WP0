"""
Script de Implementación Completa
==================================

Ejecuta todos los pasos necesarios para implementar el sistema:
1. Inserta JSON en Dataverse
2. Valida grupos
3. Activa chatbot
4. Inicia el sistema
"""

import requests
import json
import os
import sys
from pathlib import Path


# ============================================================================
# CONFIGURACIÓN
# ============================================================================

DATAVERSE_URL = os.getenv("DATAVERSE_URL", "https://tu-org.crm.dynamics.com/api/data/v9.2")
CLIENT_ID = os.getenv("CLIENT_ID", "tu-client-id")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "tu-client-secret")
TENANT_ID = os.getenv("TENANT_ID", "tu-tenant-id")

NOMBRE_CHATBOT = "Chatbot1"
JSON_FILE = "JSON_LISTO_PARA_INSERTAR.json"


# ============================================================================
# FUNCIONES
# ============================================================================

def print_step(step, title):
    """Imprime encabezado de paso"""
    print("\n" + "="*60)
    print(f"PASO {step}: {title}")
    print("="*60)


def obtener_token() -> str:
    """Obtiene token OAuth de Microsoft"""
    
    print("→ Obteniendo token de autenticación...")
    
    token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": f"{DATAVERSE_URL}/.default",
        "grant_type": "client_credentials"
    }
    
    try:
        response = requests.post(token_url, data=data)
        
        if response.status_code == 200:
            print("  ✓ Token obtenido exitosamente")
            return response.json()["access_token"]
        else:
            raise Exception(f"Error obteniendo token: {response.text}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        raise


def insertar_json_dataverse(headers: dict) -> str:
    """
    Inserta o actualiza el JSON en Dataverse.
    Returns: chatbot_id
    """
    
    print(f"\n→ Insertando configuración JSON para '{NOMBRE_CHATBOT}'...")
    
    # Leer JSON
    if not Path(JSON_FILE).exists():
        raise Exception(f"Archivo no encontrado: {JSON_FILE}")
    
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        config_json = f.read()
    
    # Verificar si existe
    response = requests.get(
        f"{DATAVERSE_URL}/cr321_chatbots",
        headers=headers,
        params={"$filter": f"cr321_name eq '{NOMBRE_CHATBOT}'"}
    )
    
    if response.status_code == 200:
        data = response.json()["value"]
        
        if data:
            # Actualizar existente
            chatbot_id = data[0]['cr321_chatbotid']
            print(f"  → Actualizando chatbot existente...")
            
            response = requests.patch(
                f"{DATAVERSE_URL}/cr321_chatbots({chatbot_id})",
                headers=headers,
                json={
                    "cr321_config": config_json,
                    "cr321_active": True
                }
            )
            
            if response.status_code == 204:
                print(f"  ✓ Chatbot '{NOMBRE_CHATBOT}' actualizado exitosamente")
                return chatbot_id
            else:
                raise Exception(f"Error actualizando: {response.text}")
        else:
            # Crear nuevo
            print(f"  → Creando nuevo chatbot...")
            
            response = requests.post(
                f"{DATAVERSE_URL}/cr321_chatbots",
                headers=headers,
                json={
                    "cr321_name": NOMBRE_CHATBOT,
                    "cr321_config": config_json,
                    "cr321_active": True
                }
            )
            
            if response.status_code == 201:
                chatbot_id = response.json()["cr321_chatbotid"]
                print(f"  ✓ Chatbot '{NOMBRE_CHATBOT}' creado exitosamente")
                return chatbot_id
            else:
                raise Exception(f"Error creando: {response.text}")
    else:
        raise Exception(f"Error consultando chatbots: {response.text}")


def validar_grupos(headers: dict):
    """Valida que todos los grupos del menú existan"""
    
    print("\n→ Validando grupos del menú...")
    
    # Obtener grupos válidos
    response = requests.get(
        f"{DATAVERSE_URL}/cr321_grupos",
        headers=headers,
        params={"$select": "cr321_grupoid,cr321_nombre"}
    )
    
    if response.status_code != 200:
        raise Exception(f"Error obteniendo grupos: {response.text}")
    
    grupos_validos = {
        g['cr321_grupoid'].lower(): g.get('cr321_nombre', 'Sin nombre')
        for g in response.json()["value"]
    }
    
    print(f"  → {len(grupos_validos)} grupos disponibles en Dataverse")
    
    # Obtener config del chatbot
    response = requests.get(
        f"{DATAVERSE_URL}/cr321_chatbots",
        headers=headers,
        params={
            "$filter": f"cr321_name eq '{NOMBRE_CHATBOT}' and cr321_active eq true",
            "$select": "cr321_config"
        }
    )
    
    if response.status_code != 200:
        raise Exception(f"Error obteniendo config: {response.text}")
    
    data = response.json()["value"]
    if not data:
        raise Exception(f"No se encontró chatbot activo: {NOMBRE_CHATBOT}")
    
    config = json.loads(data[0]['cr321_config'])
    
    # Validar cada grupo_id
    invalidos = []
    validos = 0
    
    for menu in config.get('menus', []):
        for submenu in menu.get('submenus', []):
            grupo_id = submenu.get('grupo_id')
            
            if grupo_id and grupo_id != "null" and grupo_id is not None:
                guid_limpio = grupo_id.strip('{}').lower()
                
                if guid_limpio in grupos_validos:
                    validos += 1
                else:
                    invalidos.append({
                        'numero': submenu.get('numero'),
                        'nombre': submenu.get('nombre'),
                        'grupo_id': grupo_id
                    })
    
    if invalidos:
        print(f"  ❌ {len(invalidos)} grupo(s) inválido(s):")
        for item in invalidos[:3]:
            print(f"     - {item['numero']}: {item['nombre']}")
        raise Exception("Grupos inválidos detectados")
    else:
        print(f"  ✓ Todos los grupos válidos ({validos} verificados)")


def mostrar_resumen(chatbot_id: str):
    """Muestra resumen de la implementación"""
    
    print("\n" + "="*60)
    print("✅ IMPLEMENTACIÓN COMPLETADA")
    print("="*60)
    print(f"\nChatbot ID: {chatbot_id}")
    print(f"Nombre: {NOMBRE_CHATBOT}")
    print(f"Estado: ✅ ACTIVO")
    print(f"Config: ✅ JSON insertado")
    print(f"Grupos: ✅ Validados")
    print("\n" + "="*60)


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Función principal"""
    
    print("="*60)
    print("IMPLEMENTACIÓN COMPLETA DEL SISTEMA")
    print("="*60)
    
    try:
        # PASO 1: Obtener token
        print_step(1, "Autenticación")
        token = obtener_token()
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # PASO 2: Insertar JSON
        print_step(2, "Insertar Configuración JSON")
        chatbot_id = insertar_json_dataverse(headers)
        
        # PASO 3: Validar grupos
        print_step(3, "Validar Grupos")
        validar_grupos(headers)
        
        # PASO 4: Resumen
        mostrar_resumen(chatbot_id)
        
        print("\n🚀 Sistema listo para usar!")
        print("\nPróximo paso:")
        print("  python sistema_menu_json.py")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error durante implementación: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
