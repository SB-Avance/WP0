"""
Script para verificar el estado actual de grupos en conversaciones y usuarios
"""
import os
import requests
from msal import ConfidentialClientApplication

# Configuración de Dataverse desde backend/.env
CLIENT_ID = "d05fd904-f1fb-4fe3-89e9-1779d914c828"
CLIENT_SECRET = "QYG8Q~J38KfJGUSIy-O2h-o_9pRTNuTNC7909aWg"
TENANT_ID = "41ddee82-dfb3-4c4a-bbe6-de9c741c754e"
DATAVERSE_URL = "https://org460b8a6c.crm2.dynamics.com"

def get_token():
    """Obtener token de autenticación"""
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
        raise Exception(f"Error obteniendo token: {result.get('error_description')}")

print("=" * 60)
print("VERIFICACIÓN ESTADO DE GRUPOS")
print("=" * 60)

# 1. Obtener token
print("\n1. Obteniendo token...", end=" ")
token = get_token()
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}
print("✅")

# 2. Verificar campo cr321_grupo en mensajes
print("\n2. Verificando campo cr321_grupo en mensajes...")
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$select=cr321_phone,cr321_grupo&$top=10"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    mensajes = response.json().get("value", [])
    print(f"   ✅ Campo accesible - {len(mensajes)} mensajes consultados")
    
    # Contar valores de grupo
    grupos_count = {}
    for msg in mensajes:
        grupo = msg.get("cr321_grupo")
        grupos_count[grupo] = grupos_count.get(grupo, 0) + 1
    
    print("\n   Distribución de valores:")
    # Separar None de los valores numéricos para ordenar
    items_ordenados = [(k, v) for k, v in grupos_count.items() if k is not None]
    items_ordenados.sort(key=lambda x: x[0])
    if None in grupos_count:
        items_ordenados.insert(0, (None, grupos_count[None]))
    
    for grupo, count in items_ordenados:
        if grupo is None:
            print(f"      NULL/sin asignar: {count}")
        else:
            print(f"      Grupo {grupo}: {count}")
else:
    print(f"   ❌ Error: {response.status_code}")
    print(f"   {response.text[:200]}")

# 3. Verificar usuario 0006 y sus grupos
print("\n3. Verificando usuario 0006 (Contabilidad)...")
usuario_id = "e45580f3-59fa-f011-8406-002248df122f"

url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuariogrupos?$filter=_cr321_usuarioid_value eq {usuario_id}"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    relaciones = response.json().get("value", [])
    print(f"   ✅ Usuario tiene {len(relaciones)} relación(es)")
    for rel in relaciones:
        codigo = rel.get("cr321_usuariogrupo1")
        print(f"      Código: {codigo}")
else:
    print(f"   ❌ Error: {response.status_code}")

# 4. Verificar mapeo backend
print("\n4. Mapeo backend esperado:")
print("   INT_TO_GROUP:")
INT_TO_GROUP = {1: "Soporte", 2: "Ventas", 3: "Administracion", 4: "Contabilidad", None: "GENERAL"}
for num, nombre in INT_TO_GROUP.items():
    print(f"      {num} → {nombre}")

print("\n   CODIGO_A_NOMBRE (API usuario-grupos):")
CODIGO_A_NOMBRE = {"0001": "Soporte", "0002": "Ventas", "0003": "Administracion", "0004": "Contabilidad"}
for codigo, nombre in CODIGO_A_NOMBRE.items():
    print(f"      {codigo} → {nombre}")

# 5. Verificar conversaciones con grupo 4
print("\n5. Verificando conversaciones del grupo 4 (Contabilidad)...")
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$filter=cr321_grupo eq 4&$select=cr321_phone&$orderby=cr321_phone"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    mensajes = response.json().get("value", [])
    telefonos = set(msg.get("cr321_phone") for msg in mensajes)
    print(f"   ✅ {len(mensajes)} mensajes con grupo 4")
    print(f"   💼 {len(telefonos)} conversaciones únicas:")
    for tel in sorted(telefonos):
        print(f"      {tel}")
else:
    print(f"   ❌ Error: {response.status_code}")

# 6. Probar endpoint API
print("\n6. Probando API backend local...")
try:
    response = requests.get("http://localhost:5000/api/conversations", timeout=5)
    if response.status_code == 200:
        conversations = response.json()
        print(f"   ✅ API responde - {len(conversations)} conversaciones")
        
        # Contar por grupo
        grupos = {}
        for conv in conversations:
            grupo = conv.get("group", "GENERAL")
            grupos[grupo] = grupos.get(grupo, 0) + 1
        
        print("\n   Distribución por grupo en API:")
        for grupo, count in sorted(grupos.items()):
            print(f"      {grupo}: {count}")
    else:
        print(f"   ❌ Error: {response.status_code}")
except Exception as e:
    print(f"   ⚠️ Backend no disponible: {e}")

print("\n" + "=" * 60)
print("DIAGNÓSTICO COMPLETADO")
print("=" * 60)
