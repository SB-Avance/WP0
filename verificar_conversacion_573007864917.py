"""
Script para verificar conversación 573007864917 específicamente
"""
import os
import requests
from msal import ConfidentialClientApplication

# Configuración
CLIENT_ID = "d05fd904-f1fb-4fe3-89e9-1779d914c828"
CLIENT_SECRET = "QYG8Q~J38KfJGUSIy-O2h-o_9pRTNuTNC7909aWg"
TENANT_ID = "41ddee82-dfb3-4c4a-bbe6-de9c741c754e"
DATAVERSE_URL = "https://org460b8a6c.crm2.dynamics.com"

def get_token():
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
        raise Exception(f"Error: {result.get('error_description')}")

print("=" * 70)
print("VERIFICACIÓN CONVERSACIÓN 573007864917")
print("=" * 70)

token = get_token()
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}

# Buscar todos los mensajes de esta conversación
phone = "573007864917"
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$filter=cr321_phone eq '{phone}'&$select=cr321_messageid,cr321_body,cr321_grupo,cr321_timestamp&$orderby=cr321_timestamp desc"

print(f"\nBuscando mensajes de {phone}...")
response = requests.get(url, headers=headers)

if response.status_code == 200:
    mensajes = response.json().get("value", [])
    print(f"✅ {len(mensajes)} mensajes encontrados\n")
    
    print(f"{'MessageID':<40} {'Grupo':<10} {'Body':<30} {'Timestamp'}")
    print("-" * 110)
    
    for msg in mensajes:
        msg_id = msg.get("cr321_messageid", "N/A")[:38]
        grupo = msg.get("cr321_grupo")
        body = (msg.get("cr321_body") or "")[:28]
        timestamp = msg.get("cr321_timestamp", "N/A")[:19]
        
        grupo_str = str(grupo) if grupo is not None else "NULL"
        print(f"{msg_id:<40} {grupo_str:<10} {body:<30} {timestamp}")
    
    # Estadísticas
    grupos_count = {}
    for msg in mensajes:
        grupo = msg.get("cr321_grupo")
        grupos_count[grupo] = grupos_count.get(grupo, 0) + 1
    
    print("\n" + "=" * 70)
    print("RESUMEN:")
    for grupo, count in sorted(grupos_count.items(), key=lambda x: (x[0] is None, x[0])):
        if grupo is None:
            print(f"  NULL/sin asignar: {count} mensajes")
        else:
            print(f"  Grupo {grupo}: {count} mensajes")
    
    # Verificar qué devuelve el backend
    print("\n" + "=" * 70)
    print("COMPARACIÓN CON API BACKEND:")
    try:
        backend_response = requests.get("http://localhost:5000/api/conversations", timeout=5)
        if backend_response.status_code == 200:
            data = backend_response.json()
            conversations = data.get("conversations", [])
            
            conv_encontrada = None
            for conv in conversations:
                if conv.get("phone") == phone:
                    conv_encontrada = conv
                    break
            
            if conv_encontrada:
                print(f"\n✅ Conversación encontrada en backend:")
                print(f"   Teléfono: {conv_encontrada.get('phone')}")
                print(f"   Grupo: {conv_encontrada.get('group')}")
                print(f"   Nombre: {conv_encontrada.get('name')}")
                print(f"   Último mensaje: {conv_encontrada.get('last_message')}")
            else:
                print(f"\n❌ Conversación NO encontrada en backend")
                print(f"   Total conversaciones en backend: {len(conversations)}")
        else:
            print(f"❌ Error en backend: {backend_response.status_code}")
    except Exception as e:
        print(f"⚠️ Error consultando backend: {e}")
else:
    print(f"❌ Error {response.status_code}: {response.text[:200]}")

print("\n" + "=" * 70)
