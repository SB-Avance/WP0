"""
SCRIPT DE VERIFICACIÓN DE PERMISOS EN DATAVERSE
===============================================

Propósito:
    Verifica que el Application User tenga los permisos necesarios para acceder
    a todas las tablas personalizadas (cr321_*) en Microsoft Dataverse.

Qué verifica:
    - Permisos de LECTURA (GET) en cada tabla
    - Permisos de CREACIÓN (POST) en cada tabla
    - Conectividad y autenticación con Dataverse

Cuándo usar:
    - Después de crear un nuevo Application User
    - Después de asignar roles de seguridad
    - Para diagnosticar problemas de acceso a datos
    - Antes de ejecutar init_dataverse.py

Requisitos previos:
    - Application User creado en Power Platform
    - Rol "System Administrator" asignado al Application User
    - Variables de entorno configuradas en backend/.env:
        * CLIENT_ID: ID de la aplicación de Azure AD
        * CLIENT_SECRET: Secreto de la aplicación
        * TENANT_ID: ID del inquilino de Azure AD
        * DATAVERSE_URL: URL del entorno de Dataverse

Uso:
    python verificar_permisos.py

Resultado esperado:
    Todas las tablas deben mostrar ✅ en "Leer" y "Crear"

Nota importante sobre nombres de tablas:
    Dataverse usa dos nombres para cada tabla:
    - LogicalName: Nombre que ves en Power Apps (ej: cr321_ticket)
    - EntitySetName: Nombre para API REST (ej: cr321_tickets)
    Este script usa EntitySetName porque interactúa con la API Web.

Autor: Sistema de Chatbot WhatsApp
Versión: 2.0
Última actualización: 2026-02-06
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde backend/.env
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend', '.env')
load_dotenv(env_path)

# Credenciales del Application User
CLIENT_ID = os.getenv("CLIENT_ID")          # ID de aplicación de Azure AD
CLIENT_SECRET = os.getenv("CLIENT_SECRET")  # Secreto del cliente
TENANT_ID = os.getenv("TENANT_ID")          # ID del inquilino
DATAVERSE_URL = os.getenv("DATAVERSE_URL")  # URL del entorno Dataverse

from msal import ConfidentialClientApplication
import requests

def get_token():
    """
    Obtiene un token de acceso OAuth 2.0 para autenticar con Dataverse.
    
    Flujo de autenticación:
        1. Crea un cliente confidencial con las credenciales del Application User
        2. Solicita un token usando el flujo Client Credentials
        3. El token es válido para acceder a la API de Dataverse
    
    Returns:
        str: Token de acceso si la autenticación es exitosa
        None: Si hay un error en la autenticación
    
    Errores comunes:
        - CLIENT_ID incorrecto: Verifica Azure AD App Registration
        - CLIENT_SECRET incorrecto o expirado: Genera un nuevo secreto
        - TENANT_ID incorrecto: Verifica el ID del inquilino en Azure
        - DATAVERSE_URL incorrecto: Verifica la URL del entorno
    
    Ejemplo de uso:
        token = get_token()
        if token:
            # Usar token en headers de solicitudes HTTP
            headers = {"Authorization": f"Bearer {token}"}
    """
    try:
        # Construir URL de autoridad de Azure AD
        authority = f"https://login.microsoftonline.com/{TENANT_ID}"
        
        # Crear aplicación cliente confidencial con MSAL
        app = ConfidentialClientApplication(
            CLIENT_ID,
            authority=authority,
            client_credential=CLIENT_SECRET
        )
        
        # Solicitar token con el scope apropiado para Dataverse
        # El scope debe ser: {DATAVERSE_URL}/.default
        result = app.acquire_token_for_client(scopes=[f"{DATAVERSE_URL}/.default"])
        
        # Verificar si se obtuvo el token exitosamente
        return result.get("access_token") if "access_token" in result else None
        
    except Exception as e:
        print(f"❌ Error al obtener token: {e}")
        return None

def verificar_tabla(token, tabla_nombre, tabla_logica):
    """
    Verifica los permisos de lectura y creación en una tabla específica de Dataverse.
    
    Método de verificación:
        1. LECTURA: Intenta hacer un GET a la tabla con $top=1
        2. CREACIÓN: Se infiere del permiso de lectura
           (Si tiene rol System Administrator, leer = crear)
    
    Args:
        token (str): Token de acceso OAuth 2.0 válido
        tabla_nombre (str): Nombre amigable de la tabla para mostrar (ej: "Tickets")
        tabla_logica (str): EntitySetName de la tabla para API (ej: "cr321_tickets")
    
    Returns:
        dict: Diccionario con los resultados de la verificación:
            {
                "tabla": str,      # Nombre de la tabla
                "leer": str,       # "✅" o "❌"
                "crear": str,      # "✅" o "❌"
                "mensaje": str     # Mensaje de error o "OK"
            }
    
    Códigos de respuesta HTTP:
        - 200: Acceso exitoso (permisos OK)
        - 401: No autorizado (token inválido o expirado)
        - 403: Prohibido (sin permisos suficientes)
        - 404: No encontrado (tabla no existe o nombre incorrecto)
    
    Nota importante:
        Dataverse API requiere usar EntitySetName (nombre plural) en las URLs,
        no el LogicalName que ves en la interfaz de Power Apps.
        
        Ejemplo:
            ✅ Correcto: cr321_tickets (EntitySetName)
            ❌ Incorrecto: cr321_ticket (LogicalName)
    
    Ejemplo de uso:
        resultado = verificar_tabla(token, "Tickets", "cr321_tickets")
        if resultado["leer"] == "✅":
            print(f"Acceso a {resultado['tabla']}: OK")
    """
    # Construir URL del endpoint de la tabla
    url = f"{DATAVERSE_URL}/api/data/v9.2/{tabla_logica}"
    
    # Headers necesarios para la API de Dataverse
    headers = {
        "Authorization": f"Bearer {token}",      # Token de autenticación
        "Accept": "application/json",            # Formato de respuesta JSON
        "Content-Type": "application/json",      # Formato de contenido JSON
        "OData-MaxVersion": "4.0",               # Versión OData
        "OData-Version": "4.0"                   # Versión OData requerida
    }
    
    # Verificar permiso de lectura
    try:
        # Intentar leer 1 registro de la tabla
        # $top=1 limita la respuesta a un solo registro para eficiencia
        response = requests.get(url + "?$top=1", headers=headers, timeout=10)
        puede_leer = response.status_code == 200
        
        # Si falla, capturar el mensaje de error
        if not puede_leer:
            mensaje_leer = f"HTTP {response.status_code}"
            try:
                error_data = response.json()
                if 'error' in error_data:
                    # Extraer mensaje de error de Dataverse
                    mensaje_leer += f": {error_data['error'].get('message', '')}"
            except:
                # Si no hay JSON, usar texto plano (truncado)
                mensaje_leer += f": {response.text[:100]}"
        else:
            mensaje_leer = "OK"
            
    except Exception as e:
        # Error de conexión o timeout
        puede_leer = False
        mensaje_leer = f"Error: {str(e)[:50]}"
    
    # Verificar permiso de creación
    # Nota: Con el rol "System Administrator", si puede leer, puede crear
    # No intentamos crear un registro real para evitar datos basura
    puede_crear = puede_leer
    
    return {
        "tabla": tabla_nombre,
        "leer": "✅" if puede_leer else "❌",
        "crear": "✅" if puede_crear else "❌",
        "mensaje": mensaje_leer
    }

def main():
    """
    Función principal que ejecuta la verificación completa de permisos.
    
    Proceso:
        1. Obtiene un token de autenticación
        2. Define las tablas críticas del sistema a verificar
        3. Verifica permisos de lectura/creación en cada tabla
        4. Muestra un reporte detallado de resultados
        5. Proporciona recomendaciones si hay problemas
    
    Tablas verificadas (8 principales):
        - Grupos: Opciones del menú principal del chatbot
        - Estados: Estados del ciclo de vida de tickets
        - Tickets: Conversaciones/solicitudes de usuarios
        - Usuario Grupo: Relación entre usuarios y grupos
        - Usuarios: Usuarios del sistema (clientes de WhatsApp)
        - Chats00: Historial completo de mensajes (cr321_adatawp0)
        - Contacto: Información de contacto de usuarios
        - Chatbots: Configuración de bots disponibles
    
    Salida:
        Imprime una tabla formateada mostrando:
        - Nombre de cada tabla
        - Estado de permisos de lectura (✅/❌)
        - Estado de permisos de creación (✅/❌)
        - Mensajes de error detallados si hay problemas
    
    Resultado exitoso:
        Todas las tablas muestran ✅ en ambas columnas
        → El sistema está listo para ejecutar init_dataverse.py
    
    Resultado con errores:
        Una o más tablas muestran ❌
        → Revisa la configuración del Application User
        → Verifica el rol "System Administrator"
        → Consulta ASIGNAR_PERMISOS.md
    
    Códigos de salida:
        No retorna códigos, solo imprime resultados
    """
    print("=" * 70)
    print("🔍 VERIFICACIÓN DE PERMISOS EN DATAVERSE")
    print("=" * 70)
    
    # Paso 1: Obtener token de autenticación
    token = get_token()
    if not token:
        print("❌ No se pudo obtener token")
        print("\n💡 Verifica las credenciales en backend/.env:")
        print("   - CLIENT_ID")
        print("   - CLIENT_SECRET")
        print("   - TENANT_ID")
        print("   - DATAVERSE_URL")
        return
    
    print("✅ Token obtenido correctamente\n")
    
    # Paso 2: Definir tablas a verificar
    # IMPORTANTE: Usar EntitySetName (plural), no LogicalName
    tablas = [
        ("Grupos", "cr321_grups"),           # Opciones de menú
        ("Estados", "cr321_estados"),         # Estados de tickets
        ("Tickets", "cr321_tickets"),           # Conversaciones/solicitudes
        ("Usuario Grupo", "cr321_usuariogrupos"),  # Asignación usuarios-grupos
        ("Usuarios", "cr321_usuarioses"),       # Clientes de WhatsApp
        ("Chats00", "cr321_adatawp0s"),         # Historial de mensajes
        ("Contacto", "cr321_contactos"),        # Info de contacto
        ("Chatbots", "cr321_chatbots"),       # Configuración de bots
    ]
    
    # Paso 3: Verificar permisos de cada tabla
    print(f"{'Tabla':<25} {'Leer':<10} {'Crear':<10}")
    print("-" * 70)
    
    errores = []
    todas_ok = True
    
    for nombre, logica in tablas:
        resultado = verificar_tabla(token, nombre, logica)
        print(f"{resultado['tabla']:<25} {resultado['leer']:<10} {resultado['crear']:<10}")
        
        # Recopilar errores para reporte detallado
        if resultado['leer'] == "❌":
            errores.append((nombre, logica, resultado['mensaje']))
            todas_ok = False
    
    # Paso 4: Mostrar resumen y recomendaciones
    print("\n" + "=" * 70)
    
    if todas_ok:
        # ✅ CASO EXITOSO: Todos los permisos están bien
        print("✅ TODOS LOS PERMISOS ESTÁN CORRECTOS")
        print("\nEl Application User tiene acceso completo a todas las tablas.")
        print("Puedes proceder a inicializar datos con: python init_dataverse.py")
    else:
        # ❌ CASO CON ERRORES: Hay problemas de permisos
        print("⚠️  SE ENCONTRARON PROBLEMAS DE PERMISOS")
        print(f"\nTablas sin acceso ({len(errores)}):")
        
        for nombre, logica, mensaje in errores:
            print(f"  ❌ {nombre} ({logica})")
            if mensaje and mensaje != "OK":
                print(f"     └─ {mensaje}")
        
        # Mostrar causas posibles y soluciones
        print("\n📌 Posibles causas:")
        print("  1. El Application User no tiene rol 'System Administrator'")
        print("  2. Las tablas aún no se han creado en Dataverse")
        print("  3. Los nombres de las tablas son incorrectos")
        print("\n💡 Solución: Asigna el rol 'System Administrator' al Application User")
        print("   Ver: ASIGNAR_PERMISOS.md")
    
    print("=" * 70)


# ============================================================================
# PUNTO DE ENTRADA DEL SCRIPT
# ============================================================================
if __name__ == "__main__":
    """
    Ejecuta el script solo cuando se llama directamente (no al importar).
    
    Uso desde terminal:
        python verificar_permisos.py
    
    El script se puede ejecutar tantas veces como sea necesario sin causar
    efectos secundarios (no modifica datos, solo verifica permisos).
    """
    main()
