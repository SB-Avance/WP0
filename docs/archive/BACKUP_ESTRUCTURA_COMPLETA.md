# 🗄️ BACKUP ESTRUCTURA COMPLETA - WhatsApp CRM

**Versión:** 2.0  
**Fecha:** Febrero 7, 2026  
**Propósito:** Documento maestro para recrear TODO el sistema desde cero

---

## 📊 Información General

**Dataverse URL:** `https://org460b8a6c.crm2.dynamics.com`  
**Región:** South America (crm2)  
**API Version:** v9.2  
**Prefijo Publisher:** `cr321_`

---

## 🗂️ Listado Completo de Tablas (12 tablas)

### 1. cr321_adatawp0 (Chats WhatsApp)
**Propósito:** Almacenar mensajes de WhatsApp entrantes y salientes

| Campo | Tipo | Longitud | Obligatorio | Descripción |
|-------|------|----------|-------------|-------------|
| cr321_adatawp0id | GUID | - | ✅ | Primary Key |
| cr321_name | Texto | 100 | ✅ | Nombre (campo principal) |
| cr321_from | Texto | 50 | ✅ | Número teléfono origen |
| cr321_body | Texto multilínea | 5000 | ❌ | Contenido mensaje |
| cr321_timestamp | Fecha y hora | - | ✅ | Marca temporal |
| cr321_messageid | Texto | 100 | ❌ | ID mensaje WhatsApp |
| cr321_type | Opciones | - | ✅ | Tipo mensaje (texto/imagen/audio) |
| cr321_direction | Opciones | - | ✅ | Dirección (entrante/saliente) |
| cr321_grupo | Número entero | - | ❌ | Grupo asignado (1,2,3) |

**Valores de opciones:**
- **cr321_type:** 462410000=Texto, 462410001=Imagen, 462410002=Audio, 462410003=Video, 462410004=Documento
- **cr321_direction:** 462410000=Entrante, 462410001=Saliente

---

### 2. cr321_usuarios (Usuarios)
**Propósito:** Usuarios del sistema CRM

| Campo | Tipo | Longitud | Obligatorio | Descripción |
|-------|------|----------|-------------|-------------|
| cr321_usuariosid | GUID | - | ✅ | Primary Key |
| cr321_nombre | Texto | 100 | ✅ | Nombre completo (campo principal) |
| cr321_correo | Texto | 100 | ✅ | Email (único) |
| cr321_clave | Texto | 255 | ✅ | Contraseña hash |
| cr321_rol | Opciones | - | ✅ | Rol (usuario/admin) |
| cr321_activo | Sí/No | - | ✅ | Usuario activo |

**Valores de opciones:**
- **cr321_rol:** 462410000=Usuario (default), 462410001=Administrador

---

### 3. cr321_grup (Grupos)
**Propósito:** Categorización de chats y usuarios. Tipo A = Menú WhatsApp

| Campo | Tipo | Longitud | Obligatorio | Descripción |
|-------|------|----------|-------------|-------------|
| cr321_grupoid | GUID | - | ✅ | Primary Key |
| cr321_idgrupo | Número entero | - | ✅ | ID consecutivo |
| cr321_nombre | Texto | 100 | ✅ | Nombre (campo principal) |
| cr321_tipo | Opciones | - | ✅ | Tipo grupo (A/B/C) |
| cr321_descripcion | Texto multilínea | 2000 | ❌ | Descripción |

**Valores de opciones:**
- **cr321_tipo:** 462410000=Tipo A (Menú WhatsApp), 462410001=Tipo B, 462410002=Tipo C

**⚠️ Datos iniciales obligatorios (Tipo A):**
1. ID=1, Nombre="Solicitud Ticket", Tipo=A
2. ID=2, Nombre="Cotizaciones", Tipo=A
3. ID=3, Nombre="Información", Tipo=A
4. ID=4, Nombre="Solicitar atención de agente", Tipo=A

---

### 4. cr321_estado (Estados)
**Propósito:** Estados para tickets

| Campo | Tipo | Longitud | Obligatorio | Descripción |
|-------|------|----------|-------------|-------------|
| cr321_estadoid | GUID | - | ✅ | Primary Key |
| cr321_idestado | Número entero | - | ✅ | ID consecutivo |
| cr321_nombre | Texto | 100 | ✅ | Nombre (campo principal) |
| cr321_descripcion | Texto multilínea | 500 | ❌ | Descripción |

**Datos iniciales recomendados:**
1. ID=1, Nombre="Nuevo"
2. ID=2, Nombre="En Proceso"
3. ID=3, Nombre="Pendiente Cliente"
4. ID=4, Nombre="Resuelto"
5. ID=5, Nombre="Cerrado"

---

### 5. cr321_contacto (Contactos)
**Propósito:** Información de contactos de clientes

| Campo | Tipo | Longitud | Obligatorio | Descripción |
|-------|------|----------|-------------|-------------|
| cr321_contactoid | GUID | - | ✅ | Primary Key |
| cr321_nombre | Texto | 100 | ✅ | Nombre (campo principal) |
| cr321_telefono | Texto | 50 | ✅ | Teléfono |
| cr321_email | Texto | 100 | ❌ | Email |
| cr321_empresa | Texto | 200 | ❌ | Empresa |

---

### 6. cr321_ticket (Tickets)
**Propósito:** Tickets de soporte y solicitudes

| Campo | Tipo | Longitud | Obligatorio | Descripción |
|-------|------|----------|-------------|-------------|
| cr321_ticketid | GUID | - | ✅ | Primary Key |
| cr321_idticket | Número entero | - | ✅ | ID consecutivo (campo principal) |
| cr321_fromnombre | Texto | 100 | ✅ | Nombre solicitante |
| cr321_telefono | Texto | 50 | ✅ | Teléfono |
| cr321_empresa | Texto | 200 | ❌ | Empresa |
| cr321_descripcion | Texto multilínea | 5000 | ✅ | Descripción solicitud |
| cr321_tipo | Opciones | - | ✅ | Tipo ticket |
| cr321_grupoId | Lookup | → cr321_grup | ❌ | Grupo asignado |
| cr321_estadoId | Lookup | → cr321_estado | ❌ | Estado actual |
| cr321_contactoId | Lookup | → cr321_contacto | ❌ | Contacto relacionado |
| cr321_fechacreacion | Fecha y hora | - | ✅ | Fecha creación |
| cr321_fechaactualizacion | Fecha y hora | - | ✅ | Última actualización |

**Valores de opciones:**
- **cr321_tipo:** 462410000=Soporte, 462410001=Cotización, 462410002=Información, 462410003=Atención Agente

**Relaciones:**
- N:1 con cr321_grup (campo: cr321_grupoId)
- N:1 con cr321_estado (campo: cr321_estadoid)
- N:1 con cr321_contacto (campo: cr321_contactoid)

---

### 7. cr321_usuariogrupo (Usuario-Grupo)
**Propósito:** Relación muchos a muchos entre usuarios y grupos

| Campo | Tipo | Longitud | Obligatorio | Descripción |
|-------|------|----------|-------------|-------------|
| cr321_usuariogrupoid | GUID | - | ✅ | Primary Key |
| cr321_name | Texto | 100 | ✅ | Nombre (campo principal) |
| cr321_usuarioid | Búsqueda | → cr321_usuarios | ✅ | Usuario |
| cr321_grupoid | Búsqueda | → cr321_grup | ✅ | Grupo |

**Relaciones:**
- N:1 con cr321_usuarios (campo: cr321_usuarioid)
- N:1 con cr321_grup (campo: cr321_grupoid)

---

### 8. cr321_chatbot (Chatbots)
**Propósito:** Configuración de chatbots

| Campo | Tipo | Longitud | Obligatorio | Descripción |
|-------|------|----------|-------------|-------------|
| cr321_chatbotid | GUID | - | ✅ | Primary Key |
| cr321_name | Texto | 100 | ✅ | Nombre (campo principal) |
| cr321_type | Opciones | - | ✅ | Tipo chatbot |
| cr321_config | Texto multilínea | 100000 | ❌ | Configuración JSON |
| cr321_active | Sí/No | - | ✅ | Activo (default=Sí) |

**Valores de opciones:**
- **cr321_type:** 462410000=FlowBot (default), 462410001=Simple, 462410002=AI Assistant

**⚠️ Chatbot inicial obligatorio:**
- Nombre: "Menu Principal WhatsApp"
- Tipo: FlowBot (462410000)
- Activo: Sí
- Config: `{"menu_dinamico": true, "fuente": "cr321_grup", "tipo_grupo": "A"}`

---

### 9. cr321_flows (Flujos)
**Propósito:** Flujos conversacionales para chatbots

| Campo | Tipo | Longitud | Obligatorio | Descripción |
|-------|------|----------|-------------|-------------|
| cr321_flowid | GUID | - | ✅ | Primary Key |
| cr321_nombre | Texto | 100 | ✅ | Nombre (campo principal) |
| cr321_chatbotid | Búsqueda | → cr321_chatbot | ✅ | Chatbot asociado |
| cr321_nodos | Texto multilínea | 100000 | ❌ | Nodos JSON |
| cr321_edges | Texto multilínea | 100000 | ❌ | Conexiones JSON |
| cr321_version | Número entero | - | ✅ | Versión (default=1) |

**Relaciones:**
- N:1 con cr321_chatbot (campo: cr321_chatbotid)

---

### 10. cr321_automatizacion (Automatizaciones)
**Propósito:** Reglas de automatización

| Campo | Tipo | Longitud | Obligatorio | Descripción |
|-------|------|----------|-------------|-------------|
| cr321_automatizacionid | GUID | - | ✅ | Primary Key |
| cr321_nombre | Texto | 100 | ✅ | Nombre (campo principal) |
| cr321_trigger | Opciones | - | ✅ | Evento disparador |
| cr321_condiciones | Texto multilínea | 10000 | ❌ | Condiciones JSON |
| cr321_acciones | Texto multilínea | 10000 | ❌ | Acciones JSON |
| cr321_activo | Sí/No | - | ✅ | Activa (default=Sí) |

**Valores de opciones:**
- **cr321_trigger:** 462410000=Mensaje Recibido, 462410001=Palabra Clave, 462410002=Horario, 462410003=Evento Sistema

---

### 11. cr321_template (Templates)
**Propósito:** Plantillas de mensajes WhatsApp

| Campo | Tipo | Longitud | Obligatorio | Descripción |
|-------|------|----------|-------------|-------------|
| cr321_templateid | GUID | - | ✅ | Primary Key |
| cr321_nombre | Texto | 100 | ✅ | Nombre (campo principal) |
| cr321_contenido | Texto multilínea | 5000 | ✅ | Contenido plantilla |
| cr321_categoria | Opciones | - | ✅ | Categoría |
| cr321_idioma | Texto | 10 | ✅ | Idioma (default="es") |
| cr321_aprobado | Sí/No | - | ✅ | Aprobada Meta (default=No) |

**Valores de opciones:**
- **cr321_categoria:** 462410000=Marketing, 462410001=Servicio, 462410002=Ventas, 462410003=Soporte

---

### 12. cr321_cuentadewhatsapp (Cuentas WhatsApp)
**Propósito:** Múltiples cuentas de WhatsApp Business

| Campo | Tipo | Longitud | Obligatorio | Descripción |
|-------|------|----------|-------------|-------------|
| cr321_cuentadewhatsappid | GUID | - | ✅ | Primary Key |
| cr321_name | Texto | 100 | ✅ | Nombre (campo principal) |
| cr321_phonenumberid | Texto | 50 | ✅ | Phone Number ID Meta |
| cr321_accesstoken | Texto | 500 | ✅ | Access Token Meta |
| cr321_verifytoken | Texto | 100 | ❌ | Verify Token webhook |
| cr321_activo | Sí/No | - | ✅ | Activa (default=Sí) |

---

## 📋 Orden de Creación Recomendado

**IMPORTANTE:** Crear en este orden para evitar errores de dependencias:

1. ✅ **cr321_usuarios** (independiente)
2. ✅ **cr321_grup** (independiente) → Luego ejecutar `inicializar_sistema.py`
3. ✅ **cr321_estado** (independiente)
4. ✅ **cr321_contacto** (independiente)
5. ✅ **cr321_cuentadewhatsapp** (independiente)
6. ✅ **cr321_chatbot** (independiente)
7. ✅ **cr321_automatizacion** (independiente)
8. ✅ **cr321_template** (independiente)
9. ✅ **cr321_usuariogrupo** (depende de #1 y #2)
10. ✅ **cr321_flows** (depende de #6)
11. ✅ **cr321_ticket** (depende de #2, #3, #4)
12. ✅ **cr321_adatawp0** (último)

---

## 🚀 Scripts de Inicialización

### Script: inicializar_sistema.py

**Ejecutar DESPUÉS de crear todas las tablas:**

```powershell
# Activar entorno
.\venv_clean\Scripts\Activate.ps1

# Ejecutar inicialización (solo una vez)
python inicializar_sistema.py
```

**Qué hace:**
- ✅ Crea 4 grupos tipo A (menú WhatsApp)
- ✅ Crea chatbot "Menu Principal WhatsApp"
- ✅ Verifica duplicados antes de crear

---

## 🔑 Valores Importantes de Opciones

**Todos los conjuntos de opciones inician en:** `462410000`

### Patrón de Valores:
- Primera opción: `462410000`
- Segunda opción: `462410001`
- Tercera opción: `462410002`
- Y así sucesivamente...

### Grupos Tipo A (Menú WhatsApp):
- **CRÍTICO:** Solo los grupos con `cr321_tipo = 462410000` aparecen en el menú de WhatsApp
- El webhook carga estas opciones dinámicamente cada 5 minutos

---

## 📦 Archivos de Respaldo

1. **BACKUP_ESTRUCTURA_COMPLETA.json** - Estructura completa en JSON
2. **BACKUP_ESTRUCTURA_COMPLETA.md** - Este documento (legible)
3. **tablas_dataverse.json** - Definición tablas principales
4. **REQUISITOS_ORIGINALES.md** - Requisitos del proyecto

---

## 🔧 Configuración de Aplicación

### Backend (Flask - Python)
```bash
# Iniciar backend
.\iniciar_backend.ps1

# Escucha en: http://localhost:5000
```

**Endpoints principales:**
- `/api/whatsapp-accounts` - Gestión cuentas WhatsApp
- `/api/grupos` - Gestión grupos
- `/api/chatbots` - Gestión chatbots
- `/api/tickets` - Gestión tickets
- `/api/users` - Gestión usuarios
- `/api/usuario-grupos` - Relaciones usuario-grupo
- `/webhook` - Recepción mensajes WhatsApp

### Frontend (Flet - Python)
```bash
# Modo LOCAL (con backend local)
.\iniciar.ps1 LOCAL

# Modo AZURE (backend en Azure)
.\iniciar.ps1 AZURE
```

**Puerto:** 8501

---

## ⚠️ Notas Críticas

1. **Prefijo obligatorio:** Todos los nombres de tablas y campos deben usar `cr321_`
2. **Campos principales:** Determinan qué se muestra en listas
3. **Relaciones de búsqueda:** Crean campos automáticos con sufijo `_value`
4. **GUID:** Auto-generados por Dataverse, no crear manualmente
5. **Timestamps:** Siempre en UTC formato ISO 8601
6. **Grupos Tipo A:** Solo estos aparecen en menú WhatsApp
7. **Webhook:** Debe configurarse en Meta Developer Console
8. **Tokens:** Access Token debe renovarse periódicamente

---

## 📞 Proceso Completo de Recreación

### Paso 1: Crear Tablas en Dataverse
```
1. Ir a make.powerapps.com
2. Seleccionar entorno (org460b8a6c.crm2.dynamics.com)
3. Dataverse → Tablas → Nueva tabla
4. Crear las 12 tablas en el orden recomendado
5. Agregar campos según especificaciones
6. Configurar relaciones de búsqueda
```

### Paso 2: Inicializar Datos
```powershell
python inicializar_sistema.py
```

### Paso 3: Configurar Backend
```bash
# Crear/verificar archivo .env con:
CLIENT_ID=...
CLIENT_SECRET=...
TENANT_ID=...
DATAVERSE_URL=https://org460b8a6c.crm2.dynamics.com
PHONE_NUMBER_ID=...
ACCESS_TOKEN=...
VERIFY_TOKEN=...
```

### Paso 4: Iniciar Sistema
```powershell
# Terminal 1: Backend
.\iniciar_backend.ps1

# Terminal 2: Frontend
.\iniciar.ps1 LOCAL
```

### Paso 5: Crear Usuario Administrador
```
1. Abrir frontend
2. Ir a Login
3. Registrar primer usuario (será admin)
4. Asignar grupos necesarios
```

### Paso 6: Configurar Webhook
```
1. Meta Developer Console
2. WhatsApp → Configuration
3. Callback URL: https://tu-dominio.com/webhook
4. Verify Token: (valor de .env)
5. Subscribe to: messages
```

---

## ✅ Checklist Post-Recreación

- [ ] 12 tablas creadas en Dataverse
- [ ] Grupos tipo A creados (4 registros)
- [ ] Chatbot principal creado
- [ ] Backend inicia sin errores
- [ ] Frontend conecta correctamente
- [ ] Login funciona
- [ ] Webhook configurado en Meta
- [ ] Mensajes WhatsApp se reciben
- [ ] Menú dinámico carga desde Dataverse
- [ ] Tickets se crean correctamente

---

**Documento creado:** Febrero 7, 2026  
**Versión:** 2.0  
**Mantenido por:** Sistema WhatsApp CRM
