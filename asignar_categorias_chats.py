"""
Script: Asignar Categorías a Chats Existentes
==============================================
Migra los chats existentes asignándoles una categoría del chatbot
basándose en análisis del contenido o reglas por defecto

Fecha: 7 de febrero de 2026
"""
import requests
import os
import re
from datetime import datetime
from dotenv import load_dotenv

# Cargar .env desde el directorio backend
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend', '.env')
load_dotenv(env_path)

DATAVERSE_URL = os.getenv("DATAVERSE_URL")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")

# IDs de grupos obtenidos del análisis previo
CATEGORIAS = {
    'ticket': '0001',  # Solicitud Ticket - Tipo: 462410000
    'cotizacion': '0002',  # Cotización - Tipo: 462410001
    'informacion': '0003',  # Información - Tipo: 462410002
    'agente': '0004'  # Solicitar atención de agente - Tipo: 462410003
}

# Palabras clave para clasificación automática
KEYWORDS = {
    'ticket': ['problema', 'error', 'no funciona', 'ayuda', 'soporte', 'ticket', 'issue'],
    'cotizacion': ['precio', 'costo', 'cotizar', 'cotización', 'cuanto', 'cuánto', 'valor', '$$', 'comprar'],
    'agente': ['agente', 'humano', 'persona', 'hablar con', 'transferir', 'operador'],
    'informacion': ['info', 'información', 'horario', 'dirección', 'ubicacion', 'contacto', 'qué es', 'quien']
}

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
    return None

def clasificar_mensaje(body):
    """Clasifica un mensaje basándose en palabras clave"""
    if not body:
        return None
    
    body_lower = body.lower()
    scores = {cat: 0 for cat in KEYWORDS.keys()}
    
    # Contar coincidencias de palabras clave
    for categoria, keywords in KEYWORDS.items():
        for keyword in keywords:
            if keyword in body_lower:
                scores[categoria] += 1
    
    # Retornar la categoría con mayor puntaje
    max_score = max(scores.values())
    if max_score == 0:
        return None  # No se pudo clasificar
    
    return max(scores, key=scores.get)

def obtener_chats_sin_categoria():
    """Obtiene todos los chats que no tienen categoría asignada"""
    token = get_token()
    if not token:
        return []
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Nota: Ajusta el filtro según cómo se llame el campo después de crearlo
    # Si el campo no existe aún, esto retornará todos los registros
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s"
    url += "?$select=cr321_adatawp0id,cr321_body,cr321_phone,cr321_grupo"
    url += "&$orderby=cr321_timestamp desc"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json().get('value', [])
    else:
        print(f"❌ Error obteniendo chats: {response.status_code}")
        return []

def asignar_categoria(chat_id, categoria_key):
    """Asigna una categoría a un chat específico"""
    token = get_token()
    if not token:
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # IMPORTANTE: Este campo debe existir en Dataverse primero
    # Ajusta el nombre del campo según lo hayas creado en Power Apps
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s({chat_id})"
    
    # Obtener el GUID del grupo desde la tabla cr321_grups
    grupos_url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_grups"
    grupos_url += f"?$filter=cr321_grupoid eq '{CATEGORIAS[categoria_key]}'"
    
    grupos_response = requests.get(grupos_url, headers=headers)
    
    if grupos_response.status_code != 200:
        print(f"❌ No se encontró el grupo: {categoria_key}")
        return False
    
    grupos = grupos_response.json().get('value', [])
    if not grupos:
        return False
    
    grupo_guid = grupos[0]['cr321_grupoid']
    
    # Actualizar el chat con la relación
    # NOTA: Reemplaza 'cr321_categoria_chatbot' con el nombre real del campo Lookup
    data = {
        "cr321_categoria_chatbot@odata.bind": f"/cr321_grups({grupo_guid})"
    }
    
    response = requests.patch(url, headers=headers, json=data)
    
    return response.status_code == 204

def mostrar_estadisticas_clasificacion(chats):
    """Muestra estadísticas de clasificación"""
    clasificados = {}
    sin_clasificar = 0
    
    for chat in chats:
        body = chat.get('cr321_body', '')
        categoria = clasificar_mensaje(body)
        
        if categoria:
            clasificados[categoria] = clasificados.get(categoria, 0) + 1
        else:
            sin_clasificar += 1
    
    print("📊 Estadísticas de Clasificación Automática:\n")
    print(f"   Total de chats: {len(chats)}")
    print(f"\n   Clasificados por categoría:")
    for cat, count in sorted(clasificados.items()):
        porcentaje = (count / len(chats) * 100) if chats else 0
        print(f"      • {cat.capitalize()}: {count} ({porcentaje:.1f}%)")
    
    porcentaje_sin = (sin_clasificar / len(chats) * 100) if chats else 0
    print(f"\n   Sin clasificar: {sin_clasificar} ({porcentaje_sin:.1f}%)")

def migrar_con_confirmacion():
    """Proceso principal con confirmación del usuario"""
    print("=" * 80)
    print("🔄 MIGRACIÓN: Asignar Categorías a Chats")
    print("=" * 80)
    
    # Verificar que el campo existe
    print("\n⚠️  IMPORTANTE:")
    print("   Este script requiere que el campo 'cr321_categoria_chatbot' (Lookup)")
    print("   ya exista en la tabla cr321_adatawp0 en Power Apps.")
    print("\n   Si no lo has creado aún, sigue los pasos en:")
    print("   docs/NUEVA_ESTRUCTURA_CHATS_CATEGORIA.md\n")
    
    respuesta = input("¿Has creado el campo en Power Apps? (s/n): ")
    if respuesta.lower() != 's':
        print("\n❌ Cancela la migración. Crea el campo primero.")
        return
    
    print("\n🔍 Obteniendo chats existentes...\n")
    chats = obtener_chats_sin_categoria()
    
    if not chats:
        print("❌ No se encontraron chats o error al consultar")
        return
    
    print(f"✅ {len(chats)} chats encontrados\n")
    
    # Mostrar estadísticas
    mostrar_estadisticas_clasificacion(chats)
    
    print("\n" + "=" * 80)
    print("ESTRATEGIAS DE MIGRACIÓN")
    print("=" * 80)
    print("\n1. AUTOMÁTICA: Clasificar basándose en palabras clave del mensaje")
    print("2. POR DEFECTO: Asignar 'Información' a todos los chats sin clasificar")
    print("3. MANUAL: Revisar uno por uno (para pocos registros)")
    print("4. CANCELAR: No hacer cambios ahora")
    
    opcion = input("\nElige una opción (1-4): ")
    
    if opcion == '1':
        migrar_automatica(chats)
    elif opcion == '2':
        migrar_por_defecto(chats, 'informacion')
    elif opcion == '3':
        print("\n⚠️  Migración manual no implementada aún")
        print("   Puedes hacerlo desde Power Apps o ajustar este script")
    else:
        print("\n❌ Migración cancelada")

def migrar_automatica(chats):
    """Migra automáticamente usando clasificación por keywords"""
    print("\n" + "=" * 80)
    print("🤖 MIGRACIÓN AUTOMÁTICA")
    print("=" * 80)
    
    exitos = 0
    fallos = 0
    sin_clasificar = 0
    
    for i, chat in enumerate(chats, 1):
        chat_id = chat['cr321_adatawp0id']
        body = chat.get('cr321_body', '')
        phone = chat.get('cr321_phone', 'N/A')
        
        categoria = clasificar_mensaje(body)
        
        if not categoria:
            sin_clasificar += 1
            continue
        
        print(f"\n[{i}/{len(chats)}] {phone[:15]:<15} → {categoria.upper()}")
        
        if asignar_categoria(chat_id, categoria):
            exitos += 1
            print(f"   ✅ Asignado")
        else:
            fallos += 1
            print(f"   ❌ Error")
    
    print("\n" + "=" * 80)
    print("📊 RESULTADO")
    print("=" * 80)
    print(f"   ✅ Exitosos: {exitos}")
    print(f"   ❌ Fallidos: {fallos}")
    print(f"   ⚠️  Sin clasificar: {sin_clasificar}")

def migrar_por_defecto(chats, categoria_defecto):
    """Asigna una categoría por defecto a todos los chats"""
    print(f"\n🔄 Asignando '{categoria_defecto}' a {len(chats)} chats...")
    
    exitos = 0
    fallos = 0
    
    for chat in chats:
        chat_id = chat['cr321_adatawp0id']
        
        if asignar_categoria(chat_id, categoria_defecto):
            exitos += 1
        else:
            fallos += 1
        
        if (exitos + fallos) % 10 == 0:
            print(f"   Progreso: {exitos + fallos}/{len(chats)}")
    
    print(f"\n✅ Completado: {exitos} exitosos, {fallos} fallidos")

if __name__ == "__main__":
    migrar_con_confirmacion()
