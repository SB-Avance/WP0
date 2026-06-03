"""
Handler D001 - Cotización con Cálculo Automático
================================================

Código: D001
Preguntas: 2
Funcionalidad:
- Captura producto y cantidad
- Consulta precios en sistema (simulado)
- Genera cotización automática
"""

from typing import Dict, List, Optional

from handlers.base_handler import BaseHandler


class HandlerD001(BaseHandler):
    """
    Handler para generación de cotizaciones.

    Código: D001
    Preguntas: 2 (producto, cantidad)
    """

    def get_preguntas(self) -> List[str]:
        """Define las 2 preguntas para cotización"""
        return ["¿Qué *producto* deseas cotizar?", "¿Qué *cantidad* necesitas?"]

    def ejecutar_accion_final(
        self, from_user: str, respuestas: Dict[str, str], grupo_id: Optional[str] = None
    ) -> str:
        """
        Genera cotización con cálculo automático.

        Args:
            from_user: Teléfono del usuario
            respuestas: Dict con respuestas capturadas
            grupo_id: GUID del grupo

        Returns:
            Mensaje con cotización
        """

        print(f"\n→ Generando cotización con handler D001...")

        # Obtener respuestas
        producto = respuestas.get(
            "¿Qué *producto* deseas cotizar?", "Producto genérico"
        )
        cantidad_str = respuestas.get("¿Qué *cantidad* necesitas?", "1")

        # Intentar convertir cantidad a número
        try:
            cantidad = int(cantidad_str)
        except ValueError:
            cantidad = 1

        print(f"  → Producto: {producto}")
        print(f"  → Cantidad: {cantidad}")

        # Simular consulta de precio (aquí conectarías con ERP/sistema de precios)
        precio_unitario = self._calcular_precio(producto)
        precio_total = precio_unitario * cantidad

        print(f"  → Precio unitario: ${precio_unitario:,.2f}")
        print(f"  → Precio total: ${precio_total:,.2f}")

        # Construir descripción para Dataverse
        descripcion = f"""
COTIZACIÓN AUTOMÁTICA

Producto: {producto}
Cantidad: {cantidad}
Precio Unitario: ${precio_unitario:,.2f}
Precio Total: ${precio_total:,.2f}

Teléfono: {from_user}

Generada automáticamente - Handler D001
        """.strip()

        # Crear registro de cotización
        try:
            ticket = self.crear_ticket(
                titulo=f"Cotización - {producto}",
                descripcion=descripcion,
                tipo="cotizacion",
                prioridad="Media",
                grupo_id=grupo_id,
                from_nombre="Cliente WhatsApp",
                telefono=from_user,
                empresa="",
            )

            ticket_id = ticket.get("cr321_ticketid", "XXXXX")
            print(f"  ✓ Cotización #{ticket_id} creada")

            # Mensaje de confirmación con detalles
            mensaje = f"""
💰 *Cotización Generada*

📦 *Producto:* {producto}
🔢 *Cantidad:* {cantidad}

💵 Precio unitario: ${precio_unitario:,.2f}
💵 *TOTAL:* ${precio_total:,.2f}

📋 Cotización #{ticket_id}

Un asesor te contactará pronto para confirmar disponibilidad y detalles de envío.

¡Gracias por tu interés! 🎉
            """.strip()

            return mensaje

        except Exception as e:
            print(f"  ❌ Error al crear cotización: {str(e)}")
            return f"⚠️ Error al generar cotización: {str(e)[:100]}"

    def _calcular_precio(self, producto: str) -> float:
        """
        Simula consulta de precio en sistema.
        En producción, esto consultaría un ERP o base de datos de precios.

        Args:
            producto: Nombre del producto

        Returns:
            Precio unitario
        """
        # Precios simulados
        productos_precio = {
            "laptop": 1500000,
            "computador": 1500000,
            "pc": 1200000,
            "monitor": 500000,
            "teclado": 80000,
            "mouse": 50000,
            "licencia": 200000,
            "software": 300000,
            "impresora": 800000,
            "scanner": 600000,
        }

        # Buscar por palabra clave
        producto_lower = producto.lower()
        for clave, precio in productos_precio.items():
            if clave in producto_lower:
                return precio

        # Precio por defecto si no se encuentra
        return 100000
