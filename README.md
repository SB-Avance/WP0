# 📱 Sistema de Chatbot WhatsApp - CRM/ERP

Sistema completo de gestión de conversaciones de WhatsApp Business con chatbot interactivo, sistema de tickets y gestión de grupos, integrado con Microsoft Dataverse.

## 🎯 Características Principales

- ✅ **Múltiples conexiones WhatsApp** simultáneas
- ✅ **Sistema de menú interactivo** para WhatsApp (4 opciones)
- ✅ **Gestión de tickets** desde conversaciones
- ✅ **Grupos de categorización** con permisos por rol
- ✅ **Frontend responsive** para móvil y desktop
- ✅ **Roles y permisos** (Administrador/Usuario)
- ✅ **API REST completa** para todas las entidades

## 📚 Documentación

Toda la documentación del proyecto se encuentra en la carpeta [`docs/`](docs/):

- **[INICIO_RAPIDO.md](docs/INICIO_RAPIDO.md)** - Guía de inicio rápido
- **[GUIA_COMPLETA_CREAR_TABLAS_DATAVERSE.md](docs/GUIA_COMPLETA_CREAR_TABLAS_DATAVERSE.md)** - 🆕 Crear todas las 12 tablas en Dataverse
- **[GUIA_RAPIDA_CREAR_PROYECTO_COMPLETO.md](docs/GUIA_RAPIDA_CREAR_PROYECTO_COMPLETO.md)** - Crear proyecto completo desde cero
- **[INDICE_DOCUMENTACION.md](docs/INDICE_DOCUMENTACION.md)** - Índice completo de documentación
- **[ASIGNAR_PERMISOS.md](docs/ASIGNAR_PERMISOS.md)** - Configuración de permisos en Dataverse
- **[ESTADO_REAL_PROYECTO.md](docs/ESTADO_REAL_PROYECTO.md)** - Estado actual del proyecto
- **[tablas_adicionales.json](docs/tablas_adicionales.json)** - Referencia de estructura de tablas
- **[VERIFICAR_PERMISOS_README.md](docs/VERIFICAR_PERMISOS_README.md)** - Guía del script de verificación

Ver la [documentación completa](docs/) para más detalles.

## 🏗️ Arquitectura

- **Backend**: Flask + Microsoft Graph API (WhatsApp Business)
- **Frontend**: Flet (Python GUI multiplataforma)
- **Base de datos**: Microsoft Dataverse (CRM)
- **Autenticación**: Microsoft MSAL + JWT
- **Webhook**: WhatsApp Business API

## 📁 Estructura del Proyecto

```
BIN/
├── backend/                    # Servidor Flask principal
│   ├── back.py                # Servidor principal con webhook y API REST
│   ├── config.py              # Configuración global
│   ├── goot.py                # Variables de entorno y funciones auxiliares
│   └── api/                   # Módulos API organizados por funcionalidad
│       ├── auth.py            # Autenticación de usuarios
│       ├── conversations.py   # Gestión de conversaciones
│       ├── messages.py        # Envío y recepción de mensajes
│       ├── users.py           # Administración de usuarios
│       ├── webhook.py         # Webhook de WhatsApp + Menú interactivo
│       ├── reportes.py        # Reportes y estadísticas
│       ├── settings.py        # Configuración de la app
│       ├── grupos.py          # ⭐ NUEVO: Gestión de grupos
│       ├── estados.py         # ⭐ NUEVO: Estados de tickets
│       ├── tickets.py         # ⭐ NUEVO: Sistema de tickets
│       └── usuario_grupos.py  # ⭐ NUEVO: Relaciones usuario-grupo
│
├── mobile/                     # Aplicación GUI con Flet
│   ├── main.py                # Punto de entrada de la app
│   ├── config.py              # Configuración de API URL
│   ├── assets/                # Estilos e iconos
│   └── components/            # Componentes UI
│       ├── login.py           # Pantalla de login
│       ├── dashboard.py       # Dashboard principal
│       ├── chats.py           # Lista de conversaciones con filtro de grupos
│       ├── chat_detail.py     # Detalle de conversación
│       ├── users.py           # Gestión de usuarios
│       ├── settings.py        # Configuración
│       └── sidebar.py         # Menú lateral
│
├── init_dataverse.py           # ⭐ NUEVO: Script inicialización de datos
├── crear_tablas_dataverse.ps1 # ⭐ NUEVO: Guía crear tablas
├── GUIA_SISTEMA_CHATBOT.md     # ⭐ NUEVO: Documentación completa
├── iniciar.ps1                 # Script de inicio automático
├── iniciar_backend.ps1         # Iniciar solo backend
├── requirements.txt            # Dependencias del proyecto
└── .env                        # Variables de entorno (no incluido en repo)
```

## 🚀 Inicio Rápido

### ✅ Primera vez - Configuración inicial

#### 1. Crear tablas en Dataverse
Ver guía completa: [GUIA_COMPLETA_CREAR_TABLAS_DATAVERSE.md](docs/GUIA_COMPLETA_CREAR_TABLAS_DATAVERSE.md)

**12 tablas necesarias:**
- `cr321_usuarios`, `cr321_grupos`, `cr321_estados`, `cr321_contacto`
- `cr321_cuentadewhatsapp`, `cr321_chatbot`, `cr321_template`
- `cr321_automatizaciones`, `cr321_usuariogrupo`, `cr321_flows`
- `cr321_ticket`, `cr321_adatawp0` (mensajes)

#### 2. Inicializar datos base
```powershell
python init_dataverse.py
```
Esto crea:
- 4 grupos tipo A (opciones del menú WhatsApp)
- 6 estados de tickets

#### 3. Asignar usuarios a grupos
```powershell
# Usar API o Postman
POST http://localhost:5000/api/usuario-grupos
{
  "usuario_id": "guid-del-usuario",
  "grupo_id": "guid-del-grupo"
}
```

### ✅ Uso normal (día a día)

#### Opción A: Backend en Azure (Recomendado)
El backend YA está corriendo en Azure App Services 24/7. Solo inicia el frontend:

```powershell
.\iniciar.ps1
```

#### Opción B: Todo local (Desarrollo)
```powershell
# Terminal 1 - Backend LOCAL
cd backend
python back.py

# Terminal 2 - Frontend
$env:ENVIRONMENT = "LOCAL"
cd mobile
python main.py
```

## 🌐 Configuración de Entorno

### Arquitectura de Despliegue
- **Backend**: Azure App Services (producción 24/7)
  - URL: `https://whatsapp-flask-app-f4gsb7dhhybcg6f6.eastus-01.azurewebsites.net`
  - Despliegue automático desde GitHub
- **Frontend**: Aplicación local (web browser en `http://localhost:8501`)

### Cambiar entre entornos (solo para desarrollo):
```powershell
# Conectar a backend en AZURE (por defecto)
.\cambiar_entorno.ps1 AZURE

# Conectar a backend LOCAL (desarrollo)
.\cambiar_entorno.ps1 LOCAL
```

> **Nota**: En uso normal, siempre usarás AZURE. Solo cambias a LOCAL si estás desarrollando/probando cambios en el backend.

## 🔑 Configuración

Editar `backend/goot.py` con tus credenciales:

- **WhatsApp Business API**: `PHONE_NUMBER_ID`, `ACCESS_TOKEN`, `VERIFY_TOKEN`
- **Microsoft Dataverse**: `TENANT_ID`, `CLIENT_ID`, `CLIENT_SECRET`, `DATAVERSE_URL`

## 📡 Endpoints API

### Webhook WhatsApp
- `GET /webhook` - Verificación del webhook
- `POST /webhook` - Recibe mensajes de WhatsApp y procesa menú interactivo

### Autenticación (Público)
- `POST /api/login` - Login de usuarios (retorna JWT token)
- `POST /register` - Registro de nuevos usuarios

### Gestión de Conversaciones
- `GET /api/conversations` - Lista conversaciones recientes (requiere token)
- `GET /api/messages/<phone>` - Historial de mensajes (requiere token)
- `POST /api/send_message` - Enviar mensaje manual (requiere token)

### Administración de Usuarios (Solo Admin)
- `GET /api/users` - Lista todos los usuarios (requiere token admin)
- `POST /api/users` - Crear nuevo usuario (requiere token admin)

### ⭐ Gestión de Grupos (NUEVO)
- `GET /api/grupos` - Listar grupos (filtro: ?tipo=A)
- `POST /api/grupos` - Crear grupo
- `PUT /api/grupos/<idgrupo>` - Actualizar grupo
- `DELETE /api/grupos/<idgrupo>` - Eliminar grupo

### ⭐ Gestión de Estados (NUEVO)
- `GET /api/estados` - Listar estados
- `POST /api/estados` - Crear estado
- `PUT /api/estados/<idestado>` - Actualizar estado
- `DELETE /api/estados/<idestado>` - Eliminar estado

### ⭐ Sistema de Tickets (NUEVO)
- `GET /api/tickets` - Listar tickets (filtros: ?grupo=1&estado=1&tipo=soporte)
- `GET /api/tickets/<idticket>` - Obtener ticket específico
- `POST /api/tickets` - Crear ticket
- `PUT /api/tickets/<idticket>` - Actualizar ticket
- `DELETE /api/tickets/<idticket>` - Eliminar ticket

### ⭐ Usuario-Grupos (NUEVO)
- `GET /api/usuario-grupos` - Listar relaciones
- `GET /api/usuario-grupos/usuario/<usuario_id>` - Grupos de un usuario
- `GET /api/usuario-grupos/grupo/<grupo_id>` - Usuarios de un grupo
- `POST /api/usuario-grupos` - Asignar usuario a grupo
- `DELETE /api/usuario-grupos/<relacion_id>` - Eliminar relación

## 🤖 Sistema de Menú Interactivo WhatsApp

El webhook ahora implementa un menú conversacional completo:

### Menú Principal
```
¡Bienvenido! Por favor seleccione una opción:

1. Solicitud Ticket
2. Cotizaciones
3. Información
4. Solicitar atención de agente
```

### Flujos de Conversación

**Opción 1: Solicitud Ticket**
1. Sistema: "Por favor, indique su nombre completo:"
2. Usuario: [Nombre]
3. Sistema: "¿De qué empresa nos contacta?"
4. Usuario: [Empresa]
5. Sistema: "Describa su solicitud de soporte:"
6. Usuario: [Descripción]
7. Sistema: "¡Gracias! Su solicitud ha sido registrada con el ticket #123..."

**Opción 2: Cotizaciones**
1. Sistema: "Por favor, indique su nombre completo:"
2. Usuario: [Nombre]
3. Sistema: "¿De qué empresa nos contacta?"
4. Usuario: [Empresa]
5. Sistema: "Describa el producto, marca y modelo si lo tiene:"
6. Usuario: [Descripción]
7. Sistema: "¡Gracias! Su cotización ha sido registrada con el ticket #124..."

**Opción 3: Información**
- Respuesta inmediata con información general
- No crea ticket

**Opción 4: Solicitar atención de agente**
1. Sistema: "Por favor, indique su nombre para conectarlo con un agente:"
2. Usuario: [Nombre]
3. Sistema crea ticket y notifica para asignación de agente

## 🛠️ Tecnologías

- Python 3.x
- Flask + Flask-CORS
- Flet (UI)
- Microsoft MSAL
- Requests
- Microsoft Graph API

## 🔄 Sincronización con GitHub

### Opción 1: Script automático con mensaje personalizado
```powershell
.\sync.ps1 "Descripción de tus cambios"
```

### Opción 2: Script rápido (genera mensaje automático)
```powershell
.\quick-sync.ps1
```

### Opción 3: Manual (3 comandos)
```powershell
git add -A
git commit -m "Tu mensaje"
git push origin main
```

**📖 Guía detallada:** Ver [COMO_SINCRONIZAR_GIT.md](COMO_SINCRONIZAR_GIT.md) 