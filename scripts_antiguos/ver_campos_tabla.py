"""
Script: Ver Todos los Campos de la Tabla cr321_usuarios
========================================================
Lista todos los campos de la tabla para identificar nombres reales
"""
import requests
import os
import sys
from dotenv import load_dotenv

# Cargar .env desde el directorio backend
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend', '.env')
load_dotenv(env_path)

DATAVERSE_URL = os.getenv("DATAVERSE_URL")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")

def get_token():
    """Obtener token de acceso"""
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
    else:
        print(f"❌ Error obteniendo token: {response.status_code}")
        print(f"   Respuesta: {response.text}")
        return None

def listar_campos():
    """Listar todos los campos de cr321_usuarios"""
    token = get_token()
    if not token:
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions(LogicalName='cr321_usuarios')/Attributes"
    url += "?$select=LogicalName,DisplayName,AttributeType,IsCustomAttribute"
    url += "&$filter=IsCustomAttribute eq true"
    
    print("🔍 Consultando campos personalizados de cr321_usuarios...\n")
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        campos = data.get('value', [])
        
        print(f"📊 Total de campos personalizados: {len(campos)}\n")
        print("=" * 80)
        
        # Agrupar por tipo
        campos_por_tipo = {}
        for campo in campos:
            tipo = campo.get('AttributeType', 'Unknown')
            if tipo not in campos_por_tipo:
                campos_por_tipo[tipo] = []
            campos_por_tipo[tipo].append(campo)
        
        # Mostrar campos booleanos primero (son los que nos interesan)
        if 'Boolean' in campos_por_tipo:
            print("\n🔘 CAMPOS BOOLEANOS (Boolean):")
            print("-" * 80)
            for campo in sorted(campos_por_tipo['Boolean'], key=lambda x: x['LogicalName']):
                nombre = campo['LogicalName']
                display = campo.get('DisplayName', {}).get('LocalizedLabels', [{}])[0].get('Label', 'Sin nombre')
                print(f"   • {nombre:30} → {display}")
        
        # Mostrar otros tipos
        for tipo in sorted(campos_por_tipo.keys()):
            if tipo == 'Boolean':
                continue  # Ya lo mostramos
                
            print(f"\n📝 CAMPOS {tipo.upper()}:")
            print("-" * 80)
            for campo in sorted(campos_por_tipo[tipo], key=lambda x: x['LogicalName'])[:15]:  # límite 15 por tipo
                nombre = campo['LogicalName']
                display = campo.get('DisplayName', {}).get('LocalizedLabels', [{}])[0].get('Label', 'Sin nombre')
                print(f"   • {nombre:30} → {display}")
            
            if len(campos_por_tipo[tipo]) > 15:
                print(f"   ... y {len(campos_por_tipo[tipo]) - 15} más")
        
        print("\n" + "=" * 80)
        print("\n💡 Busca los campos booleanos relacionados con grupos en la lista de arriba")
        
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"   Respuesta: {response.text}")

if __name__ == "__main__":
    listar_campos()
