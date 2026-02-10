"""
Script para agregar campos elemento1 a elemento5 a la tabla cr321_chatbot
Estos campos almacenarán opciones de menú dinámico para el frontend
"""

import os
import requests
from dotenv import load_dotenv
import msal

# Cargar variables de entorno desde backend/.env
env_path = os.path.join(os.path.dirname(__file__), 'backend', '.env')
load_dotenv(env_path)

# Configuración
TENANT_ID = os.getenv('TENANT_ID')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
DATAVERSE_URL = os.getenv('DATAVERSE_URL')
SCOPE = [f"{DATAVERSE_URL}/.default"]

def get_access_token():
    """Obtiene token de acceso usando MSAL"""
    authority = f"https://login.microsoftonline.com/{TENANT_ID}"
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=authority,
        client_credential=CLIENT_SECRET
    )
    
    result = app.acquire_token_for_client(scopes=SCOPE)
    
    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception(f"Error obteniendo token: {result.get('error_description')}")


def create_campo_elemento(token, numero):
    """
    Crea un campo cr321_elementoX en la tabla cr321_chatbot
    
    Args:
        token: Access token de Azure AD
        numero: Número del elemento (1-5)
    """
    campo_nombre = f"cr321_elemento{numero}"
    
    # Definición del campo
    campo = {
        "AttributeType": "String",
        "AttributeTypeName": {"Value": "StringType"},
        "MaxLength": 100,
        "SchemaName": campo_nombre,
        "DisplayName": {
            "@odata.type": "Microsoft.Dynamics.CRM.Label",
            "LocalizedLabels": [
                {
                    "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                    "Label": f"Elemento Menú {numero}",
                    "LanguageCode": 1034  # Español
                }
            ]
        },
        "Description": {
            "@odata.type": "Microsoft.Dynamics.CRM.Label",
            "LocalizedLabels": [
                {
                    "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                    "Label": f"Opción {numero} del menú dinámico del chatbot",
                    "LanguageCode": 1034
                }
            ]
        },
        "RequiredLevel": {
            "Value": "None",
            "CanBeChanged": True
        },
        "IsValidForAdvancedFind": {
            "Value": True
        },
        "@odata.type": "Microsoft.Dynamics.CRM.StringAttributeMetadata"
    }
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions(LogicalName='cr321_chatbot')/Attributes"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    try:
        response = requests.post(url, json=campo, headers=headers, timeout=30)
        
        if response.status_code in [200, 201, 204]:
            print(f"[OK] Campo {campo_nombre} creado exitosamente")
            return True
        else:
            print(f"[ERROR] No se pudo crear el campo {campo_nombre}: {response.status_code}")
            print(f"  Detalle: {response.text}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Excepción al crear campo {campo_nombre}: {e}")
        return False


def main():
    """Función principal"""
    print("=" * 60)
    print("AGREGAR CAMPOS ELEMENTO1-5 A TABLA cr321_chatbot")
    print("=" * 60)
    print()
    
    # Obtener token
    print("[1/6] Obteniendo token de acceso...")
    try:
        token = get_access_token()
        print("[OK] Token obtenido exitosamente")
        print()
    except Exception as e:
        print(f"[ERROR] No se pudo obtener el token: {e}")
        return
    
    # Crear los 5 campos
    exitos = 0
    for i in range(1, 6):
        print(f"[{i+1}/6] Creando campo cr321_elemento{i}...")
        if create_campo_elemento(token, i):
            exitos += 1
        print()
    
    # Resumen
    print("=" * 60)
    print("RESUMEN")
    print("=" * 60)
    print(f"Campos creados exitosamente: {exitos}/5")
    
    if exitos == 5:
        print("[OK] Todos los campos fueron creados correctamente")
        print()
        print("PROXIMOS PASOS:")
        print("1. Ir a Power Apps (make.powerapps.com)")
        print("2. Abrir la tabla 'chatbot' (cr321_chatbot)")
        print("3. Editar los chatbots activos y llenar elemento1-5 con opciones de menu")
        print("   Ejemplo: 'Solicitud Ticket', 'Cotizacion', 'Informacion', etc.")
        print("4. Ejecutar el backend y frontend para ver el menu dinamico")
    else:
        print(f"[AVISO] Solo se crearon {exitos} de 5 campos")
        print("Revisa los errores anteriores")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
