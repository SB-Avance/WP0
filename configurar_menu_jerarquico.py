"""
CONFIGURAR DATAVERSE PARA MENÚ JERÁRQUICO
==========================================

Este script agrega los campos necesarios a la tabla cr321_chatbots
para soportar el menú jerárquico con grupos por subopción.

Campos nuevos a agregar:
- cr321_orden: Orden de la categoría (1, 2, 3)
- cr321_grupo1: Grupo asignado al elemento1
- cr321_grupo2: Grupo asignado al elemento2
- cr321_grupo3: Grupo asignado al elemento3
- cr321_grupo4: Grupo asignado al elemento4
- cr321_grupo5: Grupo asignado al elemento5
"""
import requests
import sys
sys.path.append('backend')
from goot import DATAVERSE_URL, CLIENT_ID, CLIENT_SECRET, TENANT_ID


def get_token():
    """Obtiene token de autenticación"""
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": f"{DATAVERSE_URL}/.default",
        "grant_type": "client_credentials"
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    return None


def poblar_datos_ejemplo(token):
    """
    Pobla la tabla cr321_chatbots con datos de ejemplo para el menú jerárquico
    """
    print("\n" + "="*70)
    print("POBLANDO DATOS DE EJEMPLO")
    print("="*70)
    
    # Primero, desactivar todos los chatbots existentes
    print("\n⏳ Desactivando chatbots existentes...")
    url_get = f"{DATAVERSE_URL}/api/data/v9.2/cr321_chatbots?$select=cr321_chatbotid"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url_get, headers=headers, timeout=10)
        if response.status_code == 200:
            chatbots_existentes = response.json().get("value", [])
            for cb in chatbots_existentes:
                chatbot_id = cb.get("cr321_chatbotid")
                url_update = f"{DATAVERSE_URL}/api/data/v9.2/cr321_chatbots({chatbot_id})"
                requests.patch(url_update, json={"cr321_active": False}, headers=headers, timeout=10)
            print(f"✅ {len(chatbots_existentes)} chatbots desactivados")
    except Exception as e:
        print(f"⚠️  Error desactivando chatbots: {e}")
    
    # Datos de ejemplo para el menú jerárquico
    chatbots_ejemplo = [
        {
            "cr321_name": "Solicitud Ticket",
            "cr321_type": 462410000,  # FlowBot
            "cr321_active": True,
            "cr321_orden": 1,
            "cr321_elemento1": "Soporte Técnico",
            "cr321_elemento2": "Garantías",
            "cr321_elemento3": "Consultas Generales",
            "cr321_grupo1": "Soporte Técnico",
            "cr321_grupo2": "Garantías",
            "cr321_grupo3": "Consultas",
            "cr321_config": '{"menu":"jerarquico","nivel":"principal"}'
        },
        {
            "cr321_name": "Ventas",
            "cr321_type": 462410000,
            "cr321_active": True,
            "cr321_orden": 2,
            "cr321_elemento1": "Cotización",
            "cr321_elemento2": "Catálogo",
            "cr321_elemento3": "Seguimiento",
            "cr321_grupo1": "Ventas - Cotización",
            "cr321_grupo2": "Ventas - Catálogo",
            "cr321_grupo3": "Ventas - Seguimiento",
            "cr321_config": '{"menu":"jerarquico","nivel":"principal"}'
        },
        {
            "cr321_name": "Solicitar Atención",
            "cr321_type": 462410000,
            "cr321_active": True,
            "cr321_orden": 3,
            "cr321_elemento1": "Agente Disponible",
            "cr321_elemento2": "Agendar Cita",
            "cr321_grupo1": "Atención Inmediata",
            "cr321_grupo2": "Agendamiento",
            "cr321_config": '{"menu":"jerarquico","nivel":"principal"}'
        }
    ]
    
    url_create = f"{DATAVERSE_URL}/api/data/v9.2/cr321_chatbots"
    
    print("\n⏳ Creando chatbots de ejemplo...")
    creados = 0
    
    for chatbot in chatbots_ejemplo:
        try:
            response = requests.post(url_create, json=chatbot, headers=headers, timeout=10)
            if response.status_code in [200, 201, 204]:
                print(f"✅ Creado: {chatbot['cr321_name']}")
                creados += 1
            else:
                print(f"❌ Error creando '{chatbot['cr321_name']}': HTTP {response.status_code}")
                print(f"   Detalle: {response.text[:200]}")
        except Exception as e:
            print(f"❌ Excepción creando '{chatbot['cr321_name']}': {e}")
    
    print(f"\n✅ {creados}/{len(chatbots_ejemplo)} chatbots creados exitosamente")
    
    return creados > 0


def verificar_estructura():
    """Verifica que los campos necesarios existen en la tabla"""
    print("\n" + "="*70)
    print("VERIFICANDO ESTRUCTURA")
    print("="*70)
    
    token = get_token()
    if not token:
        print("❌ No se pudo obtener token")
        return False
    
    # Intentar consultar con los nuevos campos
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_chatbots"
    url += "?$select=cr321_orden,cr321_grupo1,cr321_grupo2,cr321_grupo3,cr321_grupo4,cr321_grupo5"
    url += "&$top=1"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            print("✅ Todos los campos necesarios existen:")
            print("   - cr321_orden")
            print("   - cr321_grupo1")
            print("   - cr321_grupo2")
            print("   - cr321_grupo3")
            print("   - cr321_grupo4")
            print("   - cr321_grupo5")
            return True
        else:
            print(f"⚠️  Error HTTP {response.status_code}")
            print("   Algunos campos pueden no existir")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Función principal"""
    print("="*70)
    print("CONFIGURACIÓN DE DATAVERSE PARA MENÚ JERÁRQUICO")
    print("="*70)
    
    print("\n📋 INFORMACIÓN:")
    print("   Este script configurará la tabla cr321_chatbots con:")
    print("   - 3 opciones principales del menú")
    print("   - Subopciones con grupos asignados")
    print("   - Campo cr321_orden para orden personalizado")
    print("   - Campos cr321_grupoX para asignación de grupos")
    
    print("\n⚠️  IMPORTANTE:")
    print("   Si los campos cr321_orden y cr321_grupoX no existen,")
    print("   necesitas crearlos manualmente en Power Apps:")
    print()
    print("   1. Ve a https://make.powerapps.com")
    print("   2. Abre la tabla cr321_chatbots")
    print("   3. Agrega estos campos:")
    print("      - cr321_orden (Whole Number)")
    print("      - cr321_grupo1 (Text)")
    print("      - cr321_grupo2 (Text)")
    print("      - cr321_grupo3 (Text)")
    print("      - cr321_grupo4 (Text)")
    print("      - cr321_grupo5 (Text)")
    
    continuar = input("\n¿Deseas continuar con la configuración? (s/n): ")
    
    if continuar.lower() != 's':
        print("\n❌ Configuración cancelada")
        return
    
    # Obtener token
    print("\n[1/3] Obteniendo token...")
    token = get_token()
    if not token:
        print("❌ Error obteniendo token")
        return
    print("✅ Token obtenido")
    
    # Verificar estructura
    print("\n[2/3] Verificando estructura de la tabla...")
    estructura_ok = verificar_estructura()
    
    if not estructura_ok:
        print("\n⚠️  La estructura puede no estar completa.")
        print("   El script intentará crear los datos de todas formas.")
        continuar = input("   ¿Continuar? (s/n): ")
        if continuar.lower() != 's':
            print("\n❌ Configuración cancelada")
            return
    
    # Poblar datos
    print("\n[3/3] Poblando datos de ejemplo...")
    exito = poblar_datos_ejemplo(token)
    
    # Resumen final
    print("\n" + "="*70)
    print("RESUMEN")
    print("="*70)
    
    if exito:
        print("\n✅ CONFIGURACIÓN COMPLETADA EXITOSAMENTE")
        print("\nPróximos pasos:")
        print("  1. Prueba el sistema: python sistema_menu_jerarquico.py")
        print("  2. Integra con tu backend Flask")
        print("  3. Prueba con WhatsApp real")
        print("\n💡 Para verificar el menú:")
        print("   python probar_menu_jerarquico.py")
    else:
        print("\n⚠️  CONFIGURACIÓN COMPLETADA CON ERRORES")
        print("\nRevisiones necesarias:")
        print("  1. Verifica que la tabla cr321_chatbots existe")
        print("  2. Verifica que los campos cr321_orden y cr321_grupoX existen")
        print("  3. Verifica las credenciales en backend/.env")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Configuración interrumpida por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
