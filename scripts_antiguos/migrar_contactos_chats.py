"""
Migración: Asociar Mensajes de WhatsApp con Contactos
------------------------------------------------------
Script para asociar mensajes existentes en cr321_adatawp0 con contactos 
de cr321_contacto basándose en el campo teléfono.

Requisitos:
- Campo cr321_contactoId (Lookup) debe existir en cr321_adatawp0
- Tablas cr321_contacto y cr321_adatawp0 deben estar publicadas

Uso:
    python migrar_contactos_chats.py
"""

import requests
import os
from dotenv import load_dotenv
from datetime import datetime
from msal import ConfidentialClientApplication

# Cargar configuración desde backend/.env
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend', '.env')
load_dotenv(env_path)

DATAVERSE_URL = os.getenv("DATAVERSE_URL")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")


def get_access_token():
    """Obtener token de acceso para Dataverse usando MSAL"""
    try:
        authority = f"https://login.microsoftonline.com/{TENANT_ID}"
        app = ConfidentialClientApplication(
            CLIENT_ID,
            authority=authority,
            client_credential=CLIENT_SECRET
        )
        result = app.acquire_token_for_client(scopes=[f"{DATAVERSE_URL}/.default"])
        
        if "access_token" in result:
            return result["access_token"]
        else:
            raise Exception(f"Error al obtener token: {result.get('error_description', 'Unknown')}")
    except Exception as e:
        raise Exception(f"Excepción al obtener token: {e}")


def get_headers():
    """Obtener headers con autenticación"""
    token = get_access_token()
    return {
        'Authorization': f'Bearer {token}',
        'OData-MaxVersion': '4.0',
        'OData-Version': '4.0',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }


def verificar_campo_existe():
    """Verificar que el campo cr321_contactorelacion existe en cr321_adatawp0"""
    print("\n🔍 Verificando campo cr321_contactorelacion...")
    
    headers = get_headers()
    url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions(LogicalName='cr321_adatawp0')/Attributes"
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            atributos = response.json().get("value", [])
            campo_existe = any(a.get("LogicalName") == "cr321_contactorelacion" for a in atributos)
            
            if campo_existe:
                print("✅ Campo cr321_contactorelacion existe")
                return True
            else:
                print("❌ Campo cr321_contactorelacion NO existe")
                print("\n📝 Debes crear el campo primero:")
                print("   1. Ir a https://make.powerapps.com")
                print("   2. Abrir tabla cr321_adatawp0")
                print("   3. Agregar columna tipo 'Búsqueda' → cr321_contacto")
                return False
        else:
            print(f"❌ Error al verificar campo: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def obtener_contactos():
    """Obtener todos los contactos con su teléfono"""
    print("\n📋 Obteniendo contactos...")
    
    headers = get_headers()
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_contactos"
    params = {
        "$select": "cr321_contactoid,cr321_telefono,cr321_fromnombre"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        contactos = response.json().get("value", [])
        print(f"✅ {len(contactos)} contactos encontrados")
        
        # Crear diccionario teléfono -> contacto
        telefono_a_contacto = {}
        for c in contactos:
            telefono = c.get("cr321_telefono")
            if telefono:
                telefono_a_contacto[telefono] = {
                    "id": c["cr321_contactoid"],
                    "nombre": c.get("cr321_fromnombre", "Sin nombre")
                }
        
        return telefono_a_contacto
    else:
        print(f"❌ Error al obtener contactos: {response.status_code}")
        print(response.text)
        return {}


def obtener_mensajes_sin_contacto():
    """Obtener mensajes que no tienen contacto asociado"""
    print("\n📨 Obteniendo mensajes sin contacto...")
    
    headers = get_headers()
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s"
    params = {
        "$filter": "_cr321_contactorelacion_value eq null",
        "$select": "cr321_adatawp0id,cr321_phone,cr321_fromname,cr321_timestamp",
        "$orderby": "cr321_timestamp desc"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        mensajes = response.json().get("value", [])
        print(f"📊 {len(mensajes)} mensajes sin contacto asociado")
        return mensajes
    else:
        print(f"❌ Error al obtener mensajes: {response.status_code}")
        print(response.text)
        return []


def asociar_mensaje_con_contacto(mensaje_id, contacto_id):
    """Asociar un mensaje con un contacto"""
    headers = get_headers()
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s({mensaje_id})"
    
    payload = {
        "cr321_contactorelacion@odata.bind": f"/cr321_contactos({contacto_id})"
    }
    
    response = requests.patch(url, json=payload, headers=headers)
    
    return response.status_code == 204


def migrar_mensajes():
    """Proceso principal de migración"""
    print("=" * 60)
    print("🔄 MIGRACIÓN: Asociar Mensajes con Contactos")
    print("=" * 60)
    
    # 1. Verificar que el campo existe
    if not verificar_campo_existe():
        return
    
    # 2. Obtener contactos
    telefono_a_contacto = obtener_contactos()
    
    if not telefono_a_contacto:
        print("\n⚠️ No hay contactos para asociar")
        return
    
    # 3. Obtener mensajes sin contacto
    mensajes = obtener_mensajes_sin_contacto()
    
    if not mensajes:
        print("\n✅ Todos los mensajes ya tienen contacto asociado")
        return
    
    # 4. Asociar mensajes con contactos
    print(f"\n🔄 Asociando mensajes con contactos...")
    print("-" * 60)
    
    actualizados = 0
    sin_contacto = 0
    errores = 0
    telefonos_sin_contacto = set()
    
    for i, mensaje in enumerate(mensajes, 1):
        telefono = mensaje.get("cr321_phone", "")
        mensaje_id = mensaje["cr321_adatawp0id"]
        
        # Mostrar progreso cada 10 mensajes
        if i % 10 == 0:
            print(f"   Procesando: {i}/{len(mensajes)} mensajes...")
        
        if telefono in telefono_a_contacto:
            contacto_info = telefono_a_contacto[telefono]
            
            # Asociar mensaje con contacto
            if asociar_mensaje_con_contacto(mensaje_id, contacto_info["id"]):
                actualizados += 1
            else:
                errores += 1
                print(f"   ❌ Error al actualizar mensaje ID: {mensaje_id}")
        else:
            sin_contacto += 1
            telefonos_sin_contacto.add(telefono)
    
    # 5. Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE MIGRACIÓN")
    print("=" * 60)
    print(f"✅ Mensajes actualizados:     {actualizados}")
    print(f"⚠️  Mensajes sin contacto:    {sin_contacto}")
    print(f"❌ Errores:                   {errores}")
    print(f"📱 Teléfonos únicos sin contacto: {len(telefonos_sin_contacto)}")
    
    if telefonos_sin_contacto:
        print(f"\n💡 Teléfonos sin contacto (primeros 10):")
        for telefono in list(telefonos_sin_contacto)[:10]:
            print(f"   - {telefono}")
        
        if len(telefonos_sin_contacto) > 10:
            print(f"   ... y {len(telefonos_sin_contacto) - 10} más")
        
        print("\n📝 Sugerencia: Crear contactos para estos teléfonos")
        print("   Puedes usar el script crear_contactos_faltantes.py")
    
    print("\n✅ Migración completada!")
    print("=" * 60)


def estadisticas_relacion():
    """Mostrar estadísticas de la relación mensajes-contactos"""
    print("\n" + "=" * 60)
    print("📊 ESTADÍSTICAS: Mensajes y Contactos")
    print("=" * 60)
    
    headers = get_headers()
    
    # Total de mensajes
    url_total = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$count=true&$top=0"
    response_total = requests.get(url_total, headers=headers)
    total_mensajes = response_total.json().get("@odata.count", 0) if response_total.status_code == 200 else 0
    
    # Mensajes con contacto
    url_con = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$filter=_cr321_contactorelacion_value ne null&$count=true&$top=0"
    response_con = requests.get(url_con, headers=headers)
    con_contacto = response_con.json().get("@odata.count", 0) if response_con.status_code == 200 else 0
    
    # Mensajes sin contacto
    sin_contacto = total_mensajes - con_contacto
    
    # Calcular porcentajes
    porcentaje_con = (con_contacto / total_mensajes * 100) if total_mensajes > 0 else 0
    porcentaje_sin = (sin_contacto / total_mensajes * 100) if total_mensajes > 0 else 0
    
    print(f"\n📨 Total de mensajes:        {total_mensajes}")
    print(f"✅ Con contacto asociado:    {con_contacto} ({porcentaje_con:.1f}%)")
    print(f"⚠️  Sin contacto asociado:   {sin_contacto} ({porcentaje_sin:.1f}%)")
    print("=" * 60)


if __name__ == "__main__":
    try:
        # Ejecutar migración
        migrar_mensajes()
        
        # Mostrar estadísticas
        estadisticas_relacion()
        
    except Exception as e:
        print(f"\n❌ Error durante la migración: {e}")
        import traceback
        traceback.print_exc()
