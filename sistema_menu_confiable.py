"""
SISTEMA DE MENÚ CONFIABLE CON NUMERACIÓN CONSECUTIVA
====================================================

Este módulo proporciona una gestión robusta del menú de WhatsApp con:
✅ Numeración automática consecutiva (1, 2, 3...)
✅ Validación de datos
✅ Caché inteligente
✅ Logs detallados
✅ Orden personalizable

Autor: Sistema CRM WhatsApp
Fecha: Febrero 2026
"""

import json
import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Tuple

import requests

# ============================================================================
# CONFIGURACIÓN
# ============================================================================


class MenuConfig:
    """Configuración del sistema de menú"""

    CACHE_DURATION_MINUTES = 5
    MAX_OPCIONES_POR_CATEGORIA = 10
    MENSAJE_BIENVENIDA = "Bienvenido! Por favor seleccione una opción:"
    MENSAJE_ERROR = "Lo sentimos, ocurrió un error. Intente nuevamente."
    SHOW_LOGS = True


# ============================================================================
# MODELOS DE DATOS
# ============================================================================


@dataclass
class OpcionMenu:
    """Representa una opción individual del menú"""

    numero: int
    texto: str
    categoria: Optional[str] = None
    activa: bool = True
    metadata: Optional[Dict] = None

    def __str__(self) -> str:
        return f"{self.numero}. {self.texto}"

    def to_dict(self) -> Dict:
        return {
            "numero": self.numero,
            "texto": self.texto,
            "categoria": self.categoria,
            "activa": self.activa,
            "metadata": self.metadata,
        }


@dataclass
class MenuCache:
    """Cache del menú con timestamp"""

    opciones: List[OpcionMenu]
    timestamp: datetime

    def is_expired(self, duration_minutes: int = 5) -> bool:
        """Verifica si el cache ha expirado"""
        expiration = self.timestamp + timedelta(minutes=duration_minutes)
        return datetime.now() >= expiration

    def get_age_seconds(self) -> float:
        """Obtiene la edad del cache en segundos"""
        return (datetime.now() - self.timestamp).total_seconds()


# ============================================================================
# SISTEMA DE MENÚ PRINCIPAL
# ============================================================================


class SistemaMenuConfiable:
    """
    Gestiona el menú de WhatsApp de forma confiable y escalable.

    Características:
    - Numeración automática consecutiva
    - Cache con actualización automática
    - Validación de datos robusta
    - Logs detallados para debugging
    - Orden personalizable
    """

    def __init__(self, dataverse_url: str, token_provider_func):
        """
        Inicializa el sistema de menú

        Args:
            dataverse_url: URL base de Dataverse
            token_provider_func: Función que retorna el access token
        """
        self.dataverse_url = dataverse_url
        self.get_token = token_provider_func
        self._cache: Optional[MenuCache] = None
        self._log_prefix = "[MENU_CONFIABLE]"

    # ------------------------------------------------------------------------
    # MÉTODOS PÚBLICOS
    # ------------------------------------------------------------------------

    def obtener_menu_texto(self, incluir_bienvenida: bool = True) -> str:
        """
        Obtiene el menú formateado como texto para WhatsApp

        Args:
            incluir_bienvenida: Si se incluye el mensaje de bienvenida

        Returns:
            String con el menú completo numerado
        """
        opciones = self.obtener_opciones()

        if not opciones:
            self._log("⚠️  No hay opciones disponibles en el menú")
            return MenuConfig.MENSAJE_ERROR

        # Construir el texto del menú
        partes = []

        if incluir_bienvenida:
            partes.append(MenuConfig.MENSAJE_BIENVENIDA)
            partes.append("")

        # Agregar cada opción
        for opcion in opciones:
            partes.append(str(opcion))

        menu_texto = "\n".join(partes)

        self._log(f"✅ Menú generado con {len(opciones)} opciones")
        self._log(f"📄 Texto del menú:\n{menu_texto}", detalle=True)

        return menu_texto

    def obtener_opciones(self, forzar_refresh: bool = False) -> List[OpcionMenu]:
        """
        Obtiene la lista de opciones del menú

        Args:
            forzar_refresh: Si True, ignora el cache y consulta Dataverse

        Returns:
            Lista de opciones del menú ordenadas y numeradas
        """
        # Verificar cache
        if (
            not forzar_refresh
            and self._cache
            and not self._cache.is_expired(MenuConfig.CACHE_DURATION_MINUTES)
        ):
            edad = self._cache.get_age_seconds()
            self._log(f"✅ Usando cache (edad: {edad:.1f}s)")
            return self._cache.opciones

        # Cache expirado o no existe, consultar Dataverse
        self._log("🔄 Cache expirado o forzando refresh, consultando Dataverse...")
        opciones = self._cargar_desde_dataverse()

        # Actualizar cache
        self._cache = MenuCache(opciones=opciones, timestamp=datetime.now())
        self._log(f"✅ Cache actualizado con {len(opciones)} opciones")

        return opciones

    def obtener_opcion_por_numero(self, numero: int) -> Optional[OpcionMenu]:
        """
        Obtiene una opción específica por su número

        Args:
            numero: Número de la opción (1, 2, 3...)

        Returns:
            OpcionMenu si existe, None si no
        """
        opciones = self.obtener_opciones()

        for opcion in opciones:
            if opcion.numero == numero:
                return opcion

        return None

    def validar_seleccion(self, texto_usuario: str) -> Optional[OpcionMenu]:
        """
        Valida y encuentra la opción seleccionada por el usuario

        Args:
            texto_usuario: Texto enviado por el usuario (ej: "1", "2", "opcion 3")

        Returns:
            OpcionMenu si la selección es válida, None si no
        """
        # Intentar extraer número del texto
        numero = self._extraer_numero(texto_usuario)

        if numero is None:
            self._log(f"⚠️  No se pudo extraer número de: '{texto_usuario}'")
            return None

        # Buscar la opción
        opcion = self.obtener_opcion_por_numero(numero)

        if opcion:
            self._log(f"✅ Selección válida: {opcion}")
        else:
            self._log(f"❌ Selección inválida: número {numero} no existe")

        return opcion

    def invalidar_cache(self):
        """Invalida el cache para forzar actualización en próxima consulta"""
        self._cache = None
        self._log("🗑️  Cache invalidado")

    # ------------------------------------------------------------------------
    # MÉTODOS PRIVADOS
    # ------------------------------------------------------------------------

    def _cargar_desde_dataverse(self) -> List[OpcionMenu]:
        """
        Carga el menú desde Dataverse

        Returns:
            Lista de opciones ordenadas y numeradas
        """
        token = self.get_token()
        if not token:
            self._log("❌ Error al obtener token de autenticación")
            return []

        # Consultar chatbots activos
        url = f"{self.dataverse_url}/api/data/v9.2/cr321_chatbots"
        url += "?$select=cr321_chatbotid,cr321_name,cr321_active"
        url += ",cr321_elemento1,cr321_elemento2,cr321_elemento3,cr321_elemento4,cr321_elemento5"
        url += ",cr321_orden"  # Campo opcional para orden personalizado
        url += "&$filter=cr321_active eq true"
        url += "&$orderby=cr321_orden asc,cr321_name asc"  # Orden: primero por cr321_orden, luego alfabético

        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

        try:
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code != 200:
                self._log(f"❌ Error HTTP {response.status_code} al consultar chatbots")
                return []

            data = response.json()
            chatbots = data.get("value", [])

            self._log(f"📥 Obtenidos {len(chatbots)} chatbots activos de Dataverse")

            # Procesar y validar
            opciones = self._procesar_chatbots(chatbots)

            return opciones

        except requests.exceptions.Timeout:
            self._log("❌ Timeout al consultar Dataverse")
            return []
        except Exception as e:
            self._log(f"❌ Excepción al consultar Dataverse: {e}")
            return []

    def _procesar_chatbots(self, chatbots: List[Dict]) -> List[OpcionMenu]:
        """
        Procesa los chatbots y genera lista de opciones numeradas

        Args:
            chatbots: Lista de chatbots desde Dataverse

        Returns:
            Lista de OpcionMenu validadas y numeradas
        """
        opciones = []
        numero_actual = 1

        for chatbot in chatbots:
            nombre_categoria = chatbot.get("cr321_name", "").strip()

            # Validar nombre de categoría
            if not nombre_categoria:
                self._log(
                    f"⚠️  Chatbot {chatbot.get('cr321_chatbotid')} sin nombre, omitiendo"
                )
                continue

            # Extraer elementos
            elementos = []
            for i in range(1, 6):
                elemento = chatbot.get(f"cr321_elemento{i}", "")
                if elemento and elemento.strip():
                    elementos.append(elemento.strip())

            # Validar que tenga al menos 1 elemento
            if not elementos:
                self._log(f"⚠️  Categoría '{nombre_categoria}' sin elementos, omitiendo")
                continue

            # Limitar a máximo de opciones
            if len(elementos) > MenuConfig.MAX_OPCIONES_POR_CATEGORIA:
                self._log(
                    f"⚠️  Categoría '{nombre_categoria}' tiene {len(elementos)} elementos, "
                    + f"usando solo los primeros {MenuConfig.MAX_OPCIONES_POR_CATEGORIA}"
                )
                elementos = elementos[: MenuConfig.MAX_OPCIONES_POR_CATEGORIA]

            # Crear opción para cada elemento
            for elemento_texto in elementos:
                opcion = OpcionMenu(
                    numero=numero_actual,
                    texto=elemento_texto,
                    categoria=nombre_categoria,
                    activa=True,
                    metadata={
                        "chatbot_id": chatbot.get("cr321_chatbotid"),
                        "chatbot_name": nombre_categoria,
                        "orden": chatbot.get("cr321_orden"),
                    },
                )
                opciones.append(opcion)
                numero_actual += 1

        self._log(f"✅ Procesadas {len(opciones)} opciones de menú")

        return opciones

    def _extraer_numero(self, texto: str) -> Optional[int]:
        """
        Extrae el número de la selección del usuario

        Args:
            texto: Texto del usuario (ej: "1", "opción 2", "3.", etc.)

        Returns:
            Número extraído o None si no se encuentra
        """
        import re

        # Buscar primer número en el texto
        match = re.search(r"\d+", texto)
        if match:
            try:
                return int(match.group())
            except ValueError:
                return None

        return None

    def _log(self, mensaje: str, detalle: bool = False):
        """
        Registra un log del sistema de menú

        Args:
            mensaje: Mensaje a registrar
            detalle: Si es un mensaje de detalle (solo se muestra si SHOW_LOGS=True)
        """
        if MenuConfig.SHOW_LOGS or not detalle:
            print(f"{self._log_prefix} {mensaje}")


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================


def crear_sistema_menu(dataverse_url: str, token_provider_func) -> SistemaMenuConfiable:
    """
    Factory function para crear una instancia del sistema de menú

    Args:
        dataverse_url: URL base de Dataverse
        token_provider_func: Función que retorna el access token

    Returns:
        Instancia de SistemaMenuConfiable
    """
    return SistemaMenuConfiable(dataverse_url, token_provider_func)


# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    """
    Ejemplo de cómo usar el sistema de menú confiable
    """
    import sys

    sys.path.append("backend")

    try:
        from goot import CLIENT_ID, CLIENT_SECRET, DATAVERSE_URL, TENANT_ID

        def get_token():
            """Obtener token de autenticación"""
            url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
            data = {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "scope": f"{DATAVERSE_URL}/.default",
                "grant_type": "client_credentials",
            }
            response = requests.post(url, data=data)
            if response.status_code == 200:
                return response.json().get("access_token")
            return None

        # Crear sistema de menú
        print("=" * 70)
        print("SISTEMA DE MENÚ CONFIABLE - DEMO")
        print("=" * 70)
        print()

        sistema = crear_sistema_menu(DATAVERSE_URL, get_token)

        # Obtener y mostrar menú
        print("\n1️⃣  OBTENIENDO MENÚ...")
        print("-" * 70)
        menu_texto = sistema.obtener_menu_texto()
        print("=" * 70)
        print(menu_texto)
        print("=" * 70)

        # Obtener opciones individuales
        print("\n2️⃣  LISTADO DE OPCIONES:")
        print("-" * 70)
        opciones = sistema.obtener_opciones()
        for opcion in opciones:
            print(f"  {opcion} [Categoría: {opcion.categoria}]")

        # Validar selecciones
        print("\n3️⃣  VALIDANDO SELECCIONES:")
        print("-" * 70)
        pruebas = ["1", "2", "opcion 3", "99", "hola"]
        for prueba in pruebas:
            resultado = sistema.validar_seleccion(prueba)
            if resultado:
                print(f"  '{prueba}' → ✅ {resultado}")
            else:
                print(f"  '{prueba}' → ❌ Inválida")

        print("\n✅ Demo completada exitosamente")

    except ImportError:
        print("❌ Error: No se pudo importar configuración de backend/goot.py")
        print(
            "   Asegúrate de que el archivo existe y tiene las credenciales correctas"
        )
    except Exception as e:
        print(f"❌ Error: {e}")
