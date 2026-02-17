"""
GUÍA: DEPLOYMENT EN AZURE
=========================

El código está en GitHub pero Azure todavía tiene la versión vieja.

SOLUCIÓN 1: ESPERAR (Recomendado)
==================================
Azure tiene "Continuous Deployment" configurado desde GitHub.
- Tiempo típico: 5-15 minutos
- Verificación: Ejecuta cada 2-3 minutos:
  
  python verificar_azure_simple.py

SOLUCIÓN 2: REINICIO MANUAL EN AZURE PORTAL
===========================================

1. Ve a: https://portal.azure.com

2. Busca: "whatsapp-flask-app-f4gsb7dhhybcg6f6"

3. En el menú izquierdo:
   - Deployment Center → Ver logs de deployment
   - Verifica si el commit "566067d" está desplegado
   
4. Si NO está desplegado:
   - Opciones:
     a) Overview → Restart (botón arriba)
     b) Deployment Center → Sync (forzar pull desde GitHub)

5. Espera 2-3 minutos después del restart

6. Prueba: python verificar_azure_simple.py

VERIFICACIÓN EN WHATSAPP REAL
=============================

Después del deployment:
1. Abre WhatsApp y envía "menu" al número de WhatsApp Business
2. Deberías recibir:
   
   ¡Bienvenido! Por favor seleccione una opción:
   
   1. Informacion
      - Solicitar atención de agente
      - Pagina Web
   
   2. Soporte
      - Solicitud Ticket
      - Estado Ticket
      - Solicitar atención de agente
   
   3. Ventas
      - Cotizacion
      - Catalogo
      - Seguimiento

Si recibes el menú viejo (PERSONAS, EMPRESAS, COORDINACION) → Azure no actualizó

CAMBIOS REALIZADOS EN ESTE FIX
==============================

backend/back.py:
- Línea 16: Agregado "get_menu_text" al import
- Línea 225: Eliminado try/except con fallback hardcoded
- Ahora llama directamente a get_menu_text() desde api/webhook.py

backend/api/webhook.py:
- Línea 97-185: load_menu_from_dataverse() reescrito
- Ahora itera TODOS los chatbots activos (cr321_active=true)
- Cada chatbot.cr321_name = opción principal del menú
- Cada chatbot.cr321_elemento1-5 = sub-opciones

ESTADO DEL DEPLOYMENT
=====================

✅ Código local: CORREGIDO
✅ GitHub: ACTUALIZADO (commit 566067d)
⏳ Azure: PENDIENTE (esperando deployment automático)
⏳ WhatsApp: PENDIENTE (depende de Azure)

URL Backend Azure:
https://whatsapp-flask-app-f4gsb7dhhybcg6f6.eastus-01.azurewebsites.net

Repositorio GitHub:
https://github.com/SBApoyo/WP0/commits/main

"""

print(__doc__)
