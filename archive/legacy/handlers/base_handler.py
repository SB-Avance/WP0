"""
Clase Base para Handlers
========================

Todos los handlers heredan de esta clase y deben implementar:
- get_preguntas(): Lista de preguntas a hacer al usuario
- ejecutar_accion_final(): Acción a ejecutar con los datos capturados
"""

import os
import sys
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import datetime, timezone

import requests
from goot import DATAVERSE_URL, get_token


class BaseHandler(ABC):
    """
    Clase base abstracta para todos los handlers del sistema.
    Define la interfaz que todos los handlers deben implementar.
    """

    def __init__(self, codigo: str, config: Dict):
        """
        Inicializa el handler con su configuración.

        Args:
            codigo: Código único del handler (ej: A001, B001)
            config: Configuración del handler desde config_handlers.json
        """
        self.codigo = codigo
        self.config = config
        self.nombre = config.get("nombre", "")
        self.activo = config.get("activo", True)
        self.usa_grupo_de_dataverse = config.get("usa_grupo_de_dataverse", True)
        self.grupo_override = config.get("grupo_override")

    @abstractmethod
    def get_preguntas(self) -> List[str]:
        """
        Define las preguntas que el handler hará al usuario.

        Returns:
            Lista de strings con las preguntas a realizar
        """
        pass

    @abstractmethod
    def ejecutar_accion_final(
        self, from_user: str, respuestas: Dict[str, str], grupo_id: Optional[str] = None
    ) -> str:
        """
        Ejecuta la acción final del handler con los datos capturados.

        Args:
            from_user: Teléfono/identificador del usuario
            respuestas: Diccionario con las respuestas del usuario
            grupo_id: GUID del grupo al que asignar (opcional)

        Returns:
            Mensaje de confirmación para enviar al usuario
        """
        pass

    # === MÉTODOS AUXILIARES ===

    def crear_ticket(
        self,
        titulo: str,
        descripcion: str,
        tipo: str = "soporte",
        prioridad: str = "Media",
        grupo_id: Optional[str] = None,
        from_nombre: str = "No especificado",
        telefono: str = "",
        empresa: str = "",
    ) -> Dict:
        """
        Crea un ticket en Dataverse.

        Args:
            titulo: Título del ticket
            descripcion: Descripción detallada
            tipo: Tipo de ticket (soporte, cotizacion, informacion, atencion_agente)
            prioridad: Prioridad (Baja, Media, Alta, Urgente)
            grupo_id: GUID del grupo asignado
            from_nombre: Nombre del contacto
            telefono: Teléfono del contacto
            empresa: Empresa del contacto

        Returns:
            Dict con información del ticket creado
        """
        token = get_token()
        if not token:
            raise Exception("No se pudo obtener token de autenticación")

        # Mapeos
        tipo_map = {
            "soporte": 462410000,
            "cotizacion": 462410001,
            "informacion": 462410002,
            "atencion_agente": 462410003,
        }

        # Obtener siguiente ID
        next_id = self._get_next_ticket_id(token)

        # Preparar payload
        now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

        payload = {
            "cr321_idticket": next_id,
            "cr321_fromnombre": from_nombre,
            "cr321_telefono": telefono,
            "cr321_empresa": empresa,
            "cr321_descripcion": descripcion,
            "cr321_tipo": tipo_map.get(tipo.lower(), 462410000),
            "cr321_fechacreacion": now,
            "cr321_fechaactualizacion": now,
        }

        # Asociar grupo si se proporciona
        if grupo_id:
            payload["cr321_grupoId@odata.bind"] = f"/cr321_grups({grupo_id})"

        # Crear ticket
        url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_ticketses"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 204:
            return {
                "cr321_ticketid": next_id,
                "success": True,
                "mensaje": f"Ticket #{next_id} creado exitosamente",
            }
        else:
            raise Exception(
                f"Error al crear ticket: {response.status_code} - {response.text}"
            )

    def _get_next_ticket_id(self, token: str) -> int:
        """Obtiene el siguiente ID consecutivo de ticket"""
        search_url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_ticketses?$select=cr321_idticket&$orderby=cr321_idticket desc&$top=1"
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

        response = requests.get(search_url, headers=headers)

        next_id = 1
        if response.status_code == 200:
            data = response.json()
            tickets = data.get("value", [])
            if tickets:
                last_id = tickets[0].get("cr321_idticket", 0)
                next_id = last_id + 1

        return next_id

    def asignar_conversacion(self, from_user: str, grupo_id: str) -> bool:
        """
        Asigna una conversación a un grupo en Dataverse.

        Args:
            from_user: Teléfono del usuario
            grupo_id: GUID del grupo

        Returns:
            True si se asignó correctamente
        """
        token = get_token()
        if not token:
            return False

        # Implementar lógica de asignación si es necesaria
        # Por ahora solo retornamos True
        return True

    def validar_respuestas(self, respuestas: Dict[str, str]) -> bool:
        """
        Valida que todas las respuestas necesarias estén presentes.

        Args:
            respuestas: Diccionario con las respuestas del usuario

        Returns:
            True si todas las respuestas están presentes
        """
        preguntas = self.get_preguntas()
        for pregunta in preguntas:
            if pregunta not in respuestas or not respuestas[pregunta].strip():
                return False
        return True
