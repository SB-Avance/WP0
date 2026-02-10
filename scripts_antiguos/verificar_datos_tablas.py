"""
Script para verificar si hay datos en las tablas
"""
import os
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
    """Obtener token"""
    try:
        authority = f"https://login.microsoftonline.com/{TENANT_ID}"
        app = ConfidentialClientApplication(
            CLIENT_ID,
            authority=authority,
            client_credential=CLIENT_SECRET
        )
        result = app.acquire_token_for_client(scopes=[f"{DATAVERSE_URL}/.default"])
        return result.get("access_token") if "access_token" in result else None
    except Exception as e:
        return None

def contar_registros(token, table_name):
    """Contar registros en una tabla"""
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/{table_name}?$select=cr321_{table_name.replace('cr321_', '')}id&$count=true&$top=1"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Prefer": "odata.include-annotations=*"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get('@odata.count', 0)
        else:
            return None
    except Exception as e:
        return None

def main():
    print("=" * 70)
    print("📊 VERIFICAR DATOS EN TABLAS")
    print("=" * 70)
    
    token = get_token()
    if not token:
        print("❌ No se pudo obtener token")
        return
    
    tablas = [
        ('cr321_grupo1ses', 'cr321_grupo1 (INCORRECTA)'),
        ('cr321_grups', 'cr321_grup (CORRECTA)'),
        ('cr321_usuariogrupos', 'cr321_usuariogrupo')
    ]
    
    print()
    resultados = {}
    
    for tabla_api, tabla_nombre in tablas:
        count = contar_registros(token, tabla_api)
        resultados[tabla_nombre] = count
        
        if count is None:
            print(f"❓ {tabla_nombre:35} - Sin acceso para leer")
        elif count == 0:
            print(f"✅ {tabla_nombre:35} - {count} registros (VACÍA)")
        else:
            print(f"⚠️  {tabla_nombre:35} - {count} registros")
    
    print("\n" + "=" * 70)
    print("📋 RECOMENDACIÓN:")
    print("=" * 70)
    
    grupo1_count = resultados.get('cr321_grupo1 (INCORRECTA)', 0)
    grupos_count = resultados.get('cr321_grup (CORRECTA)', 0)
    usuario_count = resultados.get('cr321_usuariogrupo', 0)
    
    if grupo1_count == 0 and usuario_count == 0:
        print("✅ FÁCIL: Ambas tablas están vacías")
        print()
        print("Pasos simplificados:")
        print("1. Eliminar el campo cr321_grupoid de cr321_usuariogrupo")
        print("2. Crear nuevo campo que apunte a cr321_grup")
        print("3. Eliminar la tabla cr321_grupo1")
        print()
        print("No hay datos que migrar ✅")
    else:
        print("⚠️  COMPLEJO: Hay datos que migrar")
        print()
        print("Necesitas:")
        print("1. Crear el nuevo campo en cr321_usuariogrupo")
        print("2. Migrar manualmente los registros")
        print("3. Luego eliminar el campo viejo")
        print("4. Finalmente eliminar cr321_grupo1")
    
    print("=" * 70)

if __name__ == "__main__":
    main()
