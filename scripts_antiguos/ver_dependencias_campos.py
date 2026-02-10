"""
Script Rápido: Ver Dependencias de Campos
==========================================
Consulta directamente las dependencias de cr321_1, cr321_3, cr321_4
desde la API de Dataverse sin necesidad de abrir Power Apps

Fecha: 7 de febrero de 2026
"""
import requests
import sys
import os
from datetime import datetime

# Configurar path para imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

from dotenv import load_dotenv

# Cargar .env desde el directorio backend
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend', '.env')
load_dotenv(env_path)

# Obtener configuración
DATAVERSE_URL = os.getenv("DATAVERSE_URL")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")

# Mapeo de tipos de componentes
COMPONENT_TYPES = {
    1: "Entidad/Tabla",
    2: "Atributo/Campo",
    9: "Atributo Option Set",
    10: "Relación Entidad",
    11: "Relación Clave Entidad",
    13: "Entidad Administrada",
    20: "Rol",
    21: "Privilegio de Rol",
    24: "Vistas Guardadas (Display String)",
    25: "Vistas Guardadas (Query)",
    26: "Vista Guardada",
    29: "Flujo de Trabajo (Process)",
    48: "Regla de Negocio",
    60: "Formulario",
    61: "Gráfico",
    62: "Dashboard",
    80: "Aplicación (Canvas/Model-Driven)",
    90: "Mapa del Sitio",
    91: "Configuración de Conexión",
    92: "Conector",
    93: "Ambiente",
    95: "Flujo (Cloud Flow)",
    300: "Canvas App",
    371: "Conector",
    380: "Flujo de Desktop",
}

def get_token():
    """Obtener token de autenticación de Azure AD"""
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": f"{DATAVERSE_URL}/.default",
        "grant_type": "client_credentials"
    }
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            print(f"❌ Error obteniendo token: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None


def obtener_metadata_campo(campo_nombre):
    """Obtener metadata del campo para obtener su MetadataId"""
    print(f"\n🔍 Buscando metadata de {campo_nombre}...")
    
    token = get_token()
    if not token:
        return None
    
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    
    # Consultar metadata de la entidad cr321_usuarios
    url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions(LogicalName='cr321_usuarios')/Attributes"
    url += f"?$filter=LogicalName eq '{campo_nombre}'"
    url += "&$select=MetadataId,LogicalName,DisplayName,AttributeType"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            campos = data.get("value", [])
            if campos:
                campo = campos[0]
                metadata_id = campo.get("MetadataId")
                display_name = campo.get("DisplayName", {}).get("UserLocalizedLabel", {}).get("Label", campo_nombre)
                attr_type = campo.get("AttributeType")
                
                print(f"✅ Campo encontrado:")
                print(f"   - Nombre: {campo_nombre}")
                print(f"   - Nombre para mostrar: {display_name}")
                print(f"   - Tipo: {attr_type}")
                print(f"   - MetadataId: {metadata_id}")
                
                return metadata_id
            else:
                print(f"⚠️  Campo '{campo_nombre}' no encontrado en la tabla cr321_usuarios")
                print(f"   Puede que ya haya sido eliminado o no exista")
                return None
        else:
            print(f"❌ Error al obtener metadata: {response.status_code}")
            print(f"   URL: {url}")
            print(f"   Respuesta: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def obtener_dependencias(metadata_id, campo_nombre):
    """Obtener dependencias de un campo usando su MetadataId"""
    print(f"\n📊 Consultando dependencias de {campo_nombre}...")
    
    token = get_token()
    if not token:
        return []
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # Usar RetrieveDependentComponents para obtener dependencias
    url = f"{DATAVERSE_URL}/api/data/v9.2/RetrieveDependentComponents"
    
    payload = {
        "ObjectId": metadata_id,
        "ComponentType": 2  # 2 = Attribute/Campo
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            # La respuesta puede estar en diferentes formatos
            if isinstance(data, dict):
                # Intentar diferentes claves posibles
                dependencias = data.get("EntityCollection", {}).get("Entities", [])
                if not dependencias:
                    dependencias = data.get("value", [])
                if not dependencias:
                    dependencias = data.get("Dependencies", [])
            else:
                dependencias = []
            
            return dependencias
        else:
            print(f"⚠️  No se pudieron obtener dependencias: {response.status_code}")
            print(f"   Respuesta: {response.text[:500]}")
            
            # Intentar método alternativo
            return obtener_dependencias_alternativo(metadata_id, campo_nombre)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return []


def obtener_dependencias_alternativo(metadata_id, campo_nombre):
    """Método alternativo para obtener dependencias usando FetchXML"""
    print(f"   🔄 Intentando método alternativo...")
    
    token = get_token()
    if not token:
        return []
    
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    
    # Consultar directamente la tabla de dependencias
    url = f"{DATAVERSE_URL}/api/data/v9.2/dependencies"
    url += f"?$filter=requiredcomponentobjectid eq {metadata_id}"
    url += "&$select=dependentcomponentobjectid,dependentcomponenttype"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get("value", [])
        else:
            print(f"   ⚠️  Método alternativo también falló: {response.status_code}")
            return []
    except Exception as e:
        print(f"   ❌ Error en método alternativo: {e}")
        return []


def obtener_nombre_componente(component_id, component_type):
    """Obtener el nombre de un componente dado su ID y tipo"""
    token = get_token()
    if not token:
        return "Desconocido"
    
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    
    # Mapeo de tipos a entidades
    type_to_entity = {
        26: "savedqueries",  # Vistas del sistema
        60: "systemforms",   # Formularios
        29: "workflows",     # Flujos de trabajo
        48: "businessrules", # Reglas de negocio
    }
    
    entity_name = type_to_entity.get(component_type)
    if not entity_name:
        return f"Componente tipo {component_type}"
    
    try:
        url = f"{DATAVERSE_URL}/api/data/v9.2/{entity_name}({component_id})?$select=name"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            return data.get("name", "Sin nombre")
        else:
            return f"ID: {component_id}"
    except:
        return f"ID: {component_id}"


def mostrar_dependencias(campo_nombre, dependencias):
    """Mostrar las dependencias de forma legible"""
    if not dependencias or len(dependencias) == 0:
        print(f"\n✅ {campo_nombre}: SIN DEPENDENCIAS (puede eliminarse)")
        return 0
    
    print(f"\n⚠️  {campo_nombre}: {len(dependencias)} DEPENDENCIA(S) ENCONTRADA(S)")
    print("="*70)
    
    # Agrupar por tipo
    por_tipo = {}
    for dep in dependencias:
        # Obtener tipo de componente
        comp_type = dep.get("dependentcomponenttype") or dep.get("DependentComponentType") or dep.get("ComponentType")
        
        if comp_type not in por_tipo:
            por_tipo[comp_type] = []
        por_tipo[comp_type].append(dep)
    
    # Mostrar agrupados
    for comp_type, items in sorted(por_tipo.items()):
        tipo_nombre = COMPONENT_TYPES.get(comp_type, f"Tipo Desconocido ({comp_type})")
        print(f"\n📌 {tipo_nombre}: {len(items)} componente(s)")
        
        for i, item in enumerate(items[:5], 1):  # Mostrar solo primeros 5
            comp_id = item.get("dependentcomponentobjectid") or item.get("DependentComponentObjectId")
            nombre = obtener_nombre_componente(comp_id, comp_type) if comp_id else "Desconocido"
            print(f"   {i}. {nombre}")
        
        if len(items) > 5:
            print(f"   ... y {len(items) - 5} más")
    
    return len(dependencias)


def generar_reporte_accion(total_cr321_1, total_cr321_3, total_cr321_4):
    """Generar reporte con acciones recomendadas"""
    print("\n" + "="*70)
    print("📋 REPORTE FINAL")
    print("="*70)
    
    total_dependencias = total_cr321_1 + total_cr321_3 + total_cr321_4
    
    if total_dependencias == 0:
        print("\n✅ ¡EXCELENTE! No hay dependencias activas")
        print("\n🎯 PUEDES ELIMINAR LOS CAMPOS AHORA:")
        print("   1. Ir a Power Apps → Tablas → cr321_usuarios → Columnas")
        print("   2. Eliminar cr321_1")
        print("   3. Eliminar cr321_3")
        print("   4. Eliminar cr321_4")
        print("   5. Publicar personalizaciones")
    else:
        print(f"\n⚠️  Total de dependencias: {total_dependencias}")
        print(f"\n   - cr321_1: {total_cr321_1} dependencia(s)")
        print(f"   - cr321_3: {total_cr321_3} dependencia(s)")
        print(f"   - cr321_4: {total_cr321_4} dependencia(s)")
        
        print("\n🎯 ACCIONES REQUERIDAS:")
        print("\n   1. VISTAS: Si hay dependencias tipo 26 (Vista Guardada)")
        print("      → Power Apps → Tablas → cr321_usuarios → Vistas")
        print("      → Abrir cada vista y remover columnas cr321_1, cr321_3, cr321_4")
        
        print("\n   2. FORMULARIOS: Si hay dependencias tipo 60 (Formulario)")
        print("      → Power Apps → Tablas → cr321_usuarios → Formularios")
        print("      → Abrir cada formulario y remover campos cr321_1, cr321_3, cr321_4")
        
        print("\n   3. FLUJOS: Si hay dependencias tipo 29 o 95 (Workflow/Flow)")
        print("      → Power Automate → Mis flujos")
        print("      → Desactivar o actualizar flujos que usen estos campos")
        
        print("\n   4. Después de limpiar, ejecutar este script nuevamente para verificar")
        
    print("\n" + "="*70)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)


def main():
    """Función principal"""
    print("\n" + "="*70)
    print("🔍 CONSULTA RÁPIDA DE DEPENDENCIAS")
    print("="*70)
    print("Campos: cr321_1, cr321_3, cr321_4")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    campos = ["cr321_1", "cr321_3", "cr321_4"]
    resultados = {}
    
    for campo in campos:
        # Obtener MetadataId del campo
        metadata_id = obtener_metadata_campo(campo)
        
        if metadata_id:
            # Obtener dependencias
            dependencias = obtener_dependencias(metadata_id, campo)
            
            # Mostrar resultados
            total = mostrar_dependencias(campo, dependencias)
            resultados[campo] = total
        else:
            print(f"\n❌ No se pudo analizar {campo}")
            resultados[campo] = -1
    
    # Generar reporte final
    generar_reporte_accion(
        resultados.get("cr321_1", 0),
        resultados.get("cr321_3", 0),
        resultados.get("cr321_4", 0)
    )
    
    print("\n✅ Análisis completado")
    print("\n💡 AYUDA:")
    print("   - Si hay dependencias, revisar la sección ACCIONES REQUERIDAS arriba")
    print("   - Si no hay dependencias, puedes eliminar los campos desde Power Apps")
    print("   - Ver guía completa: docs/GUIA_RAPIDA_ELIMINAR_CAMPOS_GRUPO.md")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Análisis interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
