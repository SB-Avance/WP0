"""
SISTEMA DE MENÚ JERÁRQUICO CON SUBMENÚS
========================================

Sistema de menú de WhatsApp con:
✅ Menú principal con 3 opciones numeradas
✅ Cada opción tiene submenú propio
✅ Asignación a grupos diferentes por submenú
✅ Navegación intuitiva

Estructura:
1. Solicitud Ticket
   1.1 Soporte Técnico → Grupo "Soporte Técnico"
   1.2 Garantías → Grupo "Garantías"
   1.3 Consultas Generales → Grupo "Consultas"

2. Ventas
   2.1 Cotización → Grupo "Ventas - Cotización"
   2.2 Catálogo → Grupo "Ventas - Catálogo"
   2.3 Seguimiento → Grupo "Ventas - Seguimiento"

3. Solicitar Atención
   3.1 Agente Disponible → Grupo "Atención Inmediata"
   3.2 Agendar Cita → Grupo "Agendamiento"

Autor: Sistema CRM WhatsApp
Fecha: Febrero 2026
"""
import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# CONFIGURACIÓN
# ============================================================================

class MenuConfig:
    """Configuración del sistema de menú jerárquico"""
    CACHE_DURATION_MINUTES = 5
    MENSAJE_BIENVENIDA = "¡Bienvenido! Seleccione una opción:"
    MENSAJE_SELECCION_INVALIDA = "Opción inválida. Por favor escriba MENU para ver las opciones."
    MENSAJE_ERROR = "Lo sentimos, ocurrió un error. Escriba MENU para intentar nuevamente."
    SHOW_LOGS = True


# ============================================================================
# MODELOS DE DATOS
# ============================================================================

@dataclass
class SubOpcion:
    """Representa una sub-opción del menú"""
    numero: str  # Ej: "1.1", "1.2", "2.1"
    texto: str
    grupo_asignado: str
    categoria_padre: str
    metadata: Optional[Dict] = None
    
    def __str__(self) -> str:
        return f"{self.numero}. {self.texto}"


@dataclass
class OpcionPrincipal:
    """Representa una opción principal del menú"""
    numero: int  # 1, 2, 3
    texto: str
    subopciones: List[SubOpcion]
    
    def __str__(self) -> str:
        return f"{self.numero}. {self.texto}"
    
    def tiene_subopciones(self) -> bool:
        return len(self.subopciones) > 0
    
    def get_subopcion_por_numero(self, numero_completo: str) -> Optional[SubOpcion]:
        """
        Obtiene una subopción por número completo (ej: "1.1", "2.3")
        """
        for sub in self.subopciones:
            if sub.numero == numero_completo:
                return sub
        return None


@dataclass
class EstadoUsuario:
    """Representa el estado de navegación del usuario en el menú"""
    telefono: str
    en_submenu: bool = False
    opcion_principal_seleccionada: Optional[int] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def reset(self):
        """Reinicia el estado del usuario"""
        self.en_submenu = False
        self.opcion_principal_seleccionada = None
        self.timestamp = datetime.now()
    
    def is_expired(self, timeout_minutes: int = 5) -> bool:
        """Verifica si el estado ha expirado"""
        expiration = self.timestamp + timedelta(minutes=timeout_minutes)
        return datetime.now() >= expiration


# ============================================================================
# SISTEMA DE MENÚ JERÁRQUICO
# ============================================================================

class SistemaMenuJerarquico:
    """
    Gestiona menú de WhatsApp con estructura jerárquica:
    - Menú principal (1, 2, 3)
    - Submenús por cada opción principal
    - Asignación automática a grupos
    """
    
    def __init__(self, dataverse_url: str, token_provider_func):
        """
        Inicializa el sistema de menú jerárquico
        
        Args:
            dataverse_url: URL base de Dataverse
            token_provider_func: Función que retorna el access token
        """
        self.dataverse_url = dataverse_url
        self.get_token = token_provider_func
        self._cache_opciones: Optional[List[OpcionPrincipal]] = None
        self._cache_timestamp: Optional[datetime] = None
        self._estados_usuarios: Dict[str, EstadoUsuario] = {}
        self._log_prefix = "[MENU_JERARQUICO]"
    
    # ------------------------------------------------------------------------
    # MÉTODOS PÚBLICOS - OBTENER MENÚS
    # ------------------------------------------------------------------------
    
    def obtener_menu_principal_texto(self) -> str:
        """
        Obtiene el texto del menú principal
        
        Returns:
            String con el menú principal numerado (1, 2, 3)
        """
        opciones = self.obtener_opciones_principales()
        
        if not opciones:
            self._log("⚠️  No hay opciones principales disponibles")
            return MenuConfig.MENSAJE_ERROR
        
        partes = [MenuConfig.MENSAJE_BIENVENIDA, ""]
        
        for opcion in opciones:
            partes.append(str(opcion))
        
        menu_texto = "\n".join(partes)
        self._log(f"✅ Menú principal generado con {len(opciones)} opciones")
        
        return menu_texto
    
    def obtener_submenu_texto(self, numero_opcion_principal: int) -> str:
        """
        Obtiene el texto del submenú de una opción principal
        
        Args:
            numero_opcion_principal: Número de la opción principal (1, 2, 3)
            
        Returns:
            String con el submenú numerado
        """
        opcion = self.obtener_opcion_principal(numero_opcion_principal)
        
        if not opcion:
            self._log(f"⚠️  Opción principal {numero_opcion_principal} no encontrada")
            return MenuConfig.MENSAJE_SELECCION_INVALIDA
        
        if not opcion.tiene_subopciones():
            self._log(f"⚠️  Opción '{opcion.texto}' no tiene subopciones")
            return f"La opción '{opcion.texto}' no tiene subopciones disponibles."
        
        partes = [
            f"📋 {opcion.texto}",
            "",
            "Seleccione una opción:",
            ""
        ]
        
        for subopcion in opcion.subopciones:
            partes.append(str(subopcion))
        
        partes.append("")
        partes.append("Escriba 0 para volver al menú principal")
        
        menu_texto = "\n".join(partes)
        self._log(f"✅ Submenú generado para '{opcion.texto}' con {len(opcion.subopciones)} opciones")
        
        return menu_texto
    
    # ------------------------------------------------------------------------
    # MÉTODOS PÚBLICOS - PROCESAMIENTO DE MENSAJES
    # ------------------------------------------------------------------------
    
    def procesar_mensaje(self, mensaje: str, telefono: str) -> Dict:
        """
        Procesa un mensaje del usuario y retorna la respuesta apropiada
        
        Args:
            mensaje: Texto del mensaje del usuario
            telefono: Número de teléfono del usuario
            
        Returns:
            Dict con la respuesta a enviar y metadata
        """
        mensaje_clean = mensaje.strip().lower()
        
        # Comando: MENU - Mostrar menú principal
        if mensaje_clean in ["menu", "menú", "inicio", "hola", "hi"]:
            self._resetear_estado_usuario(telefono)
            return {
                "tipo": "menu_principal",
                "texto": self.obtener_menu_principal_texto(),
                "grupo": None
            }
        
        # Obtener estado del usuario
        estado = self._obtener_estado_usuario(telefono)
        
        # Si el estado expiró, resetear
        if estado.is_expired():
            self._log(f"⏰ Estado expirado para {telefono}, reseteando")
            estado.reset()
        
        # Comando: 0 - Volver al menú principal (solo si está en submenú)
        if mensaje_clean == "0" and estado.en_submenu:
            estado.reset()
            return {
                "tipo": "menu_principal",
                "texto": self.obtener_menu_principal_texto(),
                "grupo": None
            }
        
        # CASO 1: Usuario NO está en submenú -> Selección de menú principal
        if not estado.en_submenu:
            return self._procesar_seleccion_principal(mensaje, telefono, estado)
        
        # CASO 2: Usuario SÍ está en submenú -> Selección de subopción
        else:
            return self._procesar_seleccion_submenu(mensaje, telefono, estado)
    
    # ------------------------------------------------------------------------
    # MÉTODOS PÚBLICOS - OBTENER DATOS
    # ------------------------------------------------------------------------
    
    def obtener_opciones_principales(self, forzar_refresh: bool = False) -> List[OpcionPrincipal]:
        """
        Obtiene las opciones principales del menú
        
        Args:
            forzar_refresh: Si True, ignora el cache
            
        Returns:
            Lista de opciones principales
        """
        # Verificar cache
        if not forzar_refresh and self._es_cache_valido():
            edad = (datetime.now() - self._cache_timestamp).total_seconds()
            self._log(f"✅ Usando cache (edad: {edad:.1f}s)")
            return self._cache_opciones
        
        # Cargar desde Dataverse
        self._log("🔄 Consultando Dataverse...")
        opciones = self._cargar_desde_dataverse()
        
        # Actualizar cache
        self._cache_opciones = opciones
        self._cache_timestamp = datetime.now()
        self._log(f"✅ Cache actualizado con {len(opciones)} opciones principales")
        
        return opciones
    
    def obtener_opcion_principal(self, numero: int) -> Optional[OpcionPrincipal]:
        """
        Obtiene una opción principal por número
        
        Args:
            numero: Número de la opción (1, 2, 3)
            
        Returns:
            OpcionPrincipal o None
        """
        opciones = self.obtener_opciones_principales()
        
        for opcion in opciones:
            if opcion.numero == numero:
                return opcion
        
        return None
    
    def invalidar_cache(self):
        """Invalida el cache para forzar actualización"""
        self._cache_opciones = None
        self._cache_timestamp = None
        self._log("🗑️  Cache invalidado")
    
    # ------------------------------------------------------------------------
    # MÉTODOS PRIVADOS - PROCESAMIENTO
    # ------------------------------------------------------------------------
    
    def _procesar_seleccion_principal(self, mensaje: str, telefono: str, estado: EstadoUsuario) -> Dict:
        """Procesa la selección de una opción del menú principal"""
        numero = self._extraer_numero(mensaje)
        
        if numero is None or numero < 1:
            return {
                "tipo": "invalido",
                "texto": MenuConfig.MENSAJE_SELECCION_INVALIDA,
                "grupo": None
            }
        
        opcion = self.obtener_opcion_principal(numero)
        
        if not opcion:
            return {
                "tipo": "invalido",
                "texto": MenuConfig.MENSAJE_SELECCION_INVALIDA,
                "grupo": None
            }
        
        # Si la opción no tiene subopciones, es una selección final
        if not opcion.tiene_subopciones():
            self._log(f"✅ Selección directa: {opcion.texto}")
            estado.reset()
            return {
                "tipo": "seleccion_final_sin_submenu",
                "texto": f"Ha seleccionado: {opcion.texto}\n\nUn agente se comunicará con usted pronto.",
                "grupo": opcion.texto,  # Usar el nombre de la opción como grupo
                "opcion_principal": opcion.texto
            }
        
        # La opción tiene subopciones, mostrar submenú
        self._log(f"✅ Mostrando submenú de: {opcion.texto}")
        estado.en_submenu = True
        estado.opcion_principal_seleccionada = numero
        estado.timestamp = datetime.now()
        
        return {
            "tipo": "submenu",
            "texto": self.obtener_submenu_texto(numero),
            "grupo": None,
            "opcion_principal": opcion.texto
        }
    
    def _procesar_seleccion_submenu(self, mensaje: str, telefono: str, estado: EstadoUsuario) -> Dict:
        """Procesa la selección de una subopción"""
        # Obtener la opción principal actual
        opcion_principal = self.obtener_opcion_principal(estado.opcion_principal_seleccionada)
        
        if not opcion_principal:
            self._log(f"❌ Error: opción principal {estado.opcion_principal_seleccionada} no encontrada")
            estado.reset()
            return {
                "tipo": "error",
                "texto": MenuConfig.MENSAJE_ERROR,
                "grupo": None
            }
        
        # Extraer número de la subopción
        numero = self._extraer_numero(mensaje)
        
        if numero is None or numero < 1:
            return {
                "tipo": "invalido",
                "texto": MenuConfig.MENSAJE_SELECCION_INVALIDA,
                "grupo": None
            }
        
        # Buscar la subopción por índice (1-based)
        if numero > len(opcion_principal.subopciones):
            return {
                "tipo": "invalido",
                "texto": MenuConfig.MENSAJE_SELECCION_INVALIDA,
                "grupo": None
            }
        
        subopcion = opcion_principal.subopciones[numero - 1]
        
        self._log(f"✅ Selección final: {subopcion.texto} → Grupo: {subopcion.grupo_asignado}")
        
        # Resetear estado
        estado.reset()
        
        return {
            "tipo": "seleccion_final",
            "texto": f"Ha seleccionado: {subopcion.texto}\n\nUn agente del área de {subopcion.grupo_asignado} se comunicará con usted pronto.",
            "grupo": subopcion.grupo_asignado,
            "opcion_principal": opcion_principal.texto,
            "subopcion": subopcion.texto,
            "numero_completo": subopcion.numero
        }
    
    # ------------------------------------------------------------------------
    # MÉTODOS PRIVADOS - GESTIÓN DE ESTADO
    # ------------------------------------------------------------------------
    
    def _obtener_estado_usuario(self, telefono: str) -> EstadoUsuario:
        """Obtiene o crea el estado de un usuario"""
        if telefono not in self._estados_usuarios:
            self._estados_usuarios[telefono] = EstadoUsuario(telefono=telefono)
        return self._estados_usuarios[telefono]
    
    def _resetear_estado_usuario(self, telefono: str):
        """Resetea el estado de un usuario"""
        if telefono in self._estados_usuarios:
            self._estados_usuarios[telefono].reset()
        else:
            self._estados_usuarios[telefono] = EstadoUsuario(telefono=telefono)
    
    # ------------------------------------------------------------------------
    # MÉTODOS PRIVADOS - CARGA DE DATOS
    # ------------------------------------------------------------------------
    
    def _cargar_desde_dataverse(self) -> List[OpcionPrincipal]:
        """
        Carga el menú jerárquico desde Dataverse
        
        Estructura esperada en cr321_chatbots:
        - cr321_name: Nombre de la categoría principal
        - cr321_orden: Orden (1, 2, 3)
        - cr321_elemento1-5: Subopciones
        - cr321_grupo1-5: Grupos asignados a cada subopción
        """
        token = self.get_token()
        if not token:
            self._log("❌ Error al obtener token")
            return self._obtener_menu_hardcoded()
        
        url = f"{self.dataverse_url}/api/data/v9.2/cr321_chatbots"
        url += "?$select=cr321_chatbotid,cr321_name,cr321_orden"
        url += ",cr321_elemento1,cr321_elemento2,cr321_elemento3,cr321_elemento4,cr321_elemento5"
        url += ",cr321_grupo1,cr321_grupo2,cr321_grupo3,cr321_grupo4,cr321_grupo5"
        url += "&$filter=cr321_active eq true"
        url += "&$orderby=cr321_orden asc,cr321_name asc"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                self._log(f"❌ Error HTTP {response.status_code}")
                return self._obtener_menu_hardcoded()
            
            data = response.json()
            chatbots = data.get("value", [])
            
            if not chatbots:
                self._log("⚠️  No hay chatbots activos, usando menú hardcoded")
                return self._obtener_menu_hardcoded()
            
            self._log(f"📥 Obtenidos {len(chatbots)} chatbots de Dataverse")
            
            opciones = self._procesar_chatbots(chatbots)
            
            if not opciones:
                self._log("⚠️  No se pudieron procesar chatbots, usando menú hardcoded")
                return self._obtener_menu_hardcoded()
            
            return opciones
            
        except Exception as e:
            self._log(f"❌ Excepción: {e}")
            return self._obtener_menu_hardcoded()
    
    def _procesar_chatbots(self, chatbots: List[Dict]) -> List[OpcionPrincipal]:
        """Procesa chatbots y genera estructura jerárquica"""
        opciones = []
        
        for idx, chatbot in enumerate(chatbots[:3], 1):  # Máximo 3 opciones principales
            nombre = chatbot.get("cr321_name", "").strip()
            orden = chatbot.get("cr321_orden", idx)
            
            if not nombre:
                continue
            
            # Extraer subopciones
            subopciones = []
            for i in range(1, 6):  # Máximo 5 subopciones
                elemento = chatbot.get(f"cr321_elemento{i}", "")
                grupo = chatbot.get(f"cr321_grupo{i}", "")
                
                if elemento and elemento.strip():
                    sub = SubOpcion(
                        numero=f"{orden}.{i}",
                        texto=elemento.strip(),
                        grupo_asignado=grupo.strip() if grupo else elemento.strip(),
                        categoria_padre=nombre,
                        metadata={"chatbot_id": chatbot.get("cr321_chatbotid")}
                    )
                    subopciones.append(sub)
            
            if subopciones:  # Solo agregar si tiene subopciones
                opcion = OpcionPrincipal(
                    numero=orden,
                    texto=nombre,
                    subopciones=subopciones
                )
                opciones.append(opcion)
        
        # Ordenar por número
        opciones.sort(key=lambda x: x.numero)
        
        self._log(f"✅ Procesadas {len(opciones)} opciones principales")
        
        return opciones
    
    def _obtener_menu_hardcoded(self) -> List[OpcionPrincipal]:
        """
        Retorna menú hardcoded como fallback
        """
        self._log("📋 Usando menú hardcoded")
        
        return [
            OpcionPrincipal(
                numero=1,
                texto="Solicitud Ticket",
                subopciones=[
                    SubOpcion("1.1", "Soporte Técnico", "Soporte Técnico", "Solicitud Ticket"),
                    SubOpcion("1.2", "Garantías", "Garantías", "Solicitud Ticket"),
                    SubOpcion("1.3", "Consultas Generales", "Consultas", "Solicitud Ticket"),
                ]
            ),
            OpcionPrincipal(
                numero=2,
                texto="Ventas",
                subopciones=[
                    SubOpcion("2.1", "Cotización", "Ventas - Cotización", "Ventas"),
                    SubOpcion("2.2", "Catálogo", "Ventas - Catálogo", "Ventas"),
                    SubOpcion("2.3", "Seguimiento", "Ventas - Seguimiento", "Ventas"),
                ]
            ),
            OpcionPrincipal(
                numero=3,
                texto="Solicitar Atención",
                subopciones=[
                    SubOpcion("3.1", "Agente Disponible", "Atención Inmediata", "Solicitar Atención"),
                    SubOpcion("3.2", "Agendar Cita", "Agendamiento", "Solicitar Atención"),
                ]
            ),
        ]
    
    # ------------------------------------------------------------------------
    # MÉTODOS PRIVADOS - UTILIDADES
    # ------------------------------------------------------------------------
    
    def _es_cache_valido(self) -> bool:
        """Verifica si el cache es válido"""
        if self._cache_opciones is None or self._cache_timestamp is None:
            return False
        
        expiracion = self._cache_timestamp + timedelta(minutes=MenuConfig.CACHE_DURATION_MINUTES)
        return datetime.now() < expiracion
    
    def _extraer_numero(self, texto: str) -> Optional[int]:
        """Extrae el primer número del texto"""
        import re
        match = re.search(r'\d+', texto)
        if match:
            try:
                return int(match.group())
            except ValueError:
                return None
        return None
    
    def _log(self, mensaje: str):
        """Registra un log"""
        if MenuConfig.SHOW_LOGS:
            print(f"{self._log_prefix} {mensaje}")


# ============================================================================
# FUNCIÓN FACTORY
# ============================================================================

def crear_sistema_menu_jerarquico(dataverse_url: str, token_provider_func) -> SistemaMenuJerarquico:
    """
    Crea una instancia del sistema de menú jerárquico
    
    Args:
        dataverse_url: URL de Dataverse
        token_provider_func: Función que retorna access token
        
    Returns:
        Instancia de SistemaMenuJerarquico
    """
    return SistemaMenuJerarquico(dataverse_url, token_provider_func)


# ============================================================================
# DEMO
# ============================================================================

if __name__ == "__main__":
    """Demo del sistema de menú jerárquico"""
    import sys
    sys.path.append('backend')
    
    try:
        from goot import DATAVERSE_URL, CLIENT_ID, CLIENT_SECRET, TENANT_ID
        
        def get_token():
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
        
        print("="*80)
        print("SISTEMA DE MENÚ JERÁRQUICO - DEMO")
        print("="*80)
        
        sistema = crear_sistema_menu_jerarquico(DATAVERSE_URL, get_token)
        telefono_prueba = "573001234567"
        
        # Simular conversación
        conversacion = [
            "menu",      # Pedir menú
            "1",         # Seleccionar Solicitud Ticket
            "2",         # Seleccionar Garantías (subopción 2)
            "menu",      # Volver al menú
            "2",         # Seleccionar Ventas
            "1",         # Seleccionar Cotización
        ]
        
        print("\n📱 SIMULANDO CONVERSACIÓN:\n")
        
        for mensaje in conversacion:
            print(f"\n👤 Usuario: {mensaje}")
            respuesta = sistema.procesar_mensaje(mensaje, telefono_prueba)
            print(f"🤖 Bot [{respuesta['tipo']}]:")
            print("-" * 70)
            print(respuesta['texto'])
            if respuesta['grupo']:
                print(f"\n✅ Asignado al grupo: {respuesta['grupo']}")
            print("-" * 70)
        
        print("\n✅ Demo completada")
        
    except ImportError:
        print("❌ Error: No se pudo importar desde backend/goot.py")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
