# WP0 - WhatsApp Manager

Sistema de gestión de conversaciones de WhatsApp Business integrado con Microsoft Dataverse.

## 🏗️ Arquitectura

- **Backend**: Flask + Microsoft Graph API (WhatsApp Business)
- **Frontend**: Flet (Python GUI)
- **Base de datos**: Microsoft Dataverse (CRM)
- **Autenticación**: Microsoft MSAL

## 📁 Estructura del Proyecto

```
CLAUDE-1/
├── backend/           # Servidor Flask principal
│   ├── app.py        # Servidor principal con webhook y API REST
│   ├── config.py     # Configuración global
│   ├── goot.py       # Variables de entorno y funciones auxiliares
│   └── api/          # Módulos API organizados por funcionalidad
│       ├── auth.py          # Autenticación de usuarios
│       ├── conversations.py # Gestión de conversaciones
│       ├── messages.py      # Envío y recepción de mensajes
│       ├── users.py         # Administración de usuarios
│       ├── webhook.py       # Webhook de WhatsApp
│       ├── reportes.py      # Reportes y estadísticas
│       └── settings.py      # Configuración de la app
│
├── mobile/            # Aplicación GUI con Flet
│   ├── main.py       # Punto de entrada de la app
│   ├── assets/       # Estilos e iconos
│   └── components/   # Componentes UI (login, chat, dashboard, etc.)
│
├── venv_clean/        # Entorno virtual de Python
├── iniciar.ps1        # Script de inicio automático
└── requirements.txt   # Dependencias del proyecto
```

## 🚀 Inicio Rápido

### Opción 1: Script automático (PowerShell)
```powershell
.\iniciar.ps1
```

### Opción 2: Manual
```powershell
# Terminal 1 - Backend
cd backend
python app.py

# Terminal 2 - Frontend (nueva ventana)
cd mobile
python main.py
```

## 🌐 Configuración de Entorno (LOCAL vs AZURE)

La aplicación móvil puede conectarse a diferentes backends:

### Cambiar entre entornos:
```powershell
# Usar backend LOCAL (por defecto)
.\cambiar_entorno.ps1 LOCAL

# Usar backend en AZURE
.\cambiar_entorno.ps1 AZURE

# Usar backend en PRODUCTION (requiere configurar PRODUCTION_URL)
.\cambiar_entorno.ps1 PRODUCTION
```

**Entornos disponibles**:
- **LOCAL**: `http://localhost:5000` (desarrollo)
- **AZURE**: `https://whatsapp-flask-app-f4gsb7dhhybcg6f6.eastus-01.azurewebsites.net`
- **PRODUCTION**: Configurar variable `PRODUCTION_URL`

> **Nota**: Después de cambiar el entorno, reinicia la aplicación móvil.

## 🔑 Configuración

Editar `backend/goot.py` con tus credenciales:

- **WhatsApp Business API**: `PHONE_NUMBER_ID`, `ACCESS_TOKEN`, `VERIFY_TOKEN`
- **Microsoft Dataverse**: `TENANT_ID`, `CLIENT_ID`, `CLIENT_SECRET`, `DATAVERSE_URL`

## 📡 Endpoints API

### Webhook WhatsApp
- `GET/POST /webhook` - Recibe mensajes de WhatsApp

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

## 🤖 Bot Automático

Responde automáticamente a:
- **"hola", "menu", "mm"** → Muestra menú de opciones
- **"1"** → Información de servicios
- **"2"** → Cotizaciones
- **"3"** → Solicitar llamada de asesor

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