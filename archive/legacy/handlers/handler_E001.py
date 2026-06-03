"""
Handler E001 - Envío de PDF sin Preguntas
==========================================

Código: E001
Preguntas: 0
Funcionalidad:
- No hace preguntas
- Envía catálogo en PDF (simulado)
- No asigna a ningún grupo
"""

from typing import Dict, List, Optional

from handlers.base_handler import BaseHandler


class HandlerE001(BaseHandler):
    """
    Handler para envío de catálogo PDF.

    Código: E001
    Preguntas: 0 (respuesta automática)
    """

    def get_preguntas(self) -> List[str]:
        """No hace preguntas, respuesta automática"""
        return []

    def ejecutar_accion_final(
        self, from_user: str, respuestas: Dict[str, str], grupo_id: Optional[str] = None
    ) -> str:
        """
        Envía catálogo PDF (mensaje con link).

        Args:
            from_user: Teléfono del usuario
            respuestas: Dict con respuestas (vacío para este handler)
            grupo_id: GUID del grupo (no usado)

        Returns:
            Mensaje con link al catálogo
        """

        print(f"\n→ Enviando catálogo PDF con handler E001 a {from_user}...")

        # En producción, aquí enviarías el PDF real usando WhatsApp Media API
        # Por ahora, retornamos mensaje con link

        mensaje = f"""
📄 *Catálogo de Productos*

Descarga nuestro catálogo completo aquí:
🔗 https://www.binario.com.co/catalogo.pdf

Encontrarás:
• Productos y servicios
• Precios actualizados
• Especificaciones técnicas
• Información de contacto

¿Necesitas más información? ¡Contáctanos! 📞
        """.strip()

        print(f"  ✓ Catálogo enviado a {from_user}")

        return mensaje
