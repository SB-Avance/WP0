"""
Handler Default - Handler por Defecto
======================================

Código: X999
Preguntas: 0
Funcionalidad:
- Se usa cuando no se encuentra el handler especificado
- Respuesta genérica
- Opcionalmente crea ticket básico
"""

from typing import Dict, List, Optional
from handlers.base_handler import BaseHandler


class HandlerDefault(BaseHandler):
    """
    Handler por defecto (fallback).
    
    Código: X999
    Usado cuando el código del handler no existe o está inactivo.
    """
    
    def get_preguntas(self) -> List[str]:
        """No hace preguntas, respuesta directa"""
        return []
    
    
    def ejecutar_accion_final(
        self,
        from_user: str,
        respuestas: Dict[str, str],
        grupo_id: Optional[str] = None
    ) -> str:
        """
        Respuesta genérica de fallback.
        
        Args:
            from_user: Teléfono del usuario
            respuestas: Dict con respuestas (vacío)
            grupo_id: GUID del grupo
        
        Returns:
            Mensaje genérico
        """
        
        print(f"\n→ Usando handler por defecto (X999) para {from_user}...")
        
        mensaje = f"""
ℹ️ *Gracias por contactarnos*

Hemos recibido tu mensaje.

Un agente revisará tu solicitud y te contactará pronto.

Si necesitas atención inmediata, por favor llama a:
📞 +57 300 123 4567

¡Que tengas un excelente día! 😊
        """.strip()
        
        print(f"  ✓ Respuesta genérica enviada")
        
        return mensaje
