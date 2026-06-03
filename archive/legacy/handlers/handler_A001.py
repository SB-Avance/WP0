"""
Handler A001 - Captura de Incidentes con Escalamiento
====================================================

Código: A001
Preguntas: 3
Funcionalidad:
- Captura nombre, asunto, empresa
- Crea ticket en Dataverse
- Asigna a grupo configurado en JSON
"""

from typing import Dict, List, Optional

from handlers.base_handler import BaseHandler


class HandlerA001(BaseHandler):
    """
    Handler para captura de incidentes técnicos.

    Código: A001
    Preguntas: nombre, asunto, empresa
    """

    def get_preguntas(self) -> List[str]:
        """Define las 3 preguntas para captura"""
        return [
            "¿Cuál es tu *nombre completo*?",
            "¿Cuál es el *asunto* del incidente?",
            "¿De qué *empresa* eres?",
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

        print(f"\n→ Creando ticket con handler A001...")

        # Obtener respuestas
        nombre = respuestas.get("¿Cuál es tu *nombre completo*?", "No especificado")
        asunto = respuestas.get(
            "¿Cuál es el *asunto* del incidente?", "No especificado"
        )
        empresa = respuestas.get("¿De qué *empresa* eres?", "No especificado")

        print(f"  → Nombre: {nombre}")
        print(f"  → Asunto: {asunto}")
        print(f"  → Empresa: {empresa}")
        print(f"  → Grupo: {grupo_id}")

        # Crear descripción
        descripcion = f"""
INCIDENTE TÉCNICO

Nombre: {nombre}
Empresa: {empresa}
Asunto: {asunto}
Teléfono: {from_user}

Capturado vía WhatsApp - Handler A001
        """.strip()

        # Crear ticket en Dataverse
        ticket = self.crear_ticket(
            titulo=asunto, descripcion=descripcion, prioridad="Media", grupo_id=grupo_id
        )

        ticket_id = ticket.get("cr321_ticketid", "XXXXX")
        print(f"  ✓ Ticket #{ticket_id} creado")

        # Mensaje de confirmación
        mensaje = f"""
✅ *Ticket registrado*

📋 Número: #{ticket_id}
👤 Nombre: {nombre}
🏢 Empresa: {empresa}
📝 Asunto: {asunto}

Un agente te contactará pronto.
Gracias por reportar el incidente.
        """.strip()

        return mensaje
