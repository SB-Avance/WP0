"""
GUÍA DE MANTENIMIENTO DEL MENÚ DE WHATSAPP
==========================================

✅ SISTEMA ACTUAL - FUNCIONANDO
================================

Tu menú está 100% funcional y confiable con estas características:

📋 ESTRUCTURA:
--------------
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


🔧 CÓMO MODIFICAR EL MENÚ
==========================

Opción A: CAMBIAR TEXTOS DE UN CATEGORIA
-----------------------------------------
1. Ve a Power Apps (https://make.powerapps.com)
2. Abre la tabla: cr321_chatbots
3. Encuentra la fila (ej: "Ventas")
4. Edita los campos:
   - cr321_name: Nombre de la categoría
   - cr321_elemento1: Primera sub-opción
   - cr321_elemento2: Segunda sub-opción
   - etc.
5. Guarda
6. El menú se actualiza automáticamente en 5 minutos (cache)

Opción B: AGREGAR UNA NUEVA CATEGORÍA
--------------------------------------
1. Ve a Power Apps
2. Tabla: cr321_chatbots
3. Click "Nuevo registro"
4. Completa:
   - cr321_name: "Recursos Humanos"
   - cr321_active: true ✅
   - cr321_elemento1: "Consulta vacaciones"
   - cr321_elemento2: "Certificados"
   - etc.
5. Guarda
6. Aparecerá automáticamente como "4. Recursos Humanos"

Opción C: OCULTAR UNA CATEGORÍA
--------------------------------
1. Ve a Power Apps
2. Abre la fila que quieres ocultar
3. Cambia: cr321_active = false ❌
4. Guarda
5. Desaparecerá del menú automáticamente

Opción D: CAMBIAR EL ORDEN
---------------------------
Actualmente el orden es ALFABÉTICO (A-Z):
- Informacion (I)
- Soporte (S)
- Ventas (V)

Para cambiar el orden, renombra las categorías con prefijos:
- "1_Ventas" (aparecerá primero)
- "2_Soporte"
- "3_Informacion"

O implementa el campo cr321_orden (requiere desarrollo).


✅ VALIDACIONES IMPLEMENTADAS
==============================

El sistema ahora valida automáticamente:

1. ✅ Nombres no vacíos
   - Si cr321_name está vacío → Se omite esa categoría
   - Log: "[!] ADVERTENCIA: Chatbot X sin nombre, omitiendo"

2. ✅ Al menos 1 sub-opción
   - Si no hay cr321_elemento1-5 → Se omite esa categoría
   - Log: "[!] ADVERTENCIA: Ventas sin sub-opciones, omitiendo"

3. ✅ Máximo 10 sub-opciones
   - Si hay más de 10 → Usa solo las primeras 10
   - Log: "[!] ADVERTENCIA: Ventas tiene 12 sub-opciones, usando solo las primeras 10"

4. ✅ Limpieza de espacios
   - Espacios al inicio/final eliminados automáticamente
   - Elementos vacíos filtrados

5. ✅ Cache automático
   - Menú se carga cada 5 minutos
   - No necesitas reiniciar nada


🚀 DEPLOYMENT Y SINCRONIZACIÓN
===============================

Para que los cambios aparezcan en WhatsApp:

1. LOCAL (desarrollo):
   - Cambios en Dataverse → Reinicia backend
   - O espera 5 minutos (cache refresh)

2. AZURE (producción):
   - Cambios en código → git push → Azure deployment automático
   - Cambios en Dataverse → Efecto inmediato (5 min cache)


📊 MONITOREO Y DEBUGGING
=========================

Ver logs del menú:
------------------
Busca en los logs del backend:

[WEBHOOK] Construyendo menú desde 3 chatbots activos:
  [1] Informacion - 2 sub-opciones
      1. Solicitar atención de agente
      2. Pagina Web
  [2] Soporte - 3 sub-opciones
      1. Solicitud Ticket
      2. Estado Ticket
      3. Solicitar atención de agente
  [3] Ventas - 3 sub-opciones
      1. Cotizacion
      2. Catalogo
      3. Seguimiento
[WEBHOOK] Menú cargado exitosamente: 3 opciones principales

Si ves advertencias:
--------------------
[!] ADVERTENCIA: Chatbot 2 sin nombre, omitiendo
→ Revisa que cr321_name no esté vacío

[!] ADVERTENCIA: Ventas sin sub-opciones, omitiendo
→ Agrega al menos un cr321_elemento1

[!] ADVERTENCIA: Soporte tiene 12 sub-opciones, usando solo las primeras 10
→ Reduce a máximo 10 opciones o divide en 2 categorías


🧪 PRUEBAS ANTES DE PRODUCCIÓN
===============================

1. Probar localmente:
   python simular_whatsapp_menu.py

2. Ver menú actual:
   python verificar_y_corregir_chatbots.py

3. Verificar Azure:
   python verificar_azure_simple.py

4. Probar en WhatsApp real:
   Enviar "menu" al número de WhatsApp Business


📋 CHECKLIST DE MANTENIMIENTO
==============================

Antes de cambiar el menú:
□ Backup de la configuración actual (export Excel desde Power Apps)
□ Verificar que cr321_active = true en las categorías que quieres mostrar
□ Verificar que cada categoría tenga al menos 1 sub-opción
□ Máximo 10 sub-opciones por categoría
□ Nombres claros y sin caracteres especiales

Después de cambiar:
□ Verificar logs del backend [WEBHOOK]
□ Probar con simular_whatsapp_menu.py
□ Verificar en WhatsApp de prueba
□ Monitorear por 24h por errores


⚡ OPTIMIZACIONES FUTURAS (OPCIONALES)
======================================

Si necesitas más flexibilidad:

1. Agregar campo cr321_orden (number)
   - Control manual del orden
   - Ejemplo: Ventas=1, Informacion=2, Soporte=3

2. Agregar más campos elemento6-10
   - Hasta 10 sub-opciones por categoría
   - Requiere modificar webhook.py

3. Agregar horarios
   - cr321_horario_inicio, cr321_horario_fin
   - Mostrar/ocultar según hora del día

4. Agregar estadísticas
   - cr321_contador_uso
   - Dashboard de opciones más usadas


💡 CONTACTO Y SOPORTE
=====================

Si algo no funciona:
1. Revisa logs del backend [WEBHOOK]
2. Ejecuta: python verificar_y_corregir_chatbots.py
3. Verifica Azure: python verificar_azure_simple.py

Archivos clave:
- backend/api/webhook.py (líneas 97-185) - Carga del menú
- backend/back.py (línea 225) - Envío del menú
- cr321_chatbots (Dataverse) - Configuración del menú

"""

print(__doc__)
