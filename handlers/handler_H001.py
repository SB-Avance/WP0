"""
Handler H001 - Urgencia con Notificación Multicanal
====================================================

Código: H001
Preguntas: 1
Funcionalidad:
- Captura descripción de urgencia
- Crea ticket con prioridad URGENTE
- Asigna a grupo de supervisores (override)
- Notifica por múltiples canales (simulado)
"""

from typing import Dict, List, Optional
from handlers.base_handler import BaseHandler


class HandlerH001(BaseHandler):
    """
    Handler para urgencias con notificaciones multicanal.
    
    Código: H001
    Preguntas: 1 (descripción de urgencia)
    """
    
    def get_preguntas(self) -> List[str]:
        """Define la pregunta para urgencia"""
        return [
            "🚨 Describe la *urgencia* lo más detallado posible:"
        ]
    
    
    def ejecutar_accion_final(
        self,
        from_user: str,
        respuestas: Dict[str, str],
        grupo_id: Optional[str] = None
    ) -> str:
        """
        Crea ticket urgente y notifica por múltiples canales.
        
        Args:
            from_user: Teléfono del usuario
            respuestas: Dict con respuestas capturadas
            grupo_id: GUID del grupo (se ignora, se usa grupo_override)
        
        Returns:
            Mensaje de confirmación
        """
        
        print(f"\n→ Procesando URGENCIA con handler H001...")
        
        # Obtener descripción
        descripcion = respuestas.get("🚨 Describe la *urgencia* lo más detallado posible:", "Urgencia sin descripción")
        
        print(f"  → Usuario: {from_user}")
        print(f"  → Descripción: {descripcion[:100]}...")
        print(f"  ⚠️ PRIORIDAD: URGENTE")
        
        # Nota: grupo_id viene del config como grupo_override (Supervisores)
        # Ya viene configurado desde handler_manager
        
        # Construir descripción completa
        descripcion_completa = f"""
🚨🚨🚨 URGENCIA 🚨🚨🚨

DESCRIPCIÓN:
{descripcion}

CONTACTO: {from_user}
FECHA: {self._get_timestamp()}

Capturada vía WhatsApp - Handler H001
REQUIERE ATENCIÓN INMEDIATA
        """.strip()
        
        # Crear ticket con prioridad URGENTE
        try:
            ticket = self.crear_ticket(
                titulo=f"🚨 URGENCIA - {descripcion[:50]}",
                descripcion=descripcion_completa,
                tipo="atencion_agente",
                prioridad="Urgente",
                grupo_id=grupo_id,  # Ya viene del override en config
                from_nombre="Cliente WhatsApp",
                telefono=from_user,
                empresa=""
            )
            
            ticket_id = ticket.get('cr321_ticketid', 'XXXXX')
            print(f"  ✓ Ticket URGENTE #{ticket_id} creado")
            
            # Simular notificaciones multicanal
            self._enviar_notificaciones_multicanal(ticket_id, descripcion, from_user)
            
            # Mensaje de confirmación al usuario
            mensaje = f"""
🚨 *URGENCIA REGISTRADA*

📋 *Ticket #*{ticket_id}
⚡ *Prioridad:* URGENTE

Tu urgencia ha sido escalada a nuestro equipo de supervisores.

📞 Te contactaremos en los próximos *2-5 minutos*.

Mantente atento a tu teléfono.

🚀 ¡Gracias por reportar!
            """.strip()
            
            return mensaje
            
        except Exception as e:
            print(f"  ❌ Error al crear ticket urgente: {str(e)}")
            return f"""
⚠️ *Error al registrar urgencia*

Por favor, llama directamente a nuestro número de emergencias:
📞 +57 300 123 4567

Error técnico: {str(e)[:50]}
            """.strip()
    
    
    def _enviar_notificaciones_multicanal(self, ticket_id: str, descripcion: str, telefono: str):
        """
        Simula envío de notificaciones por múltiples canales.
        En producción, integraría con servicios de SMS, Email, Teams, etc.
        """
        print(f"  📧 Enviando email a supervisores...")
        print(f"  📱 Enviando SMS a guardia...")
        print(f"  💬 Notificando en Teams...")
        print(f"  ✓ Notificaciones multicanal enviadas para ticket #{ticket_id}")
    
    
    def _get_timestamp(self) -> str:
        """Retorna timestamp actual formateado"""
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
