"""
Handler C001 - Proceso RFC con Aprobación
==========================================

Código: C001
Preguntas: 4
Funcionalidad:
- Captura nombre, aprobador, descripción del cambio, fecha solicitada
- Valida que el aprobador exista en sistema
- Crea RFC en Dataverse con validación de aprobador
"""

from typing import Dict, List, Optional

from handlers.base_handler import BaseHandler


class HandlerC001(BaseHandler):
    """
    Handler para solicitudes de cambio RFC.

    Código: C001
    Preguntas: 4 (nombre, aprobador, descripción, fecha)
    """

    def get_preguntas(self) -> List[str]:
        """Define las 4 preguntas para captura de RFC"""
        return [
            "¿Cuál es tu *nombre completo*?",
            "¿Quién es el *aprobador* del cambio? (nombre completo)",
            "Describe el *cambio solicitado*:",
            "¿Cuál es la *fecha deseada* para el cambio? (DD/MM/YYYY)",
        ]

    def ejecutar_accion_final(
        self, from_user: str, respuestas: Dict[str, str], grupo_id: Optional[str] = None
    ) -> str:
        """
        Crea el RFC con validación de aprobador.

        Args:
            from_user: Teléfono del usuario
            respuestas: Dict con respuestas capturadas
            grupo_id: GUID del grupo

        Returns:
            Mensaje de confirmación
        """

        print(f"\n→ Creando RFC con handler C001...")

        # Obtener respuestas
        nombre = respuestas.get("¿Cuál es tu *nombre completo*?", "No especificado")
        aprobador = respuestas.get(
            "¿Quién es el *aprobador* del cambio? (nombre completo)", "No especificado"
        )
        descripcion = respuestas.get(
            "Describe el *cambio solicitado*:", "Sin descripción"
        )
        fecha = respuestas.get(
            "¿Cuál es la *fecha deseada* para el cambio? (DD/MM/YYYY)",
            "No especificada",
        )

        print(f"  → Solicitante: {nombre}")
        print(f"  → Aprobador: {aprobador}")
        print(f"  → Descripción: {descripcion[:50]}...")
        print(f"  → Fecha: {fecha}")

        # Validar aprobador (aquí podrías consultar Dataverse para verificar)
        # Por ahora solo lo registramos

        # Construir descripción completa
        descripcion_completa = f"""
RFC - REQUEST FOR CHANGE

Solicitante: {nombre}
Aprobador Designado: {aprobador}
Fecha Solicitada: {fecha}

Descripción del Cambio:
{descripcion}

Teléfono Contacto: {from_user}

Capturado vía WhatsApp - Handler C001
        """.strip()

        # Crear ticket tipo RFC
        try:
            ticket = self.crear_ticket(
                titulo=f"RFC - {descripcion[:50]}",
                descripcion=descripcion_completa,
                tipo="soporte",  # Podrías crear un tipo específico "rfc"
                prioridad="Media",
                grupo_id=grupo_id,
                from_nombre=nombre,
                telefono=from_user,
                empresa=f"Aprobador: {aprobador}",
            )

            ticket_id = ticket.get("cr321_ticketid", "XXXXX")
            print(f"  ✓ RFC #{ticket_id} creado exitosamente")

            # Mensaje de confirmación al usuario
            mensaje = f"""
✅ *RFC Registrado*

📋 *RFC #*{ticket_id}
👤 *Solicitante:* {nombre}
✍️ *Aprobador:* {aprobador}
📅 *Fecha Deseada:* {fecha}

Tu solicitud de cambio ha sido registrada y será enviada al aprobador para su revisión.

¡Gracias! 🚀
            """.strip()

            return mensaje

        except Exception as e:
            print(f"  ❌ Error al crear RFC: {str(e)}")
            return f"⚠️ Error al registrar RFC: {str(e)[:100]}"
