import os
from dotenv import load_dotenv
load_dotenv()   # Cargar .env

# Variables de entorno
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
AZURE_REGION = os.getenv("AZURE_REGION")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
ENTITY_SET = os.getenv("ENTITY_SET")
DATAVERSE_URL = os.getenv("DATAVERSE_URL")
PHONE_NUMBER_ID  = os.getenv("PHONE_NUMBER_ID")
PHONE_NUMBER_ID0 = os.getenv("PHONE_NUMBER_ID0")
PHONE_NUMBER_ID1 = os.getenv("PHONE_NUMBER_ID1")
PHONE_NUMBER_ID2 = os.getenv("PHONE_NUMBER_ID2")
TENANT_ID = os.getenv("TENANT_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
Z_URL_ENTORNO = os.getenv("Z_URL_ENTORNO")
Z_ZPRUEBA = os.getenv("Z_PRUEBA")

#azure_region="eastus"

def clear_screen():
    # Para Windows usa 'cls', para Linux/Mac usa 'clear'
    os.system('cls' if os.name == 'nt' else 'clear')
# Ejemplo de uso:
#clear_screen()

def mostrar_variables():
    return f"""
    
ACCESS_TOKEN:       {ACCESS_TOKEN[:10]}... (oculto)
AZURE_REGION:       {AZURE_REGION}	
CLIENT_ID:          {CLIENT_ID}
CLIENT_SECRET:      {CLIENT_SECRET[:6]}... (oculto)
ENTITY_SET:         {ENTITY_SET}
DATAVERSE_URL:      {DATAVERSE_URL}
PHONE_NUMBER_ID:    {PHONE_NUMBER_ID}
PHONE_NUMBER_ID0:   {PHONE_NUMBER_ID0}
PHONE_NUMBER_ID1:   {PHONE_NUMBER_ID1}
PHONE_NUMBER_ID2:   {PHONE_NUMBER_ID2}
TENANT_ID:          {TENANT_ID}
VERIFY_TOKEN:       {VERIFY_TOKEN}
Z_URL_ENTORNO:      {Z_URL_ENTORNO}
Z_ZPRUEBA:          {Z_ZPRUEBA}
       """
