# 📋 BACKLOG DEL PROYECTO
## Sistema de Gestión de Requerimientos

**Última actualización:** 7 de febrero de 2026  
**Versión:** 1.0  

---

## 🎯 CÓMO USAR ESTE ARCHIVO

1. **Agregar Requerimiento:** Añade en la sección apropiada (Alta/Media/Baja prioridad)
2. **Formato:** Usa el template proporcionado
3. **Estados:** 📝 Pendiente | 🔄 En Progreso | ✅ Completado | ❌ Cancelado
4. **Actualizar:** Cambia estado cuando trabajes en un item

---

## 🔥 PRIORIDAD ALTA (Urgente - 0-2 semanas)

### REQ-001: Relaciones Lookup en Cotizaciones
- **Estado:** 📝 Pendiente
- **Fecha creación:** 2026-02-07
- **Descripción:** Agregar campos lookup en tabla cr321_cotizacion
  - `cr321_contactoId` → cr321_contacto (vincular con contacto)
  - `cr321_estadoId` → cr321_estado (seguimiento: Pendiente/Aprobada/Rechazada)
- **Beneficio:** Seguimiento completo de cotizaciones
- **Archivos a modificar:**
  - Script nuevo: `agregar_lookups_cotizacion.py`
  - API: `backend/api/cotizaciones.py`
- **Estimación:** 2 horas
- **Asignado a:** -
- **Notas:** Similar a lookups de tickets (cr321_ticket)

### REQ-002: Campo Asignado en Tickets
- **Estado:** 📝 Pendiente
- **Fecha creación:** 2026-02-07
- **Descripción:** Agregar `cr321_asignadoId` lookup en cr321_ticket → cr321_usuarios
- **Beneficio:** Asignar tickets a agentes específicos
- **Archivos a modificar:**
  - Script: `agregar_lookup_asignado.py`
  - API: `backend/api/tickets.py`
  - Frontend: `mobile/components/users.py`
- **Estimación:** 3 horas
- **Asignado a:** -
- **Dependencias:** Ninguna

### REQ-003: [AGREGAR NUEVO REQUERIMIENTO AQUÍ]
- **Estado:** 📝 Pendiente
- **Fecha creación:** YYYY-MM-DD
- **Descripción:** [Descripción detallada]
- **Beneficio:** [Qué problema resuelve]
- **Archivos a modificar:** [Lista de archivos]
- **Estimación:** [Horas/días]
- **Asignado a:** -
- **Dependencias:** [REQ-XXX si aplica]

---


## ⚠️ PRIORIDAD MEDIA (Importante - 2-4 semanas)

### REQ-004: Múltiples Conexiones WhatsApp
- **Estado:** 📝 Pendiente
- **Fecha creación:** 2026-02-07
- **Descripción:** Activar soporte para múltiples cuentas WhatsApp desde cr321_cuentadewhatsapp
- **Beneficio:** Escalar a múltiples líneas de atención
- **Archivos a modificar:**
  - `backend/goot.py` (selección dinámica de cuenta)
  - `backend/api/webhook.py` (webhook por cuenta)
  - Tabla: cr321_cuentadewhatsapp (agregar registros)
- **Estimación:** 8 horas
- **Asignado a:** -
- **Notas:** Infraestructura ya preparada, solo activar

### REQ-005: Persistencia de Conversaciones
- **Estado:** 📝 Pendiente
- **Fecha creación:** 2026-02-07
- **Descripción:** Mover estados de conversación de memoria a persistencia (Redis o Dataverse)
- **Beneficio:** No perder contexto al reiniciar backend
- **Archivos a modificar:**
  - `backend/api/webhook.py` línea 16 (conversation_states)
  - Opción A: Agregar Redis
  - Opción B: Crear tabla cr321_conversacion_activa
- **Estimación:** 6 horas
- **Asignado a:** -
- **Decisión técnica:** Pendiente (Redis vs Dataverse)

### REQ-006: Vincular Mensajes con Tickets/Cotizaciones
- **Estado:** 📝 Pendiente
- **Fecha creación:** 2026-02-07
- **Descripción:** Agregar lookups en cr321_adatawp0:
  - `cr321_ticketId` → cr321_ticket
  - `cr321_cotizacionId` → cr321_cotizacion
- **Beneficio:** Trazabilidad completa de conversaciones
- **Archivos a modificar:**
  - Script: `agregar_lookups_mensajes.py`
  - API: `backend/api/messages.py`
  - API: `backend/api/webhook.py` (guardar ID al crear)
- **Estimación:** 4 horas
- **Asignado a:** -

---

## 📌 PRIORIDAD BAJA (Opcional - 4+ semanas)

### REQ-007: Manejo de Errores Mejorado
- **Estado:** 📝 Pendiente
- **Fecha creación:** 2026-02-07
- **Descripción:** 
  - Try-catch en todos los endpoints
  - Logs estructurados (JSON)
  - Notificaciones de errores al frontend
- **Beneficio:** Debugging más fácil, mejor experiencia usuario
- **Archivos a modificar:** Todos los archivos en `backend/api/`
- **Estimación:** 12 horas
- **Asignado a:** -

### REQ-008: Búsqueda en Chats
- **Estado:** 📝 Pendiente
- **Fecha creación:** 2026-02-07
- **Descripción:** Barra de búsqueda por nombre/teléfono/empresa
- **Beneficio:** Encontrar conversaciones rápidamente
- **Archivos a modificar:**
  - `mobile/components/chats.py`
  - API: agregar parámetro $filter
- **Estimación:** 4 horas
- **Asignado a:** -

### REQ-009: Exportación de Reportes
- **Estado:** 📝 Pendiente
- **Fecha creación:** 2026-02-07
- **Descripción:** 
  - Exportar conversaciones a PDF/Excel
  - Estadísticas de tickets (dashboard)
  - Reportes de cotizaciones
- **Beneficio:** Análisis de datos y presentaciones
- **Archivos a modificar:**
  - Nuevo: `backend/api/reportes.py` (extender)
  - Nuevo: `mobile/components/reports.py`
- **Estimación:** 10 horas
- **Asignado a:** -
- **Dependencias:** Instalar librerías (reportlab, openpyxl)



---

## ✅ COMPLETADOS (Últimas 30 días)

### REQ-012: Documentación dependencias campos grupo usuarios
- **Estado:** ✅ Completado
- **Fecha completado:** 2026-02-07
- **Descripción:** Documentar por qué los campos cr321_1, cr321_3, cr321_4 no se pueden borrar de la tabla usuarios y cómo resolverlo
- **Problema:** Campos booleanos antiguos tienen dependencias activas en vistas, formularios, flujos de Power Automate
- **Archivos creados:**
  - `docs/DEPENDENCIAS_CAMPOS_GRUPO_USUARIOS.md` (guía completa - 650 líneas)
  - `docs/GUIA_RAPIDA_ELIMINAR_CAMPOS_GRUPO.md` (guía rápida - 150 líneas)
  - `docs/LISTADO_DEPENDENCIAS_CAMPOS_GRUPO.md` (listado detallado - 350 líneas)
  - `migrar_grupos_booleanos_a_relaciones.py` (script de migración - 350 líneas)
  - `ver_dependencias_campos.py` (script consulta rápida - 400 líneas) ⚡ NUEVO
  - `RESUMEN_DEPENDENCIAS.md` (resumen ejecutivo - 1 página)
- **Solución propuesta:**
  1. Ejecutar `python ver_dependencias_campos.py` para ver dependencias (2 min)
  2. Remover campos de vistas y formularios indicados
  3. Migrar datos a cr321_usuario_gruposes usando script automático
  4. Eliminar campos antiguos desde Power Apps
- **Herramientas creadas:**
  - ⚡ Script de consulta rápida (API directa a Dataverse)
  - 🔄 Script de migración automática de datos
  - 📚 3 guías de diferente nivel de detalle
- **Beneficio:** 
  - Limpieza de base de datos
  - Uso exclusivo del sistema nuevo (usuario_gruposes)
  - Eliminación de redundancia
  - Consulta de dependencias en 2 minutos vs 10-15 manual
- **Tiempo real:** 2 horas (documentación, scripts y herramientas)
- **Acción requerida:** Usuario debe ejecutar ver_dependencias_campos.py en su entorno

### REQ-011: Renombrar campo cr321_id a cr321_idusuario
- **Estado:** ✅ Completado (Código) ⏳ Pendiente (Dataverse)
- **Fecha completado:** 2026-02-07
- **Descripción:** Cambiar nombre del campo `cr321_id` en tabla usuarios a `cr321_idusuario` para mantener consistencia con otros campos consecutivos (cr321_idgrupo, cr321_idestado, cr321_idticket)
- **Archivos modificados:**
  - `backend/goot.py` (4 cambios - función create_user)
  - `backend/api/usuario_grupos.py` (2 cambios - función get_usuarios_by_grupo)
  - `docs/VERIFICACION_REQ010_USUARIO_GRUPOS.md` (actualizada)
  - `docs/GUIA_SISTEMA_CHATBOT.md` (actualizada)
  - `docs/MAPA_APLICACION.md` (actualizada)
- **Beneficio:** 
  - Mayor claridad en el código
  - Consistencia en nomenclatura
  - Diferenciación clara entre GUID (cr321_usuariosid) e ID consecutivo (cr321_idusuario)
- **Pendiente:** Aplicar cambio en Dataverse (Power Apps)
- **Documentación:** [CAMBIO_CAMPO_IDUSUARIO.md](CAMBIO_CAMPO_IDUSUARIO.md)
- **Tiempo real:** 30 minutos

### REQ-010: Verificacion uso grupos usuarios
- **Estado:** ✅ Completado
- **Fecha completado:** 2026-02-07
- **Descripción:** Verificar que los usuarios puedan pertenecer a uno o varios grupos de la tabla grup (el campo tipo tiene valores A, B, C) relacionado con la tabla usuarios campo id. Las relaciones se almacenan en usuariosgrupo.
- **Archivos verificados:**
  - `backend/api/usuario_grupos.py` (191 líneas - API completa)
  - `backend/api/grupos.py` (220 líneas - tipos A, B, C)
  - `backend/api/users.py` (gestión de usuarios)
  - Dataverse: cr321_usuario_gruposes (tabla de relaciones Many-to-Many)
- **Resultado de verificación:**
  - ✅ Usuarios pueden pertenecer a múltiples grupos
  - ✅ Tabla grup tiene campo tipo con valores A (462410000), B (462410001), C (462410002)
  - ✅ Relaciones almacenadas en cr321_usuario_gruposes
  - ✅ API REST completa: 5 endpoints implementados
  - ✅ Validaciones de duplicados funcionando
  - ✅ Lookups nativos de Dataverse configurados correctamente
- **Documentación:** [VERIFICACION_REQ010_USUARIO_GRUPOS.md](VERIFICACION_REQ010_USUARIO_GRUPOS.md)
- **Tiempo real:** 1 hora (verificación de código)

### REQ-DONE-001: Tabla Cotizaciones
- **Estado:** ✅ Completado
- **Fecha completado:** 2026-02-07
- **Descripción:** Crear tabla cr321_cotizacion con campos básicos
- **Archivos modificados:**
  - Dataverse: cr321_cotizacion (EntitySetName: cr321_cotizacions)
  - API: `backend/api/cotizaciones.py`
  - Backend: `backend/back.py` (blueprint)
  - Webhook: `backend/api/webhook.py` (función create_cotizacion_record)
  - Docs: Actualizados todos los archivos de documentación
- **Tiempo real:** 2 horas

### REQ-DONE-002: Migración a Nombres Singulares
- **Estado:** ✅ Completado
- **Fecha completado:** 2026-02-06
- **Descripción:** Migrar tablas plurales a singulares
  - cr321_grupos → cr321_grup
  - cr321_estados → cr321_estado
  - cr321_chatbots → cr321_chatbot
  - cr321_automatizaciones → cr321_automatizacion
- **Archivos modificados:** 20+ archivos Python actualizados
- **Tiempo real:** 4 horas

### REQ-DONE-003: Relaciones (Lookups) entre Tablas
- **Estado:** ✅ Completado
- **Fecha completado:** 2026-02-06
- **Descripción:** Crear 6 relaciones lookup:
  - ticket→grup, ticket→estado, ticket→contacto
  - usuariogrupo→usuarios, usuariogrupo→grup
  - flows→chatbot
- **Archivos modificados:**
  - `backend/api/tickets.py`
  - `backend/api/usuario_grupos.py`
- **Tiempo real:** 3 horas

---

## 📊 ESTADÍSTICAS

- **Total Requerimientos Activos:** 8
  - Alta Prioridad: 2
  - Media Prioridad: 3
  - Baja Prioridad: 3
- **Completados (último mes):** 6
- **Promedio estimación:** 5.6 horas por req
- **En progreso:** 0

---

## 📝 TEMPLATE PARA NUEVOS REQUERIMIENTOS

```markdown
### REQ-XXX: [Título del Requerimiento]
- **Estado:** 📝 Pendiente | 🔄 En Progreso | ✅ Completado | ❌ Cancelado
- **Fecha creación:** YYYY-MM-DD
- **Fecha completado:** YYYY-MM-DD (si aplica)
- **Descripción:** [Qué se necesita hacer]
- **Beneficio:** [Por qué es importante]
- **Archivos a modificar:** [Lista específica]
- **Estimación:** [Horas o días]
- **Asignado a:** [Nombre o - si no asignado]
- **Dependencias:** [REQ-XXX si depende de otro]
- **Notas:** [Información adicional]
```

---

## 🔄 PROCESO DE ACTUALIZACIÓN

1. **Al agregar requisito:**
   - Asignar número REQ-XXX
   - Clasificar por prioridad
   - Estimar tiempo
   - Describir archivos a modificar

2. **Al comenzar trabajo:**
   - Cambiar estado a 🔄 En Progreso
   - Agregar fecha de inicio
   - Asignar responsable

3. **Al completar:**
   - Cambiar estado a ✅ Completado
   - Agregar fecha de completado
   - Mover a sección COMPLETADOS
   - Registrar tiempo real
   - Listar archivos realmente modificados

4. **Sincronización:**
   - Actualizar ANALISIS_PROYECTO_COMPLETO.md si es cambio mayor
   - Actualizar REPORTE_FINAL_SISTEMA.md si afecta tablas/APIs
   - Actualizar REQUISITOS_ORIGINALES.md si cambia requisito base

---

## 🔗 REFERENCIAS

- **Requisitos Base:** [REQUISITOS_ORIGINALES.md](REQUISITOS_ORIGINALES.md)
- **Estado Sistema:** [ANALISIS_PROYECTO_COMPLETO.md](ANALISIS_PROYECTO_COMPLETO.md)
- **Reporte Técnico:** [REPORTE_FINAL_SISTEMA.md](REPORTE_FINAL_SISTEMA.md)
- **Documentación APIs:** `backend/api/README.md`

---

**Nota:** Este archivo debe actualizarse cada vez que se agregue, modifique o complete un requerimiento. Es el **único punto de verdad** para el backlog del proyecto.
