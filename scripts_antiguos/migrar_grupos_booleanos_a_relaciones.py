"""
Script de Migración: Campos Booleanos de Grupo → Tabla de Relaciones
=====================================================================

Migra los datos de los campos cr321_1, cr321_3, cr321_4 (booleanos)
a la tabla de relaciones cr321_usuario_gruposes (Many-to-Many)

Fecha: 7 de febrero de 2026
Autor: Sistema automatizado
"""
import requests
import sys
import os
from datetime import datetime

# Configurar path para imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

from dotenv import load_dotenv
load_dotenv()

# Obtener configuración
DATAVERSE_URL = os.getenv("DATAVERSE_URL")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")


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
            return None
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None


def obtener_usuarios_con_grupos_booleanos():
    """Obtener todos los usuarios y sus valores de campos booleanos"""
    print("\n📊 PASO 1: Obteniendo usuarios con grupos booleanos...")
    
    token = get_token()
    if not token:
        return None
    
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuarioses"
    url += "?$select=cr321_usuariosid,cr321_nombre,cr321_correo,cr321_1,cr321_3,cr321_4"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            usuarios = response.json().get("value", [])
            print(f"✅ {len(usuarios)} usuarios encontrados")
            
            # Estadísticas
            con_grupo_1 = sum(1 for u in usuarios if u.get("cr321_1") == True)
            con_grupo_3 = sum(1 for u in usuarios if u.get("cr321_3") == True)
            con_grupo_4 = sum(1 for u in usuarios if u.get("cr321_4") == True)
            
            print(f"\n📈 Estadísticas:")
            print(f"   - Usuarios con Grupo 1 (cr321_1=true): {con_grupo_1}")
            print(f"   - Usuarios con Grupo 3 (cr321_3=true): {con_grupo_3}")
            print(f"   - Usuarios con Grupo 4 (cr321_4=true): {con_grupo_4}")
            
            return usuarios
        else:
            print(f"❌ Error al obtener usuarios: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def obtener_mapeo_grupos():
    """Obtener IDs de grupos 1, 3 y 4 desde Dataverse"""
    print("\n📊 PASO 2: Obteniendo mapeo de grupos...")
    
    token = get_token()
    if not token:
        return None
    
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    
    # Buscar grupos con idgrupo 1, 3, 4
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_grups"
    url += "?$select=cr321_grupoid,cr321_idgrupo,cr321_nombre"
    url += "&$filter=cr321_idgrupo eq 1 or cr321_idgrupo eq 3 or cr321_idgrupo eq 4"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            grupos = response.json().get("value", [])
            
            if len(grupos) == 0:
                print("⚠️  ADVERTENCIA: No se encontraron grupos con idgrupo 1, 3 o 4")
                print("   Necesitas crear estos grupos primero en cr321_grup")
                print("\n   Ejemplo:")
                print("   - Grupo con cr321_idgrupo=1 (ej: Ventas)")
                print("   - Grupo con cr321_idgrupo=3 (ej: Soporte)")
                print("   - Grupo con cr321_idgrupo=4 (ej: Marketing)")
                return None
            
            # Crear mapeo: idgrupo → GUID
            mapeo = {g["cr321_idgrupo"]: {
                "guid": g["cr321_grupoid"],
                "nombre": g.get("cr321_nombre", f"Grupo {g['cr321_idgrupo']}")
            } for g in grupos}
            
            print(f"✅ {len(mapeo)} grupos mapeados:")
            for idgrupo, info in mapeo.items():
                print(f"   - Grupo {idgrupo}: {info['nombre']} (ID: {info['guid']})")
            
            return mapeo
        else:
            print(f"❌ Error al obtener grupos: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def crear_relacion_usuario_grupo(usuario_id, grupo_id, nombre_usuario, nombre_grupo):
    """Crear una relación en cr321_usuario_gruposes"""
    token = get_token()
    if not token:
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # Verificar si ya existe
    check_url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuario_gruposes"
    check_url += f"?$filter=_cr321_usuarioid_value eq {usuario_id} and _cr321_grupoid_value eq {grupo_id}"
    
    try:
        response = requests.get(check_url, headers=headers)
        if response.status_code == 200:
            existentes = response.json().get("value", [])
            if len(existentes) > 0:
                print(f"   ⏭️  {nombre_usuario} → {nombre_grupo} (ya existe)")
                return True  # Ya existe, no es error
        
        # Crear relación
        url_crear = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuario_gruposes"
        payload = {
            "cr321_usuarioid@odata.bind": f"/cr321_usuarioses({usuario_id})",
            "cr321_grupoid@odata.bind": f"/cr321_grups({grupo_id})"
        }
        
        response = requests.post(url_crear, json=payload, headers=headers)
        if response.status_code == 204:
            print(f"   ✅ {nombre_usuario} → {nombre_grupo}")
            return True
        else:
            print(f"   ❌ Error al crear relación: {response.status_code}")
            print(f"      {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def migrar_datos(usuarios, mapeo_grupos):
    """Ejecutar migración de datos"""
    print("\n📊 PASO 3: Migrando datos a tabla de relaciones...")
    print("="*70)
    
    total_relaciones = 0
    exitosas = 0
    fallidas = 0
    
    for usuario in usuarios:
        usuario_id = usuario.get("cr321_usuariosid")
        nombre = usuario.get("cr321_nombre", "Sin nombre")
        
        # Procesar cr321_1 (Grupo 1)
        if usuario.get("cr321_1") == True and 1 in mapeo_grupos:
            grupo_info = mapeo_grupos[1]
            total_relaciones += 1
            if crear_relacion_usuario_grupo(usuario_id, grupo_info["guid"], nombre, grupo_info["nombre"]):
                exitosas += 1
            else:
                fallidas += 1
        
        # Procesar cr321_3 (Grupo 3)
        if usuario.get("cr321_3") == True and 3 in mapeo_grupos:
            grupo_info = mapeo_grupos[3]
            total_relaciones += 1
            if crear_relacion_usuario_grupo(usuario_id, grupo_info["guid"], nombre, grupo_info["nombre"]):
                exitosas += 1
            else:
                fallidas += 1
        
        # Procesar cr321_4 (Grupo 4)
        if usuario.get("cr321_4") == True and 4 in mapeo_grupos:
            grupo_info = mapeo_grupos[4]
            total_relaciones += 1
            if crear_relacion_usuario_grupo(usuario_id, grupo_info["guid"], nombre, grupo_info["nombre"]):
                exitosas += 1
            else:
                fallidas += 1
    
    print("\n" + "="*70)
    print(f"📊 RESUMEN DE MIGRACIÓN:")
    print(f"   - Total relaciones procesadas: {total_relaciones}")
    print(f"   - Exitosas: {exitosas}")
    print(f"   - Fallidas: {fallidas}")
    
    return exitosas, fallidas


def validar_migracion(usuarios, mapeo_grupos):
    """Validar que la migración fue exitosa"""
    print("\n📊 PASO 4: Validando migración...")
    print("="*70)
    
    token = get_token()
    if not token:
        return False
    
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    
    errores = []
    
    for usuario in usuarios:
        usuario_id = usuario.get("cr321_usuariosid")
        nombre = usuario.get("cr321_nombre", "Sin nombre")
        
        # Obtener relaciones actuales del usuario
        url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuario_gruposes"
        url += f"?$filter=_cr321_usuarioid_value eq {usuario_id}"
        url += "&$expand=cr321_grupoid($select=cr321_idgrupo,cr321_nombre)"
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                relaciones = response.json().get("value", [])
                grupos_actuales = {rel.get("cr321_grupoid", {}).get("cr321_idgrupo") for rel in relaciones}
                
                # Verificar cada campo booleano
                if usuario.get("cr321_1") == True and 1 not in grupos_actuales:
                    errores.append(f"❌ {nombre}: Tiene cr321_1=true pero falta relación con Grupo 1")
                
                if usuario.get("cr321_3") == True and 3 not in grupos_actuales:
                    errores.append(f"❌ {nombre}: Tiene cr321_3=true pero falta relación con Grupo 3")
                
                if usuario.get("cr321_4") == True and 4 not in grupos_actuales:
                    errores.append(f"❌ {nombre}: Tiene cr321_4=true pero falta relación con Grupo 4")
        except Exception as e:
            errores.append(f"❌ Error al validar {nombre}: {e}")
    
    if len(errores) == 0:
        print("✅ Validación exitosa: Todos los datos fueron migrados correctamente")
        return True
    else:
        print(f"⚠️  Se encontraron {len(errores)} errores:")
        for error in errores[:10]:  # Mostrar solo los primeros 10
            print(f"   {error}")
        if len(errores) > 10:
            print(f"   ... y {len(errores) - 10} errores más")
        return False


def main():
    """Función principal"""
    print("\n" + "="*70)
    print("🔄 MIGRACIÓN DE GRUPOS BOOLEANOS A TABLA DE RELACIONES")
    print("="*70)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nEste script migrará:")
    print("  cr321_1 (Boolean) → cr321_usuario_gruposes (Grupo 1)")
    print("  cr321_3 (Boolean) → cr321_usuario_gruposes (Grupo 3)")
    print("  cr321_4 (Boolean) → cr321_usuario_gruposes (Grupo 4)")
    print("="*70)
    
    # Confirmación
    respuesta = input("\n¿Deseas continuar con la migración? (si/no): ").lower().strip()
    if respuesta not in ['si', 'sí', 's', 'yes', 'y']:
        print("\n❌ Migración cancelada por el usuario")
        return
    
    # PASO 1: Obtener usuarios
    usuarios = obtener_usuarios_con_grupos_booleanos()
    if usuarios is None:
        print("\n❌ No se pudieron obtener usuarios. Abortando migración.")
        return
    
    if len(usuarios) == 0:
        print("\n⚠️  No hay usuarios para migrar")
        return
    
    # PASO 2: Obtener mapeo de grupos
    mapeo_grupos = obtener_mapeo_grupos()
    if mapeo_grupos is None:
        print("\n❌ No se pudo obtener mapeo de grupos. Abortando migración.")
        print("\n💡 ACCIÓN REQUERIDA:")
        print("   1. Crear grupos en cr321_grup con los siguiente cr321_idgrupo:")
        print("      - cr321_idgrupo = 1 (ej: Ventas)")
        print("      - cr321_idgrupo = 3 (ej: Soporte)")
        print("      - cr321_idgrupo = 4 (ej: Marketing)")
        print("   2. Ejecutar este script nuevamente")
        return
    
    # PASO 3: Migrar datos
    exitosas, fallidas = migrar_datos(usuarios, mapeo_grupos)
    
    if fallidas > 0:
        print(f"\n⚠️  Migración completada con {fallidas} errores")
        print("   Revisa los mensajes de error arriba para más detalles")
    
    # PASO 4: Validar
    if validar_migracion(usuarios, mapeo_grupos):
        print("\n" + "="*70)
        print("✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
        print("="*70)
        print("\n📋 PRÓXIMOS PASOS:")
        print("   1. Verificar manualmente algunas relaciones en Power Apps")
        print("   2. Remover campos cr321_1, cr321_3, cr321_4 de vistas")
        print("   3. Remover campos cr321_1, cr321_3, cr321_4 de formularios")
        print("   4. Verificar flujos de Power Automate")
        print("   5. Una vez confirmado, eliminar campos desde Power Apps")
        print("\n📄 Ver documentación completa en:")
        print("   docs/DEPENDENCIAS_CAMPOS_GRUPO_USUARIOS.md")
    else:
        print("\n⚠️  La validación encontró inconsistencias")
        print("   Se recomienda revisar manualmente antes de eliminar los campos booleanos")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Migración interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
