"""
Verificar registros en tabla cr321_chatbot
"""
import requests
import json
import os
import sys

# Cargar configuración desde backend
sys.path.append('backend')
from goot import DATAVERSE_URL, CLIENT_ID, CLIENT_SECRET, TENANT_ID

def get_token():
    """Obtener token de autenticación"""
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

def verificar_chatbots():
    """Verificar registros en cr321_chatbots"""
    token = get_token()
    if not token:
        print("❌ No se pudo obtener token")
        return
    
    # Consultar todos los chatbots
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_chatbots"
    url += "?$select=cr321_chatbotid,cr321_name,cr321_active,cr321_elemento1,cr321_elemento2,cr321_elemento3,cr321_elemento4,cr321_elemento5"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
    print("\n" + "="*70)
    print("VERIFICACIÓN DE TABLA cr321_chatbot")
    print("="*70)
    
    response = requests.get(url, headers=headers, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        chatbots = data.get("value", [])
        
        print(f"\n📊 Total de registros: {len(chatbots)}")
        
        if not chatbots:
            print("\n⚠️  NO HAY REGISTROS EN cr321_chatbots")
            print("\nAcciones recomendadas:")
            print("1. Crear al menos un registro en Dataverse")
            print("2. Configurar los campos:")
            print("   - cr321_name: Nombre del chatbot")
            print("   - cr321_active: true (activo)")
            print("   - cr321_elemento1-5: Opciones del menú")
            return
        
        activos = [c for c in chatbots if c.get("cr321_active")]
        
        print(f"✅ Registros activos: {len(activos)}")
        print(f"⏸️  Registros inactivos: {len(chatbots) - len(activos)}")
        
        print("\n" + "-"*70)
        print("REGISTROS ACTIVOS:")
        print("-"*70)
        
        for idx, chatbot in enumerate(activos, 1):
            print(f"\n[{idx}] {chatbot.get('cr321_name', 'Sin nombre')}")
            print(f"    ID: {chatbot.get('cr321_chatbotid')}")
            print(f"    Activo: {'✅ Sí' if chatbot.get('cr321_active') else '❌ No'}")
            print(f"    Elementos del menú:")
            
            elementos = []
            for i in range(1, 6):
                elem = chatbot.get(f"cr321_elemento{i}")
                if elem and elem.strip():
                    elementos.append(f"      [{i}] {elem}")
            
            if elementos:
                print("\n".join(elementos))
            else:
                print("      ⚠️  No hay elementos configurados")
        
        if len(chatbots) > len(activos):
            print("\n" + "-"*70)
            print("REGISTROS INACTIVOS:")
            print("-"*70)
            
            inactivos = [c for c in chatbots if not c.get("cr321_active")]
            for idx, chatbot in enumerate(inactivos, 1):
                print(f"  [{idx}] {chatbot.get('cr321_name', 'Sin nombre')} (ID: {chatbot.get('cr321_chatbotid')})")
        
        print("\n" + "="*70)
        print("RESUMEN:")
        print("="*70)
        
        if activos:
            primer_activo = activos[0]
            elementos_configurados = sum(1 for i in range(1, 6) if primer_activo.get(f"cr321_elemento{i}"))
            
            print(f"✅ Se cargará el chatbot: {primer_activo.get('cr321_name')}")
            print(f"✅ Opciones de menú disponibles: {elementos_configurados}")
            
            if elementos_configurados == 0:
                print("\n⚠️  ADVERTENCIA: El chatbot activo no tiene elementos configurados")
                print("   El sistema usará el menú por defecto")
        else:
            print("❌ NO HAY CHATBOTS ACTIVOS")
            print("   El sistema usará el menú por defecto hardcodeado")
        
    else:
        print(f"\n❌ Error al consultar chatbots: HTTP {response.status_code}")
        print(f"   Respuesta: {response.text}")

if __name__ == "__main__":
    verificar_chatbots()
