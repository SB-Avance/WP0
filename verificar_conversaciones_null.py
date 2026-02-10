"""
Verificar conversaciones con grupo NULL
"""
import requests
from msal import ConfidentialClientApplication

CLIENT_ID = "d05fd904-f1fb-4fe3-89e9-1779d914c828"
CLIENT_SECRET = "QYG8Q~J38KfJGUSIy-O2h-o_9pRTNuTNC7909aWg"
TENANT_ID = "41ddee82-dfb3-4c4a-bbe6-de9c741c754e"
DATAVERSE_URL = "https://org460b8a6c.crm2.dynamics.com"

def get_token():
    authority = f"https://login.microsoftonline.com/{TENANT_ID}"
    scope = [f"{DATAVERSE_URL}/.default"]
    app = ConfidentialClientApplication(CLIENT_ID, authority=authority, client_credential=CLIENT_SECRET)
    result = app.acquire_token_for_client(scopes=scope)
    return result["access_token"]

print("=" * 70)
print("CONVERSACIONES CON GRUPO NULL")
print("=" * 70)

token = get_token()
headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

# Obtener mensajes con grupo NULL
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$filter=cr321_grupo eq null&$select=cr321_phone,cr321_messageid,cr321_timestamp,cr321_body&$orderby=cr321_phone,cr321_timestamp desc"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    mensajes = response.json().get("value", [])
    print(f"\n✅ {len(mensajes)} mensajes con grupo NULL\n")
    
    # Agrupar por teléfono
    conversaciones = {}
    for msg in mensajes:
        phone = msg.get("cr321_phone")
        if phone not in conversaciones:
            conversaciones[phone] = []
        conversaciones[phone].append(msg)
    
    print(f"📞 {len(conversaciones)} conversaciones únicas con grupo NULL:\n")
    
    for i, (phone, mensajes_conv) in enumerate(sorted(conversaciones.items()), 1):
        ultimo_msg = mensajes_conv[0]
        body = (ultimo_msg.get("cr321_body") or "")[:40]
        timestamp = ultimo_msg.get("cr321_timestamp", "")[:19]
        
        print(f"{i}. {phone}")
        print(f"   📧 {len(mensajes_conv)} mensajes")
        print(f"   💬 Último: {body}")
        print(f"   🕐 {timestamp}")
        print()
    
    print("=" * 70)
    print("ACCIONES RECOMENDADAS:")
    print("=" * 70)
    print("\nOpción 1: Asignar estas conversaciones a grupos reales")
    print("  - Ejemplo: Asignar a Soporte (grupo 1)")
    print("  - UPDATE cr321_adatawp0s SET cr321_grupo = 1 WHERE cr321_grupo IS NULL")
    print("\nOpción 2: Eliminar 'GENERAL' del backend")
    print("  - Modificar back.py para no devolver conversaciones sin grupo")
    print("  - Solo usuarios con permisos especiales verían conversaciones NULL")
    print("\nOpción 3: Crear grupo 'General' en Dataverse")
    print("  - Agregar registro en cr321_grup con código 0005")
    print("  - Actualizar INT_TO_GROUP: {5: 'General', ...}")
    print("  - UPDATE cr321_adatawp0s SET cr321_grupo = 5 WHERE cr321_grupo IS NULL")
    
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text[:300])

print("\n" + "=" * 70)
