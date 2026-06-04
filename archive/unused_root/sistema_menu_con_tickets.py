"""
SISTEMA DE MENÚ JERÁRQUICO CON CAPTURA DE TICKETS
==================================================

Extensión del sistema de menú que incluye:
✅ Captura de datos antes de asignar a grupo
✅ Creación automática de tickets en Dataverse
✅ Preguntas configurables por categoría
✅ Flujo inteligente de conversación

Flujo para "Solicitud Ticket":
1. Usuario selecciona "1" (Solicitud Ticket)
2. Usuario selecciona "1" (Incidente Técnico)
3. Sistema pregunta: "¿Cuál es el problema que presenta?"
4. Usuario responde: "No puedo acceder al sistema"
5. Sistema pregunta: "¿Desde cuándo presenta este problema?"
6. Usuario responde: "Desde esta mañana"
7. Sistema crea ticket con esos datos
8. Sistema asigna conversación al grupo correspondiente

Autor: Sistema CRM WhatsApp
Fecha: Febrero 2026
"""

import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Tuple

import requests

# ============================================================================
# CONFIGURACIÓN
# ============================================================================


class MenuConfig:
    """Configuración del sistema de menú jerárquico"""

    CACHE_DURATION_MINUTES = 5
    MENSAJE_BIENVENIDA = "¡Bienvenido! Seleccione una opción:"
    MENSAJE_SELECCION_INVALIDA = (
        "Opción inválida. Por favor escriba MENU para ver las opciones."
    )
    MENSAJE_ERROR = (
        "Lo sentimos, ocurrió un error. Escriba MENU para intentar nuevamente."
    )
    SHOW_LOGS = True

    # Configuración de captura de datos
    CATEGORIAS_CON_CAPTURA = ["Solicitud Ticket"]  # Categorías que requieren captura

    # Preguntas por categoría
    PREGUNTAS_POR_CATEGORIA = {
        "Solicitud Ticket": [
            "¿Cuál es el problema o solicitud que desea reportar?",
            "¿Desde cuándo presenta esta situación?",
        ]
    }

    MENSAJE_DATOS_CAPTURADOS = """
✅ Información registrada correctamente.

Resumen de su ticket:
- {subopcion}
- Descripción: {respuesta1}
- Fecha inicio: {respuesta2}

Un agente del área de {grupo} se comunicará con usted pronto.
Número de ticket: #{ticket_id}
"""


# ============================================================================
# MODELOS DE DATOS
# ============================================================================


class EstadoCaptura(Enum):
    """Estados posibles durante la captura de datos"""

    NO_CAPTURANDO = "no_capturando"
    PREGUNTA_1 = "pregunta_1"
    PREGUNTA_2 = "pregunta_2"
    COMPLETADO = "completado"


@dataclass
class DatosCaptura:
    """Datos capturados del usuario"""

    categoria: str
    subopcion: str
    grupo_destino: str
    respuestas: List[str] = field(default_factory=list)
    estado: EstadoCaptura = EstadoCaptura.NO_CAPTURANDO
    pregunta_actual: int = 0
    timestamp_inicio: datetime = None

    def __post_init__(self):
        if self.timestamp_inicio is None:
            self.timestamp_inicio = datetime.now()

    def get_pregunta_actual(self) -> Optional[str]:
        """Obtiene la pregunta actual según el estado"""
        preguntas = MenuConfig.PREGUNTAS_POR_CATEGORIA.get(self.categoria, [])
        if 0 <= self.pregunta_actual < len(preguntas):
            return preguntas[self.pregunta_actual]
        return None

    def agregar_respuesta(self, respuesta: str) -> bool:
        """
        Agrega una respuesta y avanza al siguiente estado
        Returns: True si hay más preguntas, False si terminó
        """
        self.respuestas.append(respuesta)
        self.pregunta_actual += 1

        preguntas = MenuConfig.PREGUNTAS_POR_CATEGORIA.get(self.categoria, [])

        if self.pregunta_actual >= len(preguntas):
            self.estado = EstadoCaptura.COMPLETADO
            return False  # No hay más preguntas
        else:
            if self.pregunta_actual == 0:
                self.estado = EstadoCaptura.PREGUNTA_1
            elif self.pregunta_actual == 1:
                self.estado = EstadoCaptura.PREGUNTA_2
            return True  # Hay más preguntas

    def reset(self):
        """Reinicia la captura"""
        self.respuestas = []
        self.estado = EstadoCaptura.NO_CAPTURANDO
        self.pregunta_actual = 0
        self.timestamp_inicio = datetime.now()


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

    def requiere_captura_datos(self) -> bool:
        """Verifica si esta categoría requiere captura de datos"""
        return self.texto in MenuConfig.CATEGORIAS_CON_CAPTURA


@dataclass
class EstadoUsuario:
    """Representa el estado de navegación del usuario en el menú"""

    telefono: str
    en_submenu: bool = False
    opcion_principal_seleccionada: Optional[int] = None
    timestamp: datetime = None

    # Nuevo: Captura de datos
    capturando_datos: bool = False
    datos_captura: Optional[DatosCaptura] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

    def reset(self):
        """Reinicia el estado del usuario"""
        self.en_submenu = False
        self.opcion_principal_seleccionada = None
        self.capturando_datos = False
        self.datos_captura = None
        self.timestamp = datetime.now()

    def iniciar_captura(self, categoria: str, subopcion: str, grupo: str):
        """Inicia el proceso de captura de datos"""
        self.capturando_datos = True
        self.datos_captura = DatosCaptura(
            categoria=categoria, subopcion=subopcion, grupo_destino=grupo
        )
        self.datos_captura.estado = EstadoCaptura.PREGUNTA_1

    def is_expired(self, timeout_minutes: int = 5) -> bool:
        """Verifica si el estado ha expirado"""
        expiration = self.timestamp + timedelta(minutes=timeout_minutes)
        return datetime.now() >= expiration


# ============================================================================
# SISTEMA DE MENÚ CON TICKETS
# ============================================================================


class SistemaMenuConTickets:
    """
    Sistema de menú jerárquico con captura de datos y creación de tickets
    """

    def __init__(self, dataverse_url: str, token_provider_func):
        """
        Inicializa el sistema

        Args:
            dataverse_url: URL base de Dataverse
            token_provider_func: Función que retorna el access token
        """
        self.dataverse_url = dataverse_url
        self.get_token = token_provider_func
        self._cache_opciones: Optional[List[OpcionPrincipal]] = None
        self._cache_timestamp: Optional[datetime] = None
        self._estados_usuarios: Dict[str, EstadoUsuario] = {}
        self._log_prefix = "[MENU_CON_TICKETS]"

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
        mensaje_clean = mensaje.strip()
        mensaje_lower = mensaje_clean.lower()

        # Comando: MENU - Mostrar menú principal
        if mensaje_lower in ["menu", "menú", "inicio", "hola", "hi"]:
            self._resetear_estado_usuario(telefono)
            return {
                "tipo": "menu_principal",
                "texto": self.obtener_menu_principal_texto(),
                "grupo": None,
            }

        # Obtener estado del usuario
        estado = self._obtener_estado_usuario(telefono)

        # Si el estado expiró, resetear
        if estado.is_expired():
            self._log(f"⏰ Estado expirado para {telefono}, reseteando")
            estado.reset()

        # CASO ESPECIAL: Usuario está capturando datos
        if estado.capturando_datos and estado.datos_captura:
            return self._procesar_respuesta_captura(mensaje_clean, telefono, estado)

        # Comando: 0 - Volver al menú principal (solo si está en submenú)
        if mensaje_lower == "0" and estado.en_submenu:
            estado.reset()
            return {
                "tipo": "menu_principal",
                "texto": self.obtener_menu_principal_texto(),
                "grupo": None,
            }

        # CASO 1: Usuario NO está en submenú -> Selección de menú principal
        if not estado.en_submenu:
            return self._procesar_seleccion_principal(mensaje_clean, telefono, estado)

        # CASO 2: Usuario SÍ está en submenú -> Selección de subopción
        else:
            return self._procesar_seleccion_submenu(mensaje_clean, telefono, estado)

    # ------------------------------------------------------------------------
    # MÉTODOS PRIVADOS - PROCESAMIENTO DE CAPTURA
    # ------------------------------------------------------------------------

    def _procesar_respuesta_captura(
        self, respuesta: str, telefono: str, estado: EstadoUsuario
    ) -> Dict:
        """Procesa una respuesta durante la captura de datos"""
        datos = estado.datos_captura

        # Agregar respuesta
        hay_mas_preguntas = datos.agregar_respuesta(respuesta)

        if hay_mas_preguntas:
            # Hay más preguntas, continuar capturando
            siguiente_pregunta = datos.get_pregunta_actual()
            self._log(
                f"❓ Capturando respuesta {len(datos.respuestas)} para {telefono}"
            )

            return {
                "tipo": "captura_en_progreso",
                "texto": siguiente_pregunta,
                "grupo": None,
            }
        else:
            # Captura completada, crear ticket y asignar
            self._log(f"✅ Captura completada para {telefono}, creando ticket")

            ticket_id = self._crear_ticket_en_dataverse(datos, telefono)

            # Construir mensaje de confirmación
            mensaje_confirmacion = MenuConfig.MENSAJE_DATOS_CAPTURADOS.format(
                subopcion=datos.subopcion,
                respuesta1=datos.respuestas[0] if len(datos.respuestas) > 0 else "-",
                respuesta2=datos.respuestas[1] if len(datos.respuestas) > 1 else "-",
                grupo=datos.grupo_destino,
                ticket_id=ticket_id or "PENDIENTE",
            )

            # Resetear estado
            grupo_asignar = datos.grupo_destino
            estado.reset()

            return {
                "tipo": "ticket_creado",
                "texto": mensaje_confirmacion,
                "grupo": grupo_asignar,
                "ticket_id": ticket_id,
                "respuestas": datos.respuestas,
            }

    def _crear_ticket_en_dataverse(
        self, datos: DatosCaptura, telefono: str
    ) -> Optional[str]:
        """
        Crea un ticket en la tabla cr321_tickets de Dataverse

        Args:
            datos: Datos capturados
            telefono: Teléfono del usuario

        Returns:
            ID del ticket creado o None si falla
        """
        token = self.get_token()
        if not token:
            self._log("❌ Error al obtener token para crear ticket")
            return None

        # Construir datos del ticket
        ticket_data = {
            "cr321_name": f"Ticket - {datos.subopcion}",
            "cr321_telefono": telefono,
            "cr321_categoria": datos.categoria,
            "cr321_subcategoria": datos.subopcion,
            "cr321_grupo_asignado": datos.grupo_destino,
            "cr321_estado": "Nuevo",
            "cr321_prioridad": "Media",
            "cr321_fecha_creacion": datetime.now().isoformat(),
        }

        # Agregar respuestas
        if len(datos.respuestas) > 0:
            ticket_data["cr321_descripcion"] = datos.respuestas[0]
        if len(datos.respuestas) > 1:
            ticket_data["cr321_fecha_inicio_problema"] = datos.respuestas[1]

        # Crear ticket
        url = f"{self.dataverse_url}/api/data/v9.2/cr321_tickets"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        try:
            response = requests.post(url, headers=headers, json=ticket_data, timeout=10)

            if response.status_code in [200, 201, 204]:
                # Extraer ID del ticket creado
                ticket_id = response.headers.get("OData-EntityId", "")
                if ticket_id:
                    # Formato: https://.../cr321_tickets(GUID)
                    ticket_id = ticket_id.split("(")[-1].rstrip(")")
                    self._log(f"✅ Ticket creado: {ticket_id}")
                    return ticket_id
                else:
                    self._log("⚠️  Ticket creado pero sin ID en respuesta")
                    return "CREADO"
            else:
                self._log(f"❌ Error al crear ticket: HTTP {response.status_code}")
                self._log(f"   Respuesta: {response.text}")
                return None

        except Exception as e:
            self._log(f"❌ Excepción al crear ticket: {e}")
            return None

    # ------------------------------------------------------------------------
    # MÉTODOS PRIVADOS - PROCESAMIENTO DE SELECCIÓN
    # ------------------------------------------------------------------------

    def _procesar_seleccion_submenu(
        self, mensaje: str, telefono: str, estado: EstadoUsuario
    ) -> Dict:
        """Procesa la selección de una subopción"""
        # Obtener la opción principal actual
        opcion_principal = self.obtener_opcion_principal(
            estado.opcion_principal_seleccionada
        )

        if not opcion_principal:
            self._log(
                f"❌ Error: opción principal {estado.opcion_principal_seleccionada} no encontrada"
            )
            estado.reset()
            return {"tipo": "error", "texto": MenuConfig.MENSAJE_ERROR, "grupo": None}

        # Extraer número de la subopción
        numero = self._extraer_numero(mensaje)

        if numero is None or numero < 1:
            return {
                "tipo": "invalido",
                "texto": MenuConfig.MENSAJE_SELECCION_INVALIDA,
                "grupo": None,
            }

        # Buscar la subopción por índice (1-based)
        if numero > len(opcion_principal.subopciones):
            return {
                "tipo": "invalido",
                "texto": MenuConfig.MENSAJE_SELECCION_INVALIDA,
                "grupo": None,
            }

        subopcion = opcion_principal.subopciones[numero - 1]

        self._log(
            f"✅ Selección: {subopcion.texto} → Grupo: {subopcion.grupo_asignado}"
        )

        # VERIFICAR SI REQUIERE CAPTURA DE DATOS
        if opcion_principal.requiere_captura_datos():
            self._log(f"📝 Iniciando captura de datos para '{opcion_principal.texto}'")

            # Iniciar captura
            estado.iniciar_captura(
                categoria=opcion_principal.texto,
                subopcion=subopcion.texto,
                grupo=subopcion.grupo_asignado,
            )

            # Obtener primera pregunta
            primera_pregunta = estado.datos_captura.get_pregunta_actual()

            return {
                "tipo": "iniciar_captura",
                "texto": f"📋 {subopcion.texto}\n\n{primera_pregunta}",
                "grupo": None,
                "categoria": opcion_principal.texto,
                "subopcion": subopcion.texto,
            }
        else:
            # No requiere captura, asignar directamente
            estado.reset()

            return {
                "tipo": "seleccion_final",
                "texto": f"Ha seleccionado: {subopcion.texto}\n\nUn agente del área de {subopcion.grupo_asignado} se comunicará con usted pronto.",
                "grupo": subopcion.grupo_asignado,
                "opcion_principal": opcion_principal.texto,
                "subopcion": subopcion.texto,
            }

    def _procesar_seleccion_principal(
        self, mensaje: str, telefono: str, estado: EstadoUsuario
    ) -> Dict:
        """Procesa la selección de una opción del menú principal"""
        numero = self._extraer_numero(mensaje)

        if numero is None or numero < 1:
            return {
                "tipo": "invalido",
                "texto": MenuConfig.MENSAJE_SELECCION_INVALIDA,
                "grupo": None,
            }

        opcion = self.obtener_opcion_principal(numero)

        if not opcion:
            return {
                "tipo": "invalido",
                "texto": MenuConfig.MENSAJE_SELECCION_INVALIDA,
                "grupo": None,
            }

        # Si la opción no tiene subopciones, es una selección final
        if not opcion.tiene_subopciones():
            self._log(f"✅ Selección directa: {opcion.texto}")
            estado.reset()
            return {
                "tipo": "seleccion_final_sin_submenu",
                "texto": f"Ha seleccionado: {opcion.texto}\n\nUn agente se comunicará con usted pronto.",
                "grupo": opcion.texto,
                "opcion_principal": opcion.texto,
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
            "opcion_principal": opcion.texto,
        }

    # ------------------------------------------------------------------------
    # MÉTODOS PÚBLICOS - OBTENER MENÚS (COPIADOS DEL ORIGINAL)
    # ------------------------------------------------------------------------

    def obtener_menu_principal_texto(self) -> str:
        """Obtiene el texto del menú principal"""
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
        """Obtiene el texto del submenú de una opción principal"""
        opcion = self.obtener_opcion_principal(numero_opcion_principal)

        if not opcion:
            self._log(f"⚠️  Opción principal {numero_opcion_principal} no encontrada")
            return MenuConfig.MENSAJE_SELECCION_INVALIDA

        if not opcion.tiene_subopciones():
            self._log(f"⚠️  Opción '{opcion.texto}' no tiene subopciones")
            return f"La opción '{opcion.texto}' no tiene subopciones disponibles."

        partes = [f"📋 {opcion.texto}", "", "Seleccione una opción:", ""]

        for idx, subopcion in enumerate(opcion.subopciones, 1):
            # Mostrar solo el número simple en el submenú
            partes.append(f"{idx}. {subopcion.texto}")

        partes.append("")
        partes.append("Escriba 0 para volver al menú principal")

        menu_texto = "\n".join(partes)
        self._log(
            f"✅ Submenú generado para '{opcion.texto}' con {len(opcion.subopciones)} opciones"
        )

        return menu_texto

    def obtener_opciones_principales(
        self, forzar_refresh: bool = False
    ) -> List[OpcionPrincipal]:
        """Obtiene las opciones principales del menú (usa cache)"""
        # Verificar cache
        if not forzar_refresh and self._es_cache_valido():
            return self._cache_opciones

        # Cargar desde Dataverse
        self._log("🔄 Consultando Dataverse...")
        opciones = self._cargar_desde_dataverse()

        # Actualizar cache
        self._cache_opciones = opciones
        self._cache_timestamp = datetime.now()

        return opciones

    def obtener_opcion_principal(self, numero: int) -> Optional[OpcionPrincipal]:
        """Obtiene una opción principal por número"""
        opciones = self.obtener_opciones_principales()

        for opcion in opciones:
            if opcion.numero == numero:
                return opcion

        return None

    # ------------------------------------------------------------------------
    # MÉTODOS PRIVADOS - UTILIDADES
    # ------------------------------------------------------------------------

    def _extraer_numero(self, texto: str) -> Optional[int]:
        """Extrae el primer número de un texto"""
        try:
            # Buscar todos los dígitos
            numeros = [c for c in texto if c.isdigit()]
            if numeros:
                return int("".join(numeros))
            return None
        except:
            return None

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

    def _es_cache_valido(self) -> bool:
        """Verifica si el cache es válido"""
        if not self._cache_opciones or not self._cache_timestamp:
            return False

        expiration = self._cache_timestamp + timedelta(
            minutes=MenuConfig.CACHE_DURATION_MINUTES
        )
        return datetime.now() < expiration

    def _log(self, mensaje: str):
        """Registra un mensaje en el log"""
        if MenuConfig.SHOW_LOGS:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"{self._log_prefix} [{timestamp}] {mensaje}")

    def _cargar_desde_dataverse(self) -> List[OpcionPrincipal]:
        """Carga el menú desde Dataverse (simplificado)"""
        # Por ahora, usar menú hardcoded
        # TODO: Implementar carga real desde Dataverse
        return self._obtener_menu_hardcoded()

    def _obtener_menu_hardcoded(self) -> List[OpcionPrincipal]:
        """Retorna menú hardcoded como fallback"""
        self._log("📋 Usando menú hardcoded")

        return [
            OpcionPrincipal(
                numero=1,
                texto="Solicitud Ticket",
                subopciones=[
                    SubOpcion(
                        "1.1",
                        "Incidente Técnico",
                        "Soporte Técnico",
                        "Solicitud Ticket",
                    ),
                    SubOpcion(
                        "1.2", "Solicitud Servicio", "Service Desk", "Solicitud Ticket"
                    ),
                    SubOpcion(
                        "1.3", "Cambio", "Gestión de Cambios", "Solicitud Ticket"
                    ),
                ],
            ),
            OpcionPrincipal(
                numero=2,
                texto="Ventas",
                subopciones=[
                    SubOpcion("2.1", "Cotización", "Ventas - Cotización", "Ventas"),
                    SubOpcion("2.2", "Catálogo", "Ventas - Catálogo", "Ventas"),
                    SubOpcion("2.3", "Seguimiento", "Ventas - Seguimiento", "Ventas"),
                ],
            ),
            OpcionPrincipal(
                numero=3,
                texto="Solicitar Atención",
                subopciones=[
                    SubOpcion(
                        "3.1",
                        "Hablar con Asesor",
                        "Atención al Cliente",
                        "Solicitar Atención",
                    ),
                    SubOpcion(
                        "3.2",
                        "Atención Urgente",
                        "Equipo de Urgencias",
                        "Solicitar Atención",
                    ),
                ],
            ),
        ]


# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("DEMO: SISTEMA DE MENÚ CON CAPTURA DE TICKETS")
    print("=" * 70)

    def mock_token():
        return "mock_token_12345"

    # Crear sistema
    sistema = SistemaMenuConTickets(
        dataverse_url="https://fake.crm.dynamics.com", token_provider_func=mock_token
    )

    # Simular conversación
    telefono = "+573001234567"

    print("\n1️⃣ Usuario escribe: MENU")
    resultado = sistema.procesar_mensaje("MENU", telefono)
    print(resultado["texto"])

    print("\n2️⃣ Usuario escribe: 1")
    resultado = sistema.procesar_mensaje("1", telefono)
    print(resultado["texto"])

    print("\n3️⃣ Usuario escribe: 1 (Incidente Técnico)")
    resultado = sistema.procesar_mensaje("1", telefono)
    print(f"\nTipo: {resultado['tipo']}")
    print(resultado["texto"])

    print("\n4️⃣ Usuario responde pregunta 1: No puedo acceder al sistema")
    resultado = sistema.procesar_mensaje("No puedo acceder al sistema", telefono)
    print(f"\nTipo: {resultado['tipo']}")
    print(resultado["texto"])

    print("\n5️⃣ Usuario responde pregunta 2: Desde esta mañana")
    resultado = sistema.procesar_mensaje("Desde esta mañana", telefono)
    print(f"\nTipo: {resultado['tipo']}")
    print(resultado["texto"])
    print(f"\nGrupo asignado: {resultado['grupo']}")
    print(f"Ticket ID: {resultado.get('ticket_id', 'N/A')}")
