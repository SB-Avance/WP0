# 📑 Índice de Documentación - Sistema Chatbot WhatsApp

> **Última actualización:** 8 de Febrero, 2026 | **Estado:** ✅ Sistema operacional

---

## 🚀 INICIO RÁPIDO

**Para empezar:** [INICIO_RAPIDO.md](INICIO_RAPIDO.md)
- Resumen de 5 minutos
- Próximos pasos inmediatos
- Ejemplos de uso

---

## 📚 Documentación Principal

### 1️⃣ Guías Esenciales

| Documento | Descripción | Cuándo Usar |
|-----------|-------------|-------------|
| **[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** | Guía de inicio express | Primer contacto con el sistema |
| **[GUIA_SISTEMA_CHATBOT.md](GUIA_SISTEMA_CHATBOT.md)** | Guía técnica completa | Referencia técnica detallada |
| **[GUIA_COMPLETA_CREAR_TABLAS_DATAVERSE.md](GUIA_COMPLETA_CREAR_TABLAS_DATAVERSE.md)** | 🆕 **Crear TODAS las 12 tablas** | **Configuración inicial de Dataverse** |
| **[GUIA_RAPIDA_CREAR_PROYECTO_COMPLETO.md](GUIA_RAPIDA_CREAR_PROYECTO_COMPLETO.md)** | Crear proyecto completo desde cero | Nuevo proyecto o replicar sistema |
| **[GUIA_RAPIDA_USUARIO_GRUPOS.md](GUIA_RAPIDA_USUARIO_GRUPOS.md)** | Gestión de usuarios y grupos | Configurar permisos |
| **[GUIA_CREAR_TABLAS_VISUAL.md](GUIA_CREAR_TABLAS_VISUAL.md)** | ~~Paso a paso para crear tablas~~ | ⚠️ Ver guía completa arriba |
| **[GUIA_TABLAS_ADICIONALES.md](GUIA_TABLAS_ADICIONALES.md)** | ~~Tablas complementarias~~ | ⚠️ Ver guía completa arriba |

### 2️⃣ Documentación Ejecutiva

| Documento | Descripción | Audiencia |
|-----------|-------------|-----------|
| **[RESUMEN_EJECUTIVO_MEJORAS_FEB2026.md](RESUMEN_EJECUTIVO_MEJORAS_FEB2026.md)** | 📊 Resumen ejecutivo actual | Gerentes, stakeholders |
| **[VALIDACION_SISTEMA_FEB2026.md](VALIDACION_SISTEMA_FEB2026.md)** | ✅ Validación completa del sistema | Todo el equipo |
| **[LIMPIEZA_WORKSPACE_FEB2026.md](LIMPIEZA_WORKSPACE_FEB2026.md)** | 🧹 Limpieza y organización del workspace | Mantenimiento, DevOps |
| **[RESUMEN_IMPLEMENTACION_FEB2024.md](RESUMEN_IMPLEMENTACION_FEB2024.md)** | Resumen de implementación | Referencia histórica |
| **[MEJORAS_IMPLEMENTADAS.md](MEJORAS_IMPLEMENTADAS.md)** | Mejoras completadas | Product owners |
| **[SUGERENCIAS_PROXIMOS_PASOS.md](SUGERENCIAS_PROXIMOS_PASOS.md)** | 🎯 Roadmap priorizado (6 mejoras pendientes) | Planificación |

### 2.1️⃣ APIs Mejoradas (Feb 2026)

| Documento | Descripción | Estado |
|-----------|-------------|--------|
| **[API_CHATS_EXTENDED.md](API_CHATS_EXTENDED.md)** | 🚀 Mejora #1: API con $expand (10x performance) | ✅ Completado |
| **[MEJORA_2_DASHBOARD_METRICAS.md](MEJORA_2_DASHBOARD_METRICAS.md)** | 📊 Mejora #2: Dashboard de Métricas | ⚠️ Parcial (3/5) |
| **[MEJORA_3_AUTO_CONTACTOS_LOOKUP.md](MEJORA_3_AUTO_CONTACTOS_LOOKUP.md)** | 🔗 Mejora #3: Auto-contactos con Lookup | ✅ Completado |

### 3️⃣ Documentación Técnica

| Documento | Descripción | Uso |
|-----------|-------------|-----|
| **[README.md](README.md)** | Documentación general del proyecto | Referencia general |
| **[MAPA_APLICACION.md](MAPA_APLICACION.md)** | 🗺️ Arquitectura + Diagramas | Entender estructura completa |
| **[GUIA_ENTORNOS.md](GUIA_ENTORNOS.md)** | Configuración de entornos | Desarrollo y producción |
| **[REQUISITOS_ORIGINALES.md](REQUISITOS_ORIGINALES.md)** | Requisitos del sistema | Contexto del proyecto |

---

## 🔧 Scripts y Herramientas

### Scripts Principales

| Script | Descripción | Comando |
|--------|-------------|---------|
| **init_dataverse.py** | Inicialización de Dataverse | `python init_dataverse.py` |
| **inicializar_sistema.py** | Inicialización completa del sistema | `python inicializar_sistema.py` |
| **asignar_categorias_chats.py** | Asignar categorías a chats | `python asignar_categorias_chats.py` |

### Scripts de Utilidad

| Script | Descripción | Comando |
|--------|-------------|---------|
| **iniciar.ps1** | Iniciar frontend | `.\iniciar.ps1` |
| **iniciar_backend.ps1** | Iniciar backend | `.\iniciar_backend.ps1` |
| **cambiar_entorno.ps1** | Cambiar entre LOCAL/AZURE | `.\cambiar_entorno.ps1 AZURE` |
| **sync.ps1** | Sincronizar con Git | `.\sync.ps1` |
| **crear_tablas_dataverse.ps1** | Guía para crear tablas | `.\crear_tablas_dataverse.ps1` |

### Tests (ubicados en /tests/)

| Test | Descripción | Comando |
|------|-------------|---------|
| **test_sistema.py** | Suite de pruebas completa | `python tests/test_sistema.py` |
| **test_chats_extended.py** | Tests de Mejora #1 | `python tests/test_chats_extended.py` |
| **test_dashboard.py** | Tests de Mejora #2 | `python tests/test_dashboard.py` |
| **test_webhook_enhanced.py** | Tests de Mejora #3 | `python tests/test_webhook_enhanced.py` |

> Ver [tests/README.md](../tests/README.md) para más detalles de los tests.

### Scripts Antiguos (ubicados en /scripts_antiguos/)

Scripts de migración y verificación históricos movidos a `/scripts_antiguos/` para mantener el workspace organizado.

> Ver [scripts_antiguos/README.md](../scripts_antiguos/README.md) para el listado completo.

---

## 📁 Estructura de Código

### Backend (Flask API)

```
backend/
├── back.py                    # Servidor principal
├── config.py                  # Configuración
├── goot.py                    # Variables de entorno
└── api/
    ├── auth.py                # Autenticación
    ├── users.py               # Usuarios
    ├── messages.py            # Mensajes
    ├── conversations.py       # Conversaciones
    ├── webhook.py             # Webhook + Menú interactivo
    ├── webhook_enhanced.py    # 🚀 MEJORA #3: Auto-contactos con Lookup
    ├── reportes.py            # Reportes
    ├── settings.py            # Configuración
    ├── grupos.py              # Gestión de grupos
    ├── estados.py             # Gestión de estados
    ├── tickets.py             # Gestión de tickets
    ├── usuario_grupos.py      # Relaciones usuario-grupos
    ├── chats_extended.py      # 🚀 MEJORA #1: API con $expand
    └── dashboard.py           # 🚀 MEJORA #2: Dashboard de métricas
```

### Frontend (Flet)

```
mobile/
├── main.py                    # Aplicación principal
├── config.py                  # Configuración API
├── assets/
│   └── styles.py              # Estilos
└── components/
    ├── login.py               # Login
    ├── dashboard.py           # Dashboard
    ├── chats.py               # Lista de chats
    ├── chat_detail.py         # Detalle de chat
    ├── users.py               # Gestión de usuarios
    ├── settings.py            # Configuración
    └── sidebar.py             # Menú lateral
```

### Tests

```
tests/
├── README.md                  # Documentación de tests
├── test_sistema.py            # Suite de pruebas completa
├── test_backend.py            # Tests del backend básico
├── test_chats_extended.py     # Tests Mejora #1
├── test_dashboard.py          # Tests Mejora #2
├── test_webhook_enhanced.py   # Tests Mejora #3
├── test_webhook_contacto.py   # Tests webhook contacto
└── test_campo_lookup.py       # Tests campos lookup
```

---

## 🎯 Flujos de Trabajo

### Para Desarrolladores

1. **Setup inicial:**
   - Leer: [README.md](README.md)
   - Configurar: [GUIA_ENTORNOS.md](GUIA_ENTORNOS.md)
   - Verificar: `python tests/test_sistema.py`

2. **Desarrollo:**
   - Referencia: [GUIA_SISTEMA_CHATBOT.md](GUIA_SISTEMA_CHATBOT.md)
   - Mejoras recientes: [RESUMEN_EJECUTIVO_MEJORAS_FEB2026.md](RESUMEN_EJECUTIVO_MEJORAS_FEB2026.md)
   - Pruebas: Ver [tests/README.md](../tests/README.md)

3. **Despliegue:**
   - Validación: [VALIDACION_SISTEMA_FEB2026.md](VALIDACION_SISTEMA_FEB2026.md)
   - Crear tablas: [GUIA_CREAR_TABLAS_VISUAL.md](GUIA_CREAR_TABLAS_VISUAL.md)
   - Inicializar: `python init_dataverse.py`

### Para Gerentes/Product Owners

1. **Entender el sistema:**
   - Leer: [RESUMEN_EJECUTIVO_MEJORAS_FEB2026.md](RESUMEN_EJECUTIVO_MEJORAS_FEB2026.md)
   - Inicio rápido: [INICIO_RAPIDO.md](INICIO_RAPIDO.md)

2. **Planificación:**
   - Roadmap: [SUGERENCIAS_PROXIMOS_PASOS.md](SUGERENCIAS_PROXIMOS_PASOS.md)
   - Mejoras sugeridas: [MEJORAS_SUGERIDAS.md](MEJORAS_SUGERIDAS.md)

3. **Validación:**
   - Resultados: [VALIDACION_SISTEMA_FEB2026.md](VALIDACION_SISTEMA_FEB2026.md)

### Para Soporte/QA

1. **Configuración:**
   - Crear tablas: [GUIA_CREAR_TABLAS_VISUAL.md](GUIA_CREAR_TABLAS_VISUAL.md)
   - Inicializar: `python init_dataverse.py`

2. **Pruebas:**
   - Suite completa: `python tests/test_sistema.py`
   - Tests específicos: Ver [tests/README.md](../tests/README.md)

3. **Troubleshooting:**
   - Guía técnica: [GUIA_SISTEMA_CHATBOT.md](GUIA_SISTEMA_CHATBOT.md)
   - Guía de entornos: [GUIA_ENTORNOS.md](GUIA_ENTORNOS.md)

---

## 📊 Resumen de Componentes

### ✅ Implementado y Operacional (Feb 2026)

| Componente | Estado | Documentación |
|------------|--------|---------------|
| Backend Flask | ✅ Funcional | [back.py](../backend/back.py) |
| API Grupos | ✅ Funcional | [grupos.py](../backend/api/grupos.py) |
| API Estados | ✅ Funcional | [estados.py](../backend/api/estados.py) |
| API Tickets | ✅ Funcional | [tickets.py](../backend/api/tickets.py) |
| API Usuario-Grupos | ✅ Funcional | [usuario_grupos.py](../backend/api/usuario_grupos.py) |
| Webhook WhatsApp | ✅ Funcional | [webhook.py](../backend/api/webhook.py) |
| **Mejora #1: API $expand** | ✅ Completado | [API_CHATS_EXTENDED.md](API_CHATS_EXTENDED.md) |
| **Mejora #2: Dashboard** | ⚠️ Parcial (3/5) | [MEJORA_2_DASHBOARD_METRICAS.md](MEJORA_2_DASHBOARD_METRICAS.md) |
| **Mejora #3: Auto-contactos** | ✅ Completado | [MEJORA_3_AUTO_CONTACTOS_LOOKUP.md](MEJORA_3_AUTO_CONTACTOS_LOOKUP.md) |
| Frontend Flet | ✅ Funcional | [main.py](../mobile/main.py) |

### 📈 Métricas Actuales

- **Código:** ~1,515 líneas nuevas (backend)
- **Tests:** 11/13 pasando (85%)
- **Performance:** 10x mejora (N+1 → 1 request)
- **Integridad:** 100% contactos asociados
- **Endpoints:** 59 rutas registradas (5 dashboard + 5 extended)

---

## 🔍 Búsqueda Rápida

### ¿Cómo...?

- **¿Cómo empezar?** → [INICIO_RAPIDO.md](INICIO_RAPIDO.md)
- **¿Cómo crear tablas?** → [GUIA_CREAR_TABLAS_VISUAL.md](GUIA_CREAR_TABLAS_VISUAL.md)
- **¿Cómo probar el sistema?** → `python tests/test_sistema.py`
- **¿Cómo inicializar datos?** → `python init_dataverse.py`
- **¿Cómo usar las APIs?** → [GUIA_SISTEMA_CHATBOT.md](GUIA_SISTEMA_CHATBOT.md)
- **¿Qué mejoras hay?** → [SUGERENCIAS_PROXIMOS_PASOS.md](SUGERENCIAS_PROXIMOS_PASOS.md)
- **¿Estado actual?** → [VALIDACION_SISTEMA_FEB2026.md](VALIDACION_SISTEMA_FEB2026.md)

### ¿Dónde está...?

- **Código de grupos** → [backend/api/grupos.py](../backend/api/grupos.py)
- **Código de tickets** → [backend/api/tickets.py](../backend/api/tickets.py)
- **Dashboard API** → [backend/api/dashboard.py](../backend/api/dashboard.py)
- **Menú WhatsApp** → [backend/api/webhook.py](../backend/api/webhook.py)
- **Frontend** → [mobile/main.py](../mobile/main.py)
- **Configuración** → [backend/config.py](../backend/config.py), [backend/goot.py](../backend/goot.py)
- **Tests** → `/tests/` (ver [tests/README.md](../tests/README.md))

---

## 📦 Archivos Históricos

Para mantener el workspace organizado, los siguientes archivos han sido archivados:

### 📂 docs/archive/

Documentación histórica (22 archivos) - Ver [archive/README.md](archive/README.md) para listado completo.

**Documentos archivados incluyen:**
- Reportes antiguos (REPORTE_*.md)
- Resúmenes previos (RESUMEN_*.md)
- Checklists históricos
- Guías de cambios específicos
- Estados y backlogs antiguos

### 📂 scripts_antiguos/

Scripts de migración y verificación (20 archivos) - Ver [../scripts_antiguos/README.md](../scripts_antiguos/README.md).

**Scripts archivados incluyen:**
- Scripts de análisis
- Scripts de migración (lookups, grupos, contactos)
- Scripts de verificación
- Utilidades de desarrollo

**Nota:** Estos archivos se conservan con fines de referencia histórica pero ya cumplieron su propósito.

---

## 📞 Soporte

### Recursos de Ayuda

1. **Documentación completa:** [GUIA_SISTEMA_CHATBOT.md](GUIA_SISTEMA_CHATBOT.md)
2. **Validación actual:** [VALIDACION_SISTEMA_FEB2026.md](VALIDACION_SISTEMA_FEB2026.md)
3. **Mejoras implementadas:** [RESUMEN_EJECUTIVO_MEJORAS_FEB2026.md](RESUMEN_EJECUTIVO_MEJORAS_FEB2026.md)

### Archivos de Referencia

- **Sincronización Git:** [../COMO_SINCRONIZAR_GIT.md](../COMO_SINCRONIZAR_GIT.md)
- **Próximos pasos:** [../PROXIMOS_PASOS_INMEDIATOS.md](../PROXIMOS_PASOS_INMEDIATOS.md)
- **Configuraciones:** `backend/goot.py`, `backend/config.py`

---

## 🎓 Aprendizaje

### Para Nuevos en el Proyecto

**Día 1:** [INICIO_RAPIDO.md](INICIO_RAPIDO.md) + [RESUMEN_EJECUTIVO_MEJORAS_FEB2026.md](RESUMEN_EJECUTIVO_MEJORAS_FEB2026.md)  
**Día 2:** [GUIA_SISTEMA_CHATBOT.md](GUIA_SISTEMA_CHATBOT.md)  
**Día 3:** Ejecutar tests y explorar código  
**Día 4:** Revisar [VALIDACION_SISTEMA_FEB2026.md](VALIDACION_SISTEMA_FEB2026.md)  
**Día 5:** [SUGERENCIAS_PROXIMOS_PASOS.md](SUGERENCIAS_PROXIMOS_PASOS.md) para roadmap

### Para Profundizar

1. Revisar código en [backend/api/](../backend/api/)
2. Estudiar mejoras en documentos MEJORA_*.md
3. Explorar frontend en [mobile/](../mobile/)
4. Revisar tests en [tests/](../tests/)

---

## ✅ Estado Actual

**Última actualización:** 8 de Febrero, 2026

**Estado del sistema:** ✅ **OPERACIONAL - LISTO PARA PRODUCCIÓN**

- ✅ 3 mejoras implementadas (2 completas, 1 parcial)
- ✅ 11/13 tests pasando (85%)
- ✅ Workspace organizado (limpieza Feb 2026)
- ✅ Backend funcionando en puerto 5000
- ✅ 29 chats disponibles para validación
- ⏳ Pendiente: Optimizar dashboard (2-3h)

**Mejoras completadas:**
- 🚀 Mejora #1: API con $expand - 10x performance ✅
- 📊 Mejora #2: Dashboard de métricas - 3/5 endpoints ⚠️
- 🔗 Mejora #3: Auto-contactos con Lookup ✅

**Siguiente paso:** Ver [SUGERENCIAS_PROXIMOS_PASOS.md](SUGERENCIAS_PROXIMOS_PASOS.md) para continuar con el roadmap (6 mejoras restantes).

---

**💡 Tip:** Para navegación rápida, usar Ctrl+F para buscar en este índice.
