"""
Análisis: Relación entre chats00.grupo y grup.tipo
====================================================
Analiza el campo cr321_grupo actual en chats00 y propone 
cómo relacionarlo con la tabla grup campo tipo
"""
import requests
import os
from dotenv import load_dotenv
from collections import Counter

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
        return None

def analizar_campo_grupo_chats():
    """Analiza el campo cr321_grupo actual en chats00"""
    token = get_token()
    if not token:
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("=" * 80)
    print("📊 ANÁLISIS: Campo cr321_grupo en chats00 (cr321_adatawp0s)")
    print("=" * 80)
    
    # 1. Ver metadata del campo cr321_grupo
    print("\n🔍 1. METADATA DEL CAMPO cr321_grupo:\n")
    metadata_url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions(LogicalName='cr321_adatawp0')/Attributes(LogicalName='cr321_grupo')"
    
    response = requests.get(metadata_url, headers=headers)
    
    if response.status_code == 200:
        campo = response.json()
        print(f"   • Nombre: {campo.get('LogicalName')}")
        print(f"   • Tipo: {campo.get('AttributeType')}")
        
        # Si es Lookup/Picklist mostrar detalles
        if campo.get('AttributeType') == 'Lookup':
            targets = campo.get('Targets', [])
            print(f"   • Relación con: {', '.join(targets)}")
        elif campo.get('AttributeType') == 'Picklist':
            print(f"   • Es una lista de opciones (Picklist)")
        elif campo.get('AttributeType') in ['Integer', 'Decimal', 'Double']:
            print(f"   • Es un campo numérico (NO es relación)")
    else:
        print(f"   ❌ No se pudo obtener metadata: {response.status_code}")
    
    # 2. Ver valores actuales en los datos
    print("\n📈 2. DISTRIBUCIÓN DE VALORES ACTUALES:\n")
    data_url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$select=cr321_grupo&$top=500"
    
    response = requests.get(data_url, headers=headers)
    
    if response.status_code == 200:
        registros = response.json().get('value', [])
        valores = [r.get('cr321_grupo') for r in registros if r.get('cr321_grupo') is not None]
        
        contador = Counter(valores)
        print(f"   Total registros analizados: {len(registros)}")
        print(f"   Valores encontrados:")
        
        for valor, cantidad in sorted(contador.items()):
            porcentaje = (cantidad / len(valores) * 100) if valores else 0
            print(f"      • Valor {valor}: {cantidad} registros ({porcentaje:.1f}%)")
    else:
        print(f"   ❌ No se pudieron obtener datos: {response.status_code}")

def analizar_tabla_grup():
    """Analiza la tabla grup y sus tipos"""
    token = get_token()
    if not token:
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("\n" + "=" * 80)
    print("📊 ANÁLISIS: Tabla grup (cr321_grups)")
    print("=" * 80)
    
    # Ver grupos disponibles
    print("\n🔍 GRUPOS DISPONIBLES:\n")
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_grups?$select=cr321_grupoid,cr321_nombre,cr321_tipo,cr321_descripcion"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        grupos = response.json().get('value', [])
        print(f"   Total grupos: {len(grupos)}\n")
        
        for grupo in grupos:
            nombre = grupo.get('cr321_nombre', 'Sin nombre')
            tipo = grupo.get('cr321_tipo')
            desc = grupo.get('cr321_descripcion', 'Sin descripción')
            grupo_id = grupo.get('cr321_grupoid')
            
            # Convertir tipo numérico a letra
            tipo_letra = {913850000: 'A', 913850001: 'B', 913850002: 'C'}.get(tipo, tipo)
            
            print(f"   📁 {nombre}")
            print(f"      • Tipo: {tipo_letra} (valor: {tipo})")
            print(f"      • ID: {grupo_id}")
            print(f"      • Descripción: {desc}")
            print()
    else:
        print(f"   ❌ Error: {response.status_code}")

def proponer_solucion():
    """Propone cómo hacer la relación"""
    print("\n" + "=" * 80)
    print("💡 PROPUESTA DE SOLUCIÓN")
    print("=" * 80)
    print("""
SITUACIÓN ACTUAL:
-----------------
• chats00.cr321_grupo es un campo INTEGER con valores 1, 2, 3
  - 1 = Sin atender
  - 2 = En curso
  - 3 = Resueltas
  
• grup.cr321_tipo es un campo PICKLIST con valores A, B, C

OPCIONES PARA RELACIONAR:
-------------------------

OPCIÓN 1: Cambiar cr321_grupo a Lookup (RECOMENDADO)
   ✅ Ventajas:
      - Relación formal en Dataverse
      - Integridad referencial
      - Fácil de expandir en queries
   ⚠️  Requiere:
      - Crear campo nuevo tipo Lookup en Power Apps
      - Migrar datos existentes
      - Eliminar campo viejo

   Pasos:
   1. Power Apps → Tablas → cr321_adatawp0 → Columnas
   2. Nueva columna → Lookup → Relacionar con cr321_grup
   3. Nombre: cr321_grupoid (convención Dataverse)
   4. Migrar datos: 1→GrupoA, 2→GrupoB, 3→GrupoC
   5. Actualizar código backend
   6. Eliminar cr321_grupo viejo

OPCIÓN 2: Mantener Integer con mapeo en código
   ✅ Ventajas:
      - Sin cambios en Dataverse
      - Rápido de implementar
   ❌ Desventajas:
      - Sin integridad referencial
      - Lógica duplicada en código
   
   Implementación:
   # En backend
   GRUPO_MAPPING = {
       1: 'grupo_A_guid',  # Sin atender
       2: 'grupo_B_guid',  # En curso
       3: 'grupo_C_guid'   # Resueltas
   }

OPCIÓN 3: No relacionar, usar cr321_tipo directamente
   Si el propósito es solo filtrar/agrupar por tipo,
   podrías agregar un campo cr321_tipo en chats00 que
   copie el valor del grupo asociado.

¿Cuál prefieres implementar?
""")

if __name__ == "__main__":
    analizar_campo_grupo_chats()
    analizar_tabla_grup()
    proponer_solucion()
