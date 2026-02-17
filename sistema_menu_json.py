"""
Sistema de Menú con Configuración JSON Completa
==============================================

Usa el campo cr321_config existente en Dataverse para almacenar
toda la configuración del menú en formato JSON.

Características:
- JSON completo en cr321_config (campo existente)
- Estructura jerárquica (menús → submenús)
- Handlers dinámicos con códigos
- Grupos configurables por submenú
"""

import json
import os
import importlib
import sys
from pathlib import Path
from typing import Dict, Optional, List
import requests
from datetime import datetime, timedelta
from dataclasses import dataclass


# ============================================================================
# CONFIGURACIÓN
# ============================================================================

DATAVERSE_URL = os.getenv("DATAVERSE_URL", "https://tu-org.crm.dynamics.com/api/data/v9.2")
CLIENT_ID = os.getenv("CLIENT_ID", "tu-client-id")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "tu-client-secret")
TENANT_ID = os.getenv("TENANT_ID", "tu-tenant-id")

# Nombre del chatbot activo (cambiar aquí para testing A/B)
CHATBOT_ACTIVO = "Chatbot1"  # O "Chatbot2" para testing


# ============================================================================
# CLASES DE DATOS
# ============================================================================

@dataclass
class ConfigMenu:
    """Configuración completa del menú desde JSON"""
    version: str
    chatbot_id: str
    descripcion: str
    menus: List[Dict]
    configuracion_general: Dict
    
    @classmethod
    def from_json(cls, json_str: str):
        """Crea instancia desde string JSON"""
        data = json.loads(json_str)
        return cls(
            version=data.get('version', '1.0'),
            chatbot_id=data.get('chatbot_id', 'unknown'),
            descripcion=data.get('descripcion', ''),
            menus=data.get('menus', []),
            configuracion_general=data.get('configuracion_general', {})
        )


@dataclass
class ConfigHandler:
    """Configuración de un handler desde archivo JSON externo"""
    codigo: str
    archivo: str
    clase: str
    activo: bool
    grupo_override: Optional[str] = None
    usa_grupo_de_dataverse: bool = True


# ============================================================================
# SISTEMA PRINCIPAL
# ============================================================================

class SistemaMenuJSON:
    """
    Sistema de menú usando configuración JSON completa en Dataverse.
    
    Flujo:
    1. Cargar cr321_config desde Dataverse (campo existente)
    2. Parsear JSON completo
    3. Generar menús dinámicamente
    4. Ejecutar handlers según selección
    """
    
    def __init__(self, nombre_chatbot: str = CHATBOT_ACTIVO):
        """
        Inicializa el sistema.
        
        Args:
            nombre_chatbot: Nombre del chatbot a usar (default: CHATBOT_ACTIVO)
        """
        print(f"\n{'='*60}")
        print(f"SISTEMA DE MENÚ CON JSON")
        print(f"{'='*60}\n")
        
        # 1. Obtener token de Dataverse
        self.token = self._obtener_token()
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
        print(f"✓ Token obtenido")
        
        # 2. Cargar configuración del chatbot desde Dataverse
        self.config_menu = self._cargar_config_chatbot(nombre_chatbot)
        print(f"✓ Configuración cargada: {self.config_menu.chatbot_id}")
        print(f"  Versión: {self.config_menu.version}")
        print(f"  Menús disponibles: {len(self.config_menu.menus)}")
        
        # 3. Cargar catálogo de handlers
        self.config_handlers = self._cargar_config_handlers()
        print(f"✓ Handlers disponibles: {len(self.config_handlers)}")
        
        # 4. Validar grupos del menú
        self._validar_grupos_menu()
        
        # 5. Estado de usuarios (en memoria, podrías usar Redis)
        self.estados_usuarios = {}
    
    
    def _obtener_token(self) -> str:
        """Obtiene token OAuth de Microsoft"""
        
        token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
        
        data = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "scope": f"{DATAVERSE_URL}/.default",
            "grant_type": "client_credentials"
        }
        
        response = requests.post(token_url, data=data)
        
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            raise Exception(f"Error obteniendo token: {response.text}")
    
    
    def _cargar_config_chatbot(self, nombre_chatbot: str) -> ConfigMenu:
        """
        Carga la configuración completa del chatbot desde Dataverse.
        
        Lee el campo cr321_config (que ya existe) y parsea el JSON completo.
        
        Args:
            nombre_chatbot: Nombre del chatbot (ej: "Chatbot1")
        
        Returns:
            ConfigMenu con la configuración completa
        """
        
        print(f"\n→ Buscando chatbot: {nombre_chatbot}")
        
        response = requests.get(
            f"{DATAVERSE_URL}/cr321_chatbots",
            headers=self.headers,
            params={
                "$filter": f"cr321_name eq '{nombre_chatbot}' and cr321_active eq true",
                "$select": "cr321_name,cr321_config,cr321_active"
            }
        )
        
        if response.status_code == 200:
            data = response.json()["value"]
            
            if not data:
                raise Exception(f"No se encontró chatbot activo: {nombre_chatbot}")
            
            chatbot_record = data[0]
            
            # Verificar que esté activo (doble verificación)
            if not chatbot_record.get('cr321_active', False):
                raise Exception(f"Chatbot '{nombre_chatbot}' está inactivo")
            
            # Obtener el JSON del campo cr321_config
            config_json = chatbot_record.get('cr321_config')
            
            if not config_json:
                raise Exception(f"Campo cr321_config vacío para chatbot: {nombre_chatbot}")
            
            # Parsear JSON
            try:
                config = ConfigMenu.from_json(config_json)
                return config
            except json.JSONDecodeError as e:
                raise Exception(f"Error parseando JSON de cr321_config: {e}")
        
        raise Exception(f"Error consultando Dataverse: {response.status_code}")
    
    
    def _cargar_config_handlers(self) -> Dict[str, ConfigHandler]:
        """
        Carga el catálogo de handlers desde archivo JSON externo.
        
        Returns:
            Dict {codigo: ConfigHandler}
        """
        
        ruta_json = Path(__file__).parent / "handlers" / "config_handlers.json"
        
        if not ruta_json.exists():
            print(f"⚠️ No se encontró {ruta_json}, usando handlers básicos")
            return {}
        
        with open(ruta_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        config_handlers = {}
        for codigo, config in data.items():
            config_handlers[codigo] = ConfigHandler(
                codigo=codigo,
                archivo=config['archivo'],
                clase=config['clase'],
                activo=config.get('activo', True),
                grupo_override=config.get('grupo_override'),
                usa_grupo_de_dataverse=config.get('usa_grupo_de_dataverse', True)
            )
        
        return config_handlers
    
    
    def _validar_grupos_menu(self):
        """
        Valida que todos los grupo_id del menú existan en cr321_grupos.
        
        Advertencias si encuentra GUIDs inválidos.
        """
        
        print("\n→ Validando grupos del menú...")
        
        # Obtener todos los grupos válidos de Dataverse
        try:
            response = requests.get(
                f"{DATAVERSE_URL}/cr321_grupos",
                headers=self.headers,
                params={
                    "$select": "cr321_grupoid,cr321_nombre"
                }
            )
            
            if response.status_code == 200:
                grupos_validos = {g['cr321_grupoid']: g.get('cr321_nombre', 'Sin nombre') 
                                 for g in response.json()["value"]}
            else:
                print(f"  ⚠️ No se pudieron validar grupos: {response.status_code}")
                return
        except Exception as e:
            print(f"  ⚠️ Error validando grupos: {e}")
            return
        
        # Validar cada grupo_id del menú
        grupos_invalidos = []
        grupos_validos_count = 0
        
        for menu in self.config_menu.menus:
            for submenu in menu.get('submenus', []):
                grupo_id = submenu.get('grupo_id')
                
                if grupo_id and grupo_id != "null":
                    # Limpiar el GUID (quitar llaves si las tiene)
                    guid_limpio = grupo_id.strip('{}').lower()
                    
                    # Buscar en grupos válidos (case insensitive)
                    encontrado = False
                    for guid_valido in grupos_validos.keys():
                        if guid_valido.lower() == guid_limpio:
                            encontrado = True
                            break
                    
                    if encontrado:
                        grupos_validos_count += 1
                    else:
                        grupos_invalidos.append({
                            'submenu': submenu.get('numero'),
                            'nombre': submenu.get('nombre'),
                            'grupo_id': grupo_id
                        })
        
        # Reportar resultados
        if grupos_invalidos:
            print(f"  ⚠️ {len(grupos_invalidos)} grupo(s) inválido(s) encontrado(s):")
            for item in grupos_invalidos[:3]:  # Mostrar primeros 3
                print(f"     - {item['submenu']}: {item['nombre']} → {item['grupo_id']}")
            if len(grupos_invalidos) > 3:
                print(f"     ... y {len(grupos_invalidos) - 3} más")
            print("  💡 Ejecuta: python listar_grupos_dataverse.py para ver grupos válidos")
        else:
            print(f"  ✓ Todos los grupos válidos ({grupos_validos_count} verificados)")
    
    
    def obtener_menu(self, numero: str) -> Optional[Dict]:
        """
        Obtiene un menú principal por su número.
        
        Args:
            numero: Número del menú (ej: "1", "2", "3")
        
        Returns:
            Dict con config del menú o None
        """
        
        for menu in self.config_menu.menus:
            if menu['numero'] == numero:
                return menu
        
        return None
    
    
    def obtener_submenu(self, numero: str) -> Optional[Dict]:
        """
        Obtiene configuración de un submenú específico.
        
        Args:
            numero: Número del submenú (ej: "1.1", "2.3")
        
        Returns:
            Dict con config del submenú o None
        """
        
        for menu in self.config_menu.menus:
            for submenu in menu.get('submenus', []):
                if submenu['numero'] == numero:
                    return submenu
        
        return None
    
    
    def generar_mensaje_bienvenida(self) -> str:
        """Genera mensaje de bienvenida"""
        
        return self.config_menu.configuracion_general.get(
            'mensaje_bienvenida',
            'Hola, ¿en qué puedo ayudarte?'
        )
    
    
    def generar_mensaje_menu_principal(self) -> str:
        """Genera el mensaje del menú principal"""
        
        mensaje = "📋 *Menú Principal*\n\n"
        
        for menu in self.config_menu.menus:
            if menu.get('activo', True):
                mensaje += f"{menu['numero']}. {menu['nombre']}\n"
        
        mensaje += "\n💬 Escribe el número de la opción"
        
        return mensaje
    
    
    def generar_mensaje_submenu(self, numero_menu: str) -> str:
        """
        Genera el mensaje de un submenú específico.
        
        Args:
            numero_menu: Número del menú (ej: "1", "2")
        
        Returns:
            String con el mensaje del submenú
        """
        
        # Buscar menú
        menu = self.obtener_menu(numero_menu)
        
        if not menu:
            return "❌ Opción no válida. Por favor intenta de nuevo."
        
        if not menu.get('activo', True):
            return "⚠️ Esta opción no está disponible actualmente."
        
        mensaje = f"📋 *{menu['nombre']}*\n"
        
        if menu.get('descripcion'):
            mensaje += f"{menu['descripcion']}\n"
        
        mensaje += "\n"
        
        # Listar submenús
        for submenu in menu.get('submenus', []):
            if submenu.get('activo', True):
                mensaje += f"{submenu['numero']}. {submenu['nombre']}\n"
        
        mensaje += "\n0. ⬅️ Volver al menú principal"
        mensaje += "\n\n💬 Escribe el número de la opción"
        
        return mensaje
    
    
    def procesar_seleccion(self, from_user: str, numero_seleccion: str) -> str:
        """
        Procesa la selección del usuario y ejecuta el handler correspondiente.
        
        Args:
            from_user: Teléfono del usuario
            numero_seleccion: Número seleccionado (ej: "1", "1.1", "2.3")
        
        Returns:
            String con el mensaje de respuesta
        """
        
        print(f"\n{'─'*60}")
        print(f"PROCESANDO SELECCIÓN: {numero_seleccion}")
        print(f"{'─'*60}")
        
        # Si es opción principal (un solo dígito)
        if '.' not in numero_seleccion:
            # Mostrar submenú
            return self.generar_mensaje_submenu(numero_seleccion)
        
        # Es una subopción (ej: "1.1")
        submenu = self.obtener_submenu(numero_seleccion)
        
        if not submenu:
            return "❌ Opción no válida. Por favor intenta de nuevo."
        
        if not submenu.get('activo', True):
            return "⚠️ Esta opción no está disponible actualmente."
        
        print(f"→ Opción seleccionada: {submenu['nombre']}")
        print(f"   Handler: {submenu.get('handler', 'N/A')}")
        print(f"   Grupo: {submenu.get('grupo_id', 'N/A')}")
        
        # Verificar si tiene handler
        handler_codigo = submenu.get('handler')
        
        if not handler_codigo:
            return "⚠️ Esta opción no tiene handler configurado."
        
        # Determinar grupo final
        grupo_final = self._determinar_grupo_final(
            handler_codigo,
            submenu.get('grupo_id')
        )
        
        print(f"   Grupo final: {grupo_final}")
        
        # Cargar y ejecutar handler
        try:
            handler = self._cargar_handler_dinamico(handler_codigo)
            
            resultado = handler.ejecutar(
                from_user=from_user,
                mensaje="",  # Por ahora vacío, handlers harán preguntas
                grupo_id=grupo_final
            )
            
            return resultado
            
        except Exception as e:
            print(f"❌ Error ejecutando handler: {e}")
            return self.config_menu.configuracion_general.get(
                'mensaje_error',
                'Lo siento, hubo un error. Por favor intenta de nuevo.'
            )
    
    
    def _determinar_grupo_final(
        self,
        codigo_handler: str,
        grupo_submenu: Optional[str]
    ) -> Optional[str]:
        """
        Determina qué grupo usar según configuración del handler.
        
        Args:
            codigo_handler: Código del handler (ej: "A001")
            grupo_submenu: GUID del grupo en el submenú (del JSON de Dataverse)
        
        Returns:
            GUID del grupo final a usar o None
        """
        
        # Si no hay config del handler, usar grupo del submenú
        if codigo_handler not in self.config_handlers:
            return grupo_submenu
        
        config = self.config_handlers[codigo_handler]
        
        # 1. Si hay grupo_override, usarlo (ignora grupo del submenú)
        if config.grupo_override:
            return config.grupo_override
        
        # 2. Si usa_grupo_de_dataverse es True, usar grupo del submenú
        if config.usa_grupo_de_dataverse:
            return grupo_submenu
        
        # 3. No usar grupo
        return None
    
    
    def _cargar_handler_dinamico(self, codigo: str):
        """
        Carga dinámicamente un handler según su código.
        
        Args:
            codigo: Código del handler (ej: "A001")
        
        Returns:
            Instancia del handler
        """
        
        print(f"\n→ Cargando handler: {codigo}")
        
        # Buscar en configuración
        if codigo not in self.config_handlers:
            raise Exception(f"Handler {codigo} no encontrado en config_handlers.json")
        
        config = self.config_handlers[codigo]
        
        # Verificar que esté activo
        if not config.activo:
            raise Exception(f"Handler {codigo} está desactivado")
        
        # Obtener nombre de archivo y clase
        nombre_archivo = config.archivo.replace('.py', '')
        nombre_clase = config.clase
        
        print(f"  → Archivo: {nombre_archivo}")
        print(f"  → Clase: {nombre_clase}")
        
        # Importar módulo dinámicamente
        try:
            modulo_path = f"handlers.{nombre_archivo}"
            
            if modulo_path in sys.modules:
                modulo = importlib.reload(sys.modules[modulo_path])
            else:
                modulo = importlib.import_module(modulo_path)
            
            # Obtener clase
            clase_handler = getattr(modulo, nombre_clase)
            
            # Instanciar
            instancia = clase_handler(
                dataverse_url=DATAVERSE_URL,
                headers=self.headers
            )
            
            print(f"  ✓ Handler cargado exitosamente")
            
            return instancia
            
        except Exception as e:
            raise Exception(f"Error cargando handler {codigo}: {e}")


# ============================================================================
# FUNCIÓN PRINCIPAL (PARA TESTING)
# ============================================================================

def main():
    """Función principal para testing"""
    
    try:
        # Inicializar sistema
        sistema = SistemaMenuJSON()
        
        print(f"\n{'='*60}")
        print("SIMULACIÓN DE FLUJO")
        print(f"{'='*60}\n")
        
        # 1. Mostrar bienvenida
        print("📱 WhatsApp: Usuario conecta")
        print("─" * 60)
        mensaje = sistema.generar_mensaje_bienvenida()
        print(mensaje)
        print()
        
        # 2. Mostrar menú principal
        mensaje = sistema.generar_mensaje_menu_principal()
        print(mensaje)
        print()
        
        # 3. Usuario selecciona "1"
        print("👤 Usuario: 1")
        print("─" * 60)
        mensaje = sistema.procesar_seleccion("573001234567", "1")
        print(mensaje)
        print()
        
        # 4. Usuario selecciona "1.1"
        print("👤 Usuario: 1.1")
        print("─" * 60)
        mensaje = sistema.procesar_seleccion("573001234567", "1.1")
        print(mensaje)
        print()
        
        print("✓ Simulación completada")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
