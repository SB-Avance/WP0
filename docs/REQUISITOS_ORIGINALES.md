# 📋 REQUISITOS ORIGINALES DEL PROYECTO

## 🎯 Objetivo Principal

Crear aplicación como experto en Python, WhatsApp API, y desarrollo de chatbots

**Stack Tecnológico:**
- WhatsApp API (múltiples conexiones)
- Microsoft Dataverse
- Python (Backend)
- Flet (Frontend)

---

## 🗂️ Tablas en Dataverse
### Tablas Principales

- ✅ **chats00** → `cr321_adatawp0` - Mensajes de WhatsApp
- ✅ **usuarios** → `cr321_usuarios` - Usuarios del sistema
- ✅ **grupos** → `cr321_grupos` - Grupos/Categorías
  - Campos: grupoid (consecutivo), nombre, tipo ("A", "B", "C"), descripcion
  - **Grupos tipo "A"** (Menú WhatsApp):
    1. Solicitud Ticket
    2. Cotización
    3. Información
    4. Solicitar atención de agente
- ✅ **chatbots** → `cr321_chatbots` - Configuración de bots
- ✅ **contacto** → `cr321_contacto` - Contactos
- ✅ **ticket** → `cr321_ticket` - Tickets de soporte
  - Campos: from_name (de chats00), id consecutivo
- ✅ **cotizacion** → `cr321_cotizacion` - Cotizaciones de clientes
  - Campos: nombre, cliente, descripcion, fecha
- ✅ **estados** → `cr321_estado` - Estados de tickets
- ✅ **usuario_grupo** → `cr321_usuariogrupo` - Relación usuarios-grupos
- ✅ **flujos** → `cr321_flows` - Flujos conversacionales
- ✅ **cuentas de whatsapp** → `cr321_cuentadewhatsapp` - Múltiples cuentas
- ✅ **templates** → `cr321_template` - Plantillas de mensajes

---

## 🎨 Diseño de Interfaz

### Menú de WhatsApp
- El menú debe cargar **dinámicamente** los elementos de la tabla `grupos` que sean tipo "A"

### Layout del Frontend

**Sidebar Izquierdo:**
- 👤 Botón para cambio de usuario
- 🔽 Cuadro combinado para los grupos
- ⚙️ Ajustes (vacía por ahora)
**Chatbot:** "Menú Principal WhatsApp"
- Debe crearse en la tabla `cr321_chatbots`
- Desde ajustes, permitir crear múltiples chatbots adicionales

### Opciones del Menú

**Opción 1: Solicitud Ticket**
- Pregunta 1: Nombre
- Pregunta 2: Empresa
- Pregunta 3: Describa solicitud de soporte
- Acción: Crear ticket en `cr321_ticket`

**Opción 2: Cotizaciones**
- Pregunta 1: Nombre
- Pregunta 2: Empresa
- Pregunta 3: Describa el producto, marca, y modelo si lo tiene
- Acción: Crear registro en `cr321_cotizacion`

**Opción 3: Información**
- Respuesta directa (sin preguntas)

**Opción 4: Solicitar atención de agente**
- Pregunta 1: Nombre
- Acción: Derivar a agente humano

---

## 🚀 Scripts de Inicio
**Usuario ROL "administrador":**
### Ejecución Local

```powershell
# Iniciar backend
.\iniciar_backend.ps1    # Flask en http://localhost:5000

# Iniciar frontend (modo LOCAL)
.\iniciar.ps1 LOCAL      # Frontend conecta a backend local

# Iniciar frontend (modo AZURE)
.\iniciar.ps1 AZURE      # Frontend conecta a Azure (sin backend local)
```

---

## ⚠️ IMPORTANTE: Scripts PowerShell

**NO usar caracteres especiales en archivos .ps1:**
- ❌ Evitar: Unicode checkmark, box-drawing, bullets
- ✅ Usar solo ASCII: `[OK]`, `[ERROR]`, `[WARN]`, `[AVISO]`
- ✅ Usar solo guiones y signos de igual para separadores
- 📝 Los archivos Markdown (.md) **SÍ** pueden usar emojis

---

## 🔗 Conexión Dataverse

**Cadena de conexión:** `https://org460b8a6c.crm2.dynamics.com`

Esta es la URL base para todas las operaciones con Dataverse:
- API REST: `https://org460b8a6c.crm2.dynamics.com/api/data/v9.2/`
- Región: South America (crm2)
- Configurada en: `.env` → `DATAVERSE_URL`

---

## ✅ Estado Actual (Febrero 2026)

**Todas las funcionalidades solicitadas han sido implementadas:**
- ✅ Múltiples conexiones WhatsApp
- ✅ Menú dinámico desde Dataverse
- ✅ Sistema de permisos por grupo
- ✅ Frontend con selector de grupos
- ✅ Scripts limpios (solo ASCII en .ps1)
- ✅ Chatbot principal creado automáticamente

**Ver implementación completa:** [MEJORAS_IMPLEMENTADAS.md](MEJORAS_IMPLEMENTADAS.md)
opcion	3. informacion 
opcion	4. Solicitar atencion de agente.

************************************
conservar para ejecutar locl o en azure lo siguiente :
iniciar_backend.ps1		Inicia Flask en http://localhost:5000
.\iniciar.ps1 LOCAL		Frontend conecta a backend local
.\iniciar.ps1 AZURE		Frontend conecta a Azure (sin backend local)

************************************
IMPORTANTE: NO USAR CARACTERES ESPECIALES EN SCRIPTS PS1
- Evitar caracteres Unicode como: checkmark, box-drawing, bullets
- Usar solo ASCII: [OK], [ERROR], [WARN], [AVISO]
- Usar solo guiones y signos de igual para separadores
- Archivos afectados: *.ps1 (PowerShell scripts)
- Archivos MD pueden usar emojis sin problema

es para cadena de conecion https://org460b8a6c.crm2.dynamics.com
