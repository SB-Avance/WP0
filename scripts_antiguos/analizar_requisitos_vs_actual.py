"""
Script para comparar REQUISITOS ORIGINALES vs ESTADO ACTUAL del sistema
Genera reporte de tablas, campos y relaciones faltantes
"""
import os
from dotenv import load_dotenv
from msal import ConfidentialClientApplication
import requests
import json

env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend', '.env')
load_dotenv(env_path)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
DATAVERSE_URL = os.getenv("DATAVERSE_URL")

def get_token():
    authority = f"https://login.microsoftonline.com/{TENANT_ID}"
    app = ConfidentialClientApplication(CLIENT_ID, authority=authority, client_credential=CLIENT_SECRET)
    result = app.acquire_token_for_client(scopes=[f"{DATAVERSE_URL}/.default"])
    return result.get("access_token")

def verificar_tabla_existe(token, logical_name):
    """Verificar si una tabla existe en Dataverse"""
    url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions(LogicalName='{logical_name}')?$select=LogicalName,EntitySetName"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return True, data.get("EntitySetName")
        return False, None
    except:
        return False, None

def obtener_relaciones_tabla(token, logical_name):
    """Obtener todas las relaciones (lookups) de una tabla"""
    url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions(LogicalName='{logical_name}')?$select=LogicalName&$expand=Attributes($select=LogicalName,AttributeType,Targets)"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            attributes = data.get("Attributes", [])
            lookups = []
            for attr in attributes:
                if attr.get("AttributeType") == "Lookup":
                    logical = attr.get("LogicalName")
                    targets = attr.get("Targets", [])
                    if targets:
                        lookups.append({
                            "campo": logical,
                            "hacia": targets[0] if isinstance(targets, list) else targets
                        })
            return lookups
        return []
    except:
        return []

def main():
    print("=" * 90)
    print("   ANÁLISIS COMPARATIVO: REQUISITOS vs REALIDAD")
    print("=" * 90)
    print()
    
    token = get_token()
    if not token:
        print("❌ No se pudo obtener token de autenticación")
        return
    
    # Definir tablas requeridas según requisitos originales
    tablas_requeridas = [
        {
            "nombre": "chats00 / adatawp0",
            "logical_name": "cr321_adatawp0",
            "descripcion": "Mensajes WhatsApp",
            "campos_criticos": ["cr321_from", "cr321_body", "cr321_timestamp", "cr321_type", "cr321_direction"],
            "relaciones_esperadas": []
        },
        {
            "nombre": "usuarios",
            "logical_name": "cr321_usuarios",
            "descripcion": "Usuarios del sistema",
            "campos_criticos": ["cr321_nombre", "cr321_correo", "cr321_clave", "cr321_rol", "cr321_activo"],
            "relaciones_esperadas": []
        },
        {
            "nombre": "grupos",
            "logical_name": "cr321_grup",
            "descripcion": "Grupos/Categorías (Menú WhatsApp)",
            "campos_criticos": ["cr321_idgrupo", "cr321_nombre", "cr321_tipo", "cr321_descripcion"],
            "relaciones_esperadas": [],
            "datos_iniciales": "4 grupos tipo A obligatorios"
        },
        {
            "nombre": "estados",
            "logical_name": "cr321_estado",
            "descripcion": "Estados de tickets",
            "campos_criticos": ["cr321_idestado", "cr321_nombre", "cr321_descripcion"],
            "relaciones_esperadas": [],
            "datos_iniciales": "5 estados recomendados"
        },
        {
            "nombre": "contacto",
            "logical_name": "cr321_contacto",
            "descripcion": "Contactos de clientes",
            "campos_criticos": ["cr321_nombre", "cr321_telefono", "cr321_email", "cr321_empresa"],
            "relaciones_esperadas": []
        },
        {
            "nombre": "ticket",
            "logical_name": "cr321_ticket",
            "descripcion": "Tickets de soporte",
            "campos_criticos": ["cr321_idticket", "cr321_fromnombre", "cr321_telefono", "cr321_descripcion", "cr321_tipo"],
            "relaciones_esperadas": [
                {"campo": "cr321_grupoid", "hacia": "cr321_grup"},
                {"campo": "cr321_estadoid", "hacia": "cr321_estado"},
                {"campo": "cr321_contactoid", "hacia": "cr321_contacto"}
            ]
        },
        {
            "nombre": "usuario_grupo",
            "logical_name": "cr321_usuariogrupo",
            "descripcion": "Relación usuarios-grupos",
            "campos_criticos": ["cr321_usuarioid", "cr321_grupoid"],
            "relaciones_esperadas": [
                {"campo": "cr321_usuarioid", "hacia": "cr321_usuarios"},
                {"campo": "cr321_grupoid", "hacia": "cr321_grup"}
            ]
        },
        {
            "nombre": "chatbots",
            "logical_name": "cr321_chatbot",
            "descripcion": "Configuración chatbots",
            "campos_criticos": ["cr321_name", "cr321_type", "cr321_config", "cr321_active"],
            "relaciones_esperadas": [],
            "datos_iniciales": "Chatbot 'Menu Principal WhatsApp'"
        },
        {
            "nombre": "flujos",
            "logical_name": "cr321_flows",
            "descripcion": "Flujos conversacionales",
            "campos_criticos": ["cr321_nombre", "cr321_chatbotid", "cr321_nodos", "cr321_edges", "cr321_version"],
            "relaciones_esperadas": [
                {"campo": "cr321_chatbotid", "hacia": "cr321_chatbot"}
            ]
        },
        {
            "nombre": "cuentas_whatsapp",
            "logical_name": "cr321_cuentadewhatsapp",
            "descripcion": "Múltiples cuentas WhatsApp",
            "campos_criticos": ["cr321_name", "cr321_phonenumberid", "cr321_accesstoken", "cr321_activo"],
            "relaciones_esperadas": []
        },
        {
            "nombre": "templates",
            "logical_name": "cr321_template",
            "descripcion": "Plantillas de mensajes",
            "campos_criticos": ["cr321_nombre", "cr321_contenido", "cr321_categoria", "cr321_idioma"],
            "relaciones_esperadas": []
        },
        {
            "nombre": "automatizaciones",
            "logical_name": "cr321_automatizacion",
            "descripcion": "Reglas de automatización",
            "campos_criticos": ["cr321_nombre", "cr321_trigger", "cr321_condiciones", "cr321_acciones", "cr321_activo"],
            "relaciones_esperadas": []
        }
    ]
    
    print("[1/3] VERIFICANDO EXISTENCIA DE TABLAS")
    print("-" * 90)
    print()
    
    tablas_existentes = []
    tablas_faltantes = []
    
    for tabla in tablas_requeridas:
        existe, entity_set = verificar_tabla_existe(token, tabla["logical_name"])
        if existe:
            tabla["entity_set"] = entity_set
            tablas_existentes.append(tabla)
            print(f"✅ {tabla['nombre']:25} → {tabla['logical_name']:30} (EntitySet: {entity_set})")
        else:
            tablas_faltantes.append(tabla)
            print(f"❌ {tabla['nombre']:25} → {tabla['logical_name']:30} FALTA")
    
    print()
    print("=" * 90)
    print(f"[2/3] VERIFICANDO RELACIONES (LOOKUPS)")
    print("=" * 90)
    print()
    
    relaciones_ok = []
    relaciones_faltantes = []
    
    for tabla in tablas_existentes:
        if not tabla.get("relaciones_esperadas"):
            continue
        
        print(f"\n📋 Tabla: {tabla['nombre']} ({tabla['logical_name']})")
        print("-" * 90)
        
        relaciones_actuales = obtener_relaciones_tabla(token, tabla["logical_name"])
        
        for rel_esperada in tabla["relaciones_esperadas"]:
            campo_esperado = rel_esperada["campo"]
            hacia_esperado = rel_esperada["hacia"]
            
            # Buscar si existe esta relación
            encontrada = False
            for rel_actual in relaciones_actuales:
                if campo_esperado in rel_actual["campo"] and hacia_esperado in rel_actual["hacia"]:
                    encontrada = True
                    break
            
            if encontrada:
                relaciones_ok.append({
                    "tabla": tabla["nombre"],
                    "campo": campo_esperado,
                    "hacia": hacia_esperado
                })
                print(f"  ✅ {campo_esperado:30} → {hacia_esperado}")
            else:
                relaciones_faltantes.append({
                    "tabla": tabla["nombre"],
                    "logical_name": tabla["logical_name"],
                    "campo": campo_esperado,
                    "hacia": hacia_esperado
                })
                print(f"  ❌ {campo_esperado:30} → {hacia_esperado:30} FALTA")
        
        # Mostrar relaciones adicionales no esperadas
        for rel_actual in relaciones_actuales:
            es_esperada = False
            for rel_esp in tabla.get("relaciones_esperadas", []):
                if rel_esp["campo"] in rel_actual["campo"]:
                    es_esperada = True
                    break
            
            if not es_esperada:
                print(f"  ℹ️  {rel_actual['campo']:30} → {rel_actual['hacia']:30} (adicional)")
    
    print()
    print("=" * 90)
    print("[3/3] RESUMEN EJECUTIVO")
    print("=" * 90)
    print()
    
    total_tablas = len(tablas_requeridas)
    total_existentes = len(tablas_existentes)
    total_faltantes = len(tablas_faltantes)
    
    print(f"📊 TABLAS:")
    print(f"   Total requeridas: {total_tablas}")
    print(f"   ✅ Existentes: {total_existentes} ({100*total_existentes//total_tablas}%)")
    print(f"   ❌ Faltantes: {total_faltantes}")
    print()
    
    if tablas_faltantes:
        print("⚠️  TABLAS FALTANTES:")
        for tabla in tablas_faltantes:
            print(f"   • {tabla['nombre']} ({tabla['logical_name']})")
        print()
    
    total_rel_esperadas = sum(len(t.get("relaciones_esperadas", [])) for t in tablas_existentes)
    total_rel_ok = len(relaciones_ok)
    total_rel_faltantes = len(relaciones_faltantes)
    
    print(f"🔗 RELACIONES (LOOKUPS):")
    print(f"   Total esperadas: {total_rel_esperadas}")
    print(f"   ✅ Implementadas: {total_rel_ok}")
    print(f"   ❌ Faltantes: {total_rel_faltantes}")
    print()
    
    if relaciones_faltantes:
        print("⚠️  RELACIONES FALTANTES:")
        for rel in relaciones_faltantes:
            print(f"   • {rel['tabla']:20} → {rel['campo']:30} apuntando a {rel['hacia']}")
        print()
    
    print("=" * 90)
    print("RECOMENDACIONES")
    print("=" * 90)
    print()
    
    if tablas_faltantes:
        print("1️⃣  CREAR TABLAS FALTANTES:")
        print("   • Ir a make.powerapps.com → Dataverse → Tablas → Nueva tabla")
        print("   • Crear en el orden recomendado (ver BACKUP_ESTRUCTURA_COMPLETA.md)")
        print()
    
    if relaciones_faltantes:
        print("2️⃣  AGREGAR RELACIONES FALTANTES:")
        print("   • Para cada relación faltante:")
        print("   • En la tabla origen, agregar campo de tipo 'Lookup'")
        print("   • Seleccionar la tabla destino")
        print("   • O ejecutar scripts automatizados de creación")
        print()
    
    # Verificar datos iniciales
    print("3️⃣  VERIFICAR DATOS INICIALES:")
    print("   • Ejecutar: python verificar_migracion.py")
    print("   • Verificar 4 grupos tipo A existen")
    print("   • Verificar chatbot 'Menu Principal WhatsApp' existe")
    print()
    
    print("4️⃣  PROBAR FUNCIONALIDADES:")
    print("   • Backend: .\\iniciar_backend.ps1")
    print("   • Frontend: .\\iniciar.ps1 LOCAL")
    print("   • Webhook: Configurar en Meta Developer Console")
    print()
    
    print("=" * 90)
    print(f"✅ Análisis completado - {total_existentes}/{total_tablas} tablas, {total_rel_ok}/{total_rel_esperadas} relaciones")
    print("=" * 90)

if __name__ == "__main__":
    main()
