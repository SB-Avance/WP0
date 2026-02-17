"""
Script para Gestionar Estado de Chatbots (Activar/Desactivar)
============================================================

Permite activar o desactivar chatbots cambiando el campo cr321_active.
Solo los chatbots activos serán cargados por el sistema.
"""

import requests
import os


# ============================================================================
# CONFIGURACIÓN
# ============================================================================

DATAVERSE_URL = os.getenv("DATAVERSE_URL", "https://tu-org.crm.dynamics.com/api/data/v9.2")
CLIENT_ID = os.getenv("CLIENT_ID", "tu-client-id")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "tu-client-secret")
TENANT_ID = os.getenv("TENANT_ID", "tu-tenant-id")


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


def listar_chatbots(headers: dict):
    """Lista todos los chatbots con su estado"""
    
    response = requests.get(
        f"{DATAVERSE_URL}/cr321_chatbots",
        headers=headers,
        params={
            "$select": "cr321_chatbotid,cr321_name,cr321_active",
            "$orderby": "cr321_name asc"
        }
    )
    
    if response.status_code == 200:
        return response.json()["value"]
    else:
        raise Exception(f"Error obteniendo chatbots: {response.text}")


def cambiar_estado(headers: dict, guid: str, activo: bool):
    """Cambia el estado activo/inactivo de un chatbot"""
    
    data = {
        "cr321_active": activo
    }
    
    response = requests.patch(
        f"{DATAVERSE_URL}/cr321_chatbots({guid})",
        headers=headers,
        json=data
    )
    
    if response.status_code != 204:
        raise Exception(f"Error actualizando estado: {response.text}")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Función principal"""
    
    print("="*60)
    print("GESTIÓN DE CHATBOTS - ACTIVAR/DESACTIVAR")
    print("="*60)
    print()
    
    try:
        # 1. Obtener token
        print("→ Obteniendo token...")
        token = obtener_token()
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        print("  ✓ Token obtenido")
        
        # 2. Listar chatbots
        print("\n→ Consultando chatbots...")
        chatbots = listar_chatbots(headers)
        
        if not chatbots:
            print("  ⚠️ No se encontraron chatbots")
            return
        
        print(f"  ✓ {len(chatbots)} chatbots encontrados\n")
        
        # 3. Mostrar chatbots
        print("┌" + "─"*58 + "┐")
        print("│ CHATBOTS DISPONIBLES                                     │")
        print("├" + "─"*58 + "┤")
        
        for i, chatbot in enumerate(chatbots, 1):
            nombre = chatbot.get('cr321_name', 'Sin nombre')
            guid = chatbot.get('cr321_chatbotid', 'N/A')
            activo = chatbot.get('cr321_active', False)
            
            estado_emoji = "✅" if activo else "❌"
            estado_texto = "ACTIVO" if activo else "INACTIVO"
            
            print(f"│ {i}. {nombre:<35} {estado_emoji} {estado_texto:<12} │")
            print(f"│    GUID: {guid:<44} │")
            
            if i < len(chatbots):
                print("├" + "─"*58 + "┤")
        
        print("└" + "─"*58 + "┘")
        
        # 4. Menú de acciones
        print("\n" + "="*60)
        print("ACCIONES")
        print("="*60)
        print("\n1. Activar un chatbot")
        print("2. Desactivar un chatbot")
        print("3. Salir")
        
        opcion = input("\nSelecciona una opción (1-3): ").strip()
        
        if opcion == "3":
            print("\n👋 Hasta luego")
            return
        
        if opcion not in ["1", "2"]:
            print("\n❌ Opción inválida")
            return
        
        # 5. Seleccionar chatbot
        print("\n" + "─"*60)
        numero = input("Número del chatbot (1-" + str(len(chatbots)) + "): ").strip()
        
        try:
            idx = int(numero) - 1
            if idx < 0 or idx >= len(chatbots):
                raise ValueError()
        except ValueError:
            print("\n❌ Número inválido")
            return
        
        chatbot_seleccionado = chatbots[idx]
        nombre = chatbot_seleccionado['cr321_name']
        guid = chatbot_seleccionado['cr321_chatbotid']
        activo_actual = chatbot_seleccionado.get('cr321_active', False)
        
        # 6. Confirmar acción
        nuevo_estado = (opcion == "1")
        accion = "ACTIVAR" if nuevo_estado else "DESACTIVAR"
        
        if activo_actual == nuevo_estado:
            estado_actual_texto = "ACTIVO" if activo_actual else "INACTIVO"
            print(f"\n⚠️ El chatbot '{nombre}' ya está {estado_actual_texto}")
            return
        
        print(f"\n¿Deseas {accion} el chatbot '{nombre}'?")
        confirmar = input("Escribe 'si' para continuar: ").strip().lower()
        
        if confirmar != 'si':
            print("\n❌ Operación cancelada")
            return
        
        # 7. Cambiar estado
        print(f"\n→ {accion}ndo chatbot...")
        cambiar_estado(headers, guid, nuevo_estado)
        
        print(f"  ✓ Chatbot '{nombre}' {accion}do exitosamente")
        
        # 8. Mensaje informativo
        print("\n" + "="*60)
        print("✅ OPERACIÓN EXITOSA")
        print("="*60)
        
        if nuevo_estado:
            print(f"\nEl chatbot '{nombre}' ahora está ACTIVO")
            print("→ El sistema lo cargará automáticamente")
        else:
            print(f"\nEl chatbot '{nombre}' ahora está INACTIVO")
            print("→ El sistema NO lo cargará")
            print("⚠️ Si era el chatbot activo, el sistema fallará al iniciar")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
