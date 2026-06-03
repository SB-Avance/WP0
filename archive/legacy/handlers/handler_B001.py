"""
Handler B001 - Solicitud de Servicio Básica
=========================================

Código: B001
Preguntas: 2
Funcionalidad:
- Captura asunto y descripción de la solicitud
- Crea ticket en Dataverse tipo "soporte"
- Asigna a grupo configurado en JSON
"""

from typing import Dict, List, Optional

from handlers.base_handler import BaseHandler


class HandlerB001(BaseHandler):
    """
    Handler para solicitudes de servicio básicas.

    Código: B001
    Preguntas: 2 (asunto y descripción)
    """

    def get_preguntas(self) -> List[str]:
        """Define las 2 preguntas para captura de solicitud"""
        return [
            "¿Cuál es el *asunto* de tu solicitud?",
            "Por favor, describe brevemente tu *solicitud de servicio*",
        ]

    def ejecutar_accion_final(
        self, from_user: str, respuestas: Dict[str, str], grupo_id: Optional[str] = None
    ) -> str:
        """
        Crea el ticket con los datos capturados.

        Args:
            from_user: Teléfono del usuario
            respuestas: Dict con respuestas capturadas
            grupo_id: GUID del grupo (viene del JSON de Dataverse)

        Returns:
            Mensaje de confirmación
        """

        print(f"\n→ Creando ticket con handler B001 (Solicitud de Servicio)...")

        # Obtener respuestas
        asunto = respuestas.get(
            "¿Cuál es el *asunto* de tu solicitud?", "Solicitud de servicio"
        )
        descripcion = respuestas.get(
            "Por favor, describe brevemente tu *solicitud de servicio*",
            "Sin descripción",
        )

        print(f"  → Asunto: {asunto}")
        print(f"  → Descripción: {descripcion[:50]}...")
        print(f"  → Grupo: {grupo_id}")
        print(f"  → Usuario: {from_user}")

        # Construir descripción completa
        descripcion_completa = f"""
SOLICITUD DE SERVICIO

Asunto: {asunto}
Descripción: {descripcion}
Teléfono: {from_user}

Capturado vía WhatsApp - Handler B001
        """.strip()

        # Crear ticket en Dataverse
        try:
            ticket = self.crear_ticket(
                titulo=asunto,
                descripcion=descripcion_completa,
                tipo="soporte",
                prioridad="Media",
                grupo_id=grupo_id,
                from_nombre="Cliente WhatsApp",
                telefono=from_user,
                empresa="",
            )

            ticket_id = ticket.get("cr321_ticketid", "XXXXX")
            print(f"  ✓ Ticket #{ticket_id} creado exitosamente")

            # Mensaje de confirmación al usuario
            mensaje = f"""
✅ *Solicitud registrada*

📋 *Ticket #*{ticket_id}
📝 *Asunto:* {asunto}

Tu solicitud ha sido registrada y será atendida pronto por nuestro equipo.

¡Gracias por contactarnos! 😊
            """.strip()

            return mensaje

        except Exception as e:
            print(f"  ❌ Error al crear ticket: {str(e)}")

            # Mensaje de error al usuario
            return f"""
⚠️ *Hubo un problema al registrar tu solicitud*

Por favor, intenta nuevamente más tarde o contacta directamente con soporte.

Error: {str(e)[:100]}
            """.strip()

    def validar_asunto(self, asunto: str) -> bool:
        """
        Valida que el asunto sea válido.

        Args:
            asunto: Texto del asunto

        Returns:
            True si es válido
        """
        # Validar longitud mínima
        if len(asunto.strip()) < 5:
            return False

        # Validar longitud máxima
        if len(asunto) > 200:
            return False

        return True

    def validar_descripcion(self, descripcion: str) -> bool:
        """
        Valida que la descripción sea válida.

        Args:
            descripcion: Texto de la descripción

        Returns:
            True si es válida
        """
        # Validar longitud mínima
        if len(descripcion.strip()) < 10:
            return False

        # Validar longitud máxima
        if len(descripcion) > 2000:
            return False

        return True
