"""
Script para crear contactos automáticamente desde mensajes de WhatsApp
----------------------------------------------------------------------
Cuando llega un mensaje de un número nuevo que no tiene contacto,
se crea automáticamente el contacto y se asocia.

Uso:
    1. Procesar mensajes existentes: python crear_contacto_auto_desde_mensaje.py
    2. Procesar un mensaje específico: python crear_contacto_auto_desde_mensaje.py --mensaje-id <GUID>
    3. Procesar por teléfono: python crear_contacto_auto_desde_mensaje.py --telefono <numero>
"""

import requests
import os
import sys
from dotenv import load_dotenv
from msal import ConfidentialClientApplication
from datetime import datetime

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


def get_headers(token=None):
    """Obtener headers con autenticación"""
    if token is None:
        token = get_access_token()
    return {
        'Authorization': f'Bearer {token}',
        'OData-MaxVersion': '4.0',
        'OData-Version': '4.0',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }


def verificar_contacto_existe(telefono, token=None):
    """Verificar si ya existe un contacto con ese teléfono"""
    headers = get_headers(token)
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_contactos"
    params = {
        "$filter": f"cr321_telefono eq '{telefono}'",
        "$select": "cr321_contactoid,cr321_fromnombre,cr321_telefono"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        contactos = response.json().get("value", [])
        if contactos:
            return contactos[0]  # Retorna el contacto existente
    
    return None  # No existe contacto


def crear_contacto_desde_mensaje(telefono, nombre, mensaje_id=None, token=None):
    """Crear un nuevo contacto desde los datos del mensaje"""
    headers = get_headers(token)
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_contactos"
    
    # Limpiar y formatear datos
    nombre_limpio = nombre.strip() if nombre else f"Contacto {telefono}"
    
    payload = {
        "cr321_fromnombre": nombre_limpio,
        "cr321_telefono": telefono,
        "cr321_descripcion": f"Contacto creado automáticamente desde WhatsApp",
        "cr321_fechacreacion": datetime.now().isoformat()
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 204:
        # Obtener el ID del contacto creado
        contacto_url = response.headers.get('OData-EntityId')
        if contacto_url:
            contacto_id = contacto_url.split('(')[1].split(')')[0]
            return contacto_id
        else:
            # Buscar el contacto recién creado
            contacto = verificar_contacto_existe(telefono, token)
            return contacto['cr321_contactoid'] if contacto else None
    else:
        print(f"   ❌ Error al crear contacto: {response.status_code}")
        print(f"   {response.text[:200]}")
        return None


def asociar_mensaje_con_contacto(mensaje_id, contacto_id):
    """Asociar un mensaje con un contacto"""
    headers = get_headers()
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s({mensaje_id})"
    
    payload = {
        "cr321_contactorelacion@odata.bind": f"/cr321_contactos({contacto_id})"
    }
    
    response = requests.patch(url, json=payload, headers=headers)
    return response.status_code == 204


def obtener_mensajes_sin_contacto():
    """Obtener mensajes que no tienen contacto asociado"""
    headers = get_headers()
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s"
    params = {
        "$filter": "_cr321_contactorelacion_value eq null",
        "$select": "cr321_adatawp0id,cr321_phone,cr321_fromname",
        "$orderby": "cr321_timestamp desc"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("value", [])
    else:
        print(f"❌ Error al obtener mensajes: {response.status_code}")
        return []


def procesar_mensaje(mensaje_id, telefono, nombre):
    """Procesar un mensaje: verificar contacto, crear si no existe, asociar"""
    print(f"\n📱 Procesando: {nombre} ({telefono})")
    
    # 1. Verificar si ya existe contacto
    contacto = verificar_contacto_existe(telefono)
    
    if contacto:
        print(f"   ✅ Contacto existente: {contacto['cr321_fromnombre']}")
        contacto_id = contacto['cr321_contactoid']
    else:
        # 2. Crear nuevo contacto
        print(f"   📝 Creando nuevo contacto...")
        contacto_id = crear_contacto_desde_mensaje(telefono, nombre, mensaje_id)
        
        if contacto_id:
            print(f"   ✅ Contacto creado: {contacto_id}")
        else:
            print(f"   ❌ No se pudo crear el contacto")
            return False
    
    # 3. Asociar mensaje con contacto
    if asociar_mensaje_con_contacto(mensaje_id, contacto_id):
        print(f"   🔗 Mensaje asociado con contacto")
        return True
    else:
        print(f"   ❌ No se pudo asociar el mensaje")
        return False


def procesar_todos_los_mensajes():
    """Procesar todos los mensajes sin contacto"""
    print("=" * 70)
    print("🔄 CREAR CONTACTOS AUTOMÁTICOS DESDE MENSAJES")
    print("=" * 70)
    
    mensajes = obtener_mensajes_sin_contacto()
    
    if not mensajes:
        print("\n✅ Todos los mensajes ya tienen contacto asociado")
        return
    
    print(f"\n📊 {len(mensajes)} mensajes sin contacto encontrados")
    print("-" * 70)
    
    # Agrupar por teléfono para crear un solo contacto por número
    mensajes_por_telefono = {}
    for msg in mensajes:
        telefono = msg.get("cr321_phone", "")
        if telefono:
            if telefono not in mensajes_por_telefono:
                mensajes_por_telefono[telefono] = []
            mensajes_por_telefono[telefono].append(msg)
    
    print(f"\n📱 {len(mensajes_por_telefono)} números únicos a procesar\n")
    
    exitos = 0
    errores = 0
    contactos_creados = 0
    contactos_existentes = 0
    
    for telefono, mensajes_tel in mensajes_por_telefono.items():
        # Usar el nombre del primer mensaje
        nombre = mensajes_tel[0].get("cr321_fromname", f"Contacto {telefono}")
        
        print(f"\n{'='*70}")
        print(f"📞 Teléfono: {telefono}")
        print(f"👤 Nombre: {nombre}")
        print(f"💬 {len(mensajes_tel)} mensaje(s) de este número")
        print(f"{'='*70}")
        
        # Verificar si ya existe contacto
        contacto = verificar_contacto_existe(telefono)
        
        if contacto:
            print(f"   ✅ Contacto existente: {contacto['cr321_fromnombre']}")
            contacto_id = contacto['cr321_contactoid']
            contactos_existentes += 1
        else:
            # Crear nuevo contacto
            print(f"   📝 Creando nuevo contacto...")
            contacto_id = crear_contacto_desde_mensaje(telefono, nombre)
            
            if contacto_id:
                print(f"   ✅ Contacto creado: {contacto_id}")
                contactos_creados += 1
            else:
                print(f"   ❌ Error al crear contacto")
                errores += len(mensajes_tel)
                continue
        
        # Asociar todos los mensajes de este número
        print(f"\n   🔗 Asociando {len(mensajes_tel)} mensaje(s)...")
        for i, msg in enumerate(mensajes_tel, 1):
            mensaje_id = msg['cr321_adatawp0id']
            if asociar_mensaje_con_contacto(mensaje_id, contacto_id):
                exitos += 1
                if i % 5 == 0:
                    print(f"      ✓ {i}/{len(mensajes_tel)} mensajes asociados...")
            else:
                errores += 1
                print(f"      ✗ Error en mensaje {i}")
        
        print(f"   ✅ Completado: {len(mensajes_tel)} mensajes asociados")
    
    # Resumen final
    print("\n" + "=" * 70)
    print("📊 RESUMEN FINAL")
    print("=" * 70)
    print(f"✅ Mensajes asociados:         {exitos}")
    print(f"❌ Errores:                    {errores}")
    print(f"📝 Contactos creados:          {contactos_creados}")
    print(f"♻️  Contactos ya existentes:    {contactos_existentes}")
    print(f"📱 Total números procesados:   {len(mensajes_por_telefono)}")
    print("=" * 70)
    print("\n✅ Proceso completado!")


def procesar_por_telefono(telefono):
    """Procesar todos los mensajes de un teléfono específico"""
    print(f"\n🔍 Buscando mensajes del teléfono: {telefono}")
    
    headers = get_headers()
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s"
    params = {
        "$filter": f"cr321_phone eq '{telefono}' and _cr321_contactorelacion_value eq null",
        "$select": "cr321_adatawp0id,cr321_phone,cr321_fromname"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        mensajes = response.json().get("value", [])
        if mensajes:
            nombre = mensajes[0].get("cr321_fromname", f"Contacto {telefono}")
            
            # Verificar/crear contacto
            contacto = verificar_contacto_existe(telefono)
            if not contacto:
                contacto_id = crear_contacto_desde_mensaje(telefono, nombre)
            else:
                contacto_id = contacto['cr321_contactoid']
            
            # Asociar mensajes
            for msg in mensajes:
                asociar_mensaje_con_contacto(msg['cr321_adatawp0id'], contacto_id)
            
            print(f"✅ {len(mensajes)} mensajes procesados")
        else:
            print("⚠️ No hay mensajes sin contacto para ese teléfono")
    else:
        print(f"❌ Error: {response.status_code}")


def procesar_desde_webhook(telefono, nombre, mensaje_id=None, token=None):
    """
    Función para usar desde webhook cuando llega un mensaje nuevo
    Retorna el ID del contacto (existente o creado)
    
    Args:
        telefono: Número de teléfono del contacto
        nombre: Nombre del contacto (puede ser None)
        mensaje_id: ID del mensaje (opcional)
        token: Token de autenticación (opcional, si no se provee usa MSAL)
    """
    try:
        # Verificar si existe contacto
        contacto = verificar_contacto_existe(telefono, token)
        
        if contacto:
            print(f"[CONTACTO] Contacto existente encontrado: {contacto['cr321_contactoid']}")
            return contacto['cr321_contactoid']
        
        # Crear nuevo contacto
        contacto_id = crear_contacto_desde_mensaje(telefono, nombre, mensaje_id, token)
        if contacto_id:
            print(f"[CONTACTO] Nuevo contacto creado: {contacto_id}")
        return contacto_id
    except Exception as e:
        print(f"[CONTACTO ERROR] {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            if sys.argv[1] == "--telefono" and len(sys.argv) > 2:
                procesar_por_telefono(sys.argv[2])
            elif sys.argv[1] == "--mensaje-id" and len(sys.argv) > 2:
                # Obtener datos del mensaje
                headers = get_headers()
                url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s({sys.argv[2]})"
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    msg = response.json()
                    procesar_mensaje(
                        msg['cr321_adatawp0id'],
                        msg['cr321_phone'],
                        msg['cr321_fromname']
                    )
            else:
                print("Uso:")
                print("  python crear_contacto_auto_desde_mensaje.py")
                print("  python crear_contacto_auto_desde_mensaje.py --telefono <numero>")
                print("  python crear_contacto_auto_desde_mensaje.py --mensaje-id <GUID>")
        else:
            # Procesar todos los mensajes sin contacto
            procesar_todos_los_mensajes()
            
    except Exception as e:
        print(f"\n❌ Error durante el proceso: {e}")
        import traceback
        traceback.print_exc()
