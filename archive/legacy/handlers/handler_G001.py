"""
Handler G001 - Asignación Directa sin Preguntas
================================================

Código: G001
Preguntas: 0
Funcionalidad:
- No hace preguntas
- Asigna conversación directamente al grupo
- Notifica al grupo que hay una solicitud
"""

from typing import Dict, List, Optional

from handlers.base_handler import BaseHandler


class HandlerG001(BaseHandler):
    """
    Handler para asignación directa a grupo.

    Código: G001
    Preguntas: 0 (asignación automática)
    """

    def get_preguntas(self) -> List[str]:
        """No hace preguntas, asignación directa"""
        return []

    def ejecutar_accion_final(
        self, from_user: str, respuestas: Dict[str, str], grupo_id: Optional[str] = None
    ) -> str:
        """
        Asigna conversación al grupo y notifica.

        Args:
            from_user: Teléfono del usuario
            respuestas: Dict con respuestas (vacío)
            grupo_id: GUID del grupo

        Returns:
            Mensaje de confirmación
        """

        print(f"\n→ Asignando conversación al grupo con handler G001...")
        print(f"  → Usuario: {from_user}")
        print(f"  → Grupo: {grupo_id}")

        # Asignar conversación
        if grupo_id:
            exito = self.asignar_conversacion(from_user, grupo_id)

            if exito:
                mensaje = f"""
✅ *Solicitud de Atención*

Tu conversación ha sido asignada a un agente.

Un miembro de nuestro equipo se pondrá en contacto contigo en breve.

⏱️ Tiempo estimado de respuesta: 5-10 minutos

¡Gracias por tu paciencia! 😊
                """.strip()

                print(f"  ✓ Conversación asignada al grupo {grupo_id}")
            else:
                mensaje = "⚠️ Error al asignar conversación. Intenta nuevamente."
                print(f"  ❌ Error al asignar conversación")
        else:
            mensaje = "⚠️ No se pudo determinar el grupo de atención."
            print(f"  ❌ No hay grupo_id")

        return mensaje
