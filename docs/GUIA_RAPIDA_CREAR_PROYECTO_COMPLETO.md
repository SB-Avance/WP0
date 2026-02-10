# 🚀 GUÍA RÁPIDA - Crear Proyecto Completo Desde Cero

> **Guía Consolidada** para crear todos los archivos del Sistema de Chatbot WhatsApp con CRM/ERP integrado con Microsoft Dataverse.

---

## 📋 Tabla de Contenidos

1. [Estructura del Proyecto](#estructura-del-proyecto)
2. [Paso 1: Configuración Inicial](#paso-1-configuración-inicial)
3. [Paso 2: Crear Backend (Flask API)](#paso-2-crear-backend-flask-api)
4. [Paso 3: Crear Frontend (Flet)](#paso-3-crear-frontend-flet)
5. [Paso 4: Scripts de Inicialización](#paso-4-scripts-de-inicialización)
6. [Paso 5: Tests](#paso-5-tests)
7. [Paso 6: Documentación](#paso-6-documentación)
8. [Paso 7: Configurar Dataverse](#paso-7-configurar-dataverse)
9. [Paso 8: Iniciar Sistema](#paso-8-iniciar-sistema)

---

## 📁 Estructura del Proyecto

```
BIN/
├── .env                           # Variables de entorno (NO incluir en Git)
├── requirements.txt               # Dependencias principales
├── README.md                      # Documentación principal
├── init_dataverse.py             # Script de inicialización de datos
├── inicializar_sistema.py        # Script de inicialización completa
├── asignar_categorias_chats.py   # Script de asignación de categorías
├── iniciar.ps1                   # Script PowerShell - iniciar frontend
├── iniciar_backend.ps1           # Script PowerShell - iniciar backend
├── cambiar_entorno.ps1           # Script PowerShell - cambiar entorno
├── sync.ps1                      # Script PowerShell - sync Git
├── crear_tablas_dataverse.ps1    # Guía para crear tablas
│
├── backend/                       # API Flask
│   ├── back.py                   # Servidor principal
│   ├── config.py                 # Configuración global
│   ├── goot.py                   # Variables de entorno y funciones
│   ├── requirements.txt          # Dependencias backend
│   ├── startup.txt               # Comando de inicio para Azure
│   └── api/                      # Módulos API (Blueprints)
│       ├── __init__.py
│       ├── auth.py               # Autenticación
│       ├── users.py              # Gestión de usuarios
│       ├── messages.py           # Mensajes WhatsApp
│       ├── conversations.py      # Conversaciones
│       ├── webhook.py            # Webhook + Menú interactivo
│       ├── webhook_enhanced.py   # Webhook mejorado con auto-contactos
│       ├── reportes.py           # Reportes y estadísticas
│       ├── settings.py           # Configuración del sistema
│       ├── grupos.py             # Gestión de grupos
│       ├── estados.py            # Gestión de estados
│       ├── tickets.py            # Sistema de tickets
│       ├── usuario_grupos.py     # Relaciones usuario-grupo
│       ├── chatbots.py           # Gestión de chatbots
│       ├── whatsapp_accounts.py  # Cuentas de WhatsApp
│       ├── cotizaciones.py       # Sistema de cotizaciones
│       ├── chats_extended.py     # API extendida con $expand
│       └── dashboard.py          # Dashboard de métricas
│
├── mobile/                        # Frontend Flet
│   ├── main.py                   # Aplicación principal
│   ├── config.py                 # Configuración API URL
│   ├── Dockerfile                # Contenedor Docker
│   ├── assets/
│   │   └── styles.py             # Estilos globales
│   └── components/               # Pantallas UI
│       ├── login.py              # Pantalla de login
│       ├── dashboard.py          # Dashboard principal
│       ├── chats.py              # Lista de conversaciones
│       ├── chat_detail.py        # Detalle de conversación
│       ├── users.py              # Gestión de usuarios
│       ├── settings.py           # Configuración
│       ├── sidebar.py            # Menú lateral
│       └── chatbots.py           # Gestión de chatbots
│
├── tests/                         # Suite de pruebas
│   ├── README.md
│   ├── test_sistema.py           # Tests completos del sistema
│   ├── test_backend.py           # Tests básicos del backend
│   ├── test_chats_extended.py    # Tests de API extendida
│   ├── test_dashboard.py         # Tests del dashboard
│   ├── test_campo_lookup.py      # Tests de campos lookup
│   ├── test_webhook_contacto.py  # Tests de webhook con contactos
│   └── test_webhook_enhanced.py  # Tests de webhook mejorado
│
├── scripts_antiguos/              # Scripts históricos
│   └── README.md
│
├── docs/                          # Documentación completa
│   ├── INDICE_DOCUMENTACION.md   # Índice de toda la documentación
│   ├── INICIO_RAPIDO.md          # Guía de inicio rápido
│   ├── GUIA_SISTEMA_CHATBOT.md   # Guía técnica completa
│   ├── GUIA_CREAR_TABLAS_VISUAL.md           # Crear tablas en Dataverse
│   ├── GUIA_RAPIDA_USUARIO_GRUPOS.md         # Usuarios y grupos
│   ├── GUIA_TABLAS_ADICIONALES.md            # Tablas adicionales
│   ├── GUIA_RAPIDA_CREAR_PROYECTO_COMPLETO.md # (este archivo)
│   ├── MAPA_APLICACION.md        # Arquitectura del sistema
│   ├── README.md
│   ├── tablas_dataverse.json     # Estructura de tablas
│   └── tablas_adicionales.json   # Tablas complementarias
│
└── venv_clean/                    # Entorno virtual Python
```

---

## Paso 1: Configuración Inicial

### 1.1 Crear Directorio del Proyecto

```powershell
# Crear carpeta principal
New-Item -ItemType Directory -Path "C:\VS\BIN"
Set-Location "C:\VS\BIN"
```

### 1.2 Crear Entorno Virtual

```powershell
# Crear entorno virtual
python -m venv venv_clean

# Activar entorno virtual
.\venv_clean\Scripts\Activate.ps1
```

### 1.3 Crear archivo `.env` (Variables de Entorno)

**Archivo:** `.env`

```bash
# ========== MICROSOFT AZURE AD ==========
TENANT_ID=tu-tenant-id-aqui
CLIENT_ID=tu-client-id-aqui
CLIENT_SECRET=tu-client-secret-aqui

# ========== MICROSOFT DATAVERSE ==========
DATAVERSE_URL=https://org123456.crm.dynamics.com
ENTITY_SET=cr321_chats

# ========== WHATSAPP BUSINESS API V17.0 ==========
PHONE_NUMBER_ID=123456789012345
PHONE_NUMBER_ID0=123456789012345  # Cuenta principal
PHONE_NUMBER_ID1=987654321098765  # Cuenta secundaria (opcional)
ACCESS_TOKEN=tu-whatsapp-access-token-aqui
VERIFY_TOKEN=mi_token_secreto_webhook_2024

# ========== FLASK ==========
SECRET_KEY=supersecretkey_produccion_2024
FLASK_ENV=development
FLASK_DEBUG=1

# ========== FRONTEND ==========
# Valores: LOCAL o AZURE
ENVIRONMENT=LOCAL
```

**⚠️ IMPORTANTE:** 
- Nunca incluir `.env` en Git (agregar a `.gitignore`)
- Reemplazar todos los valores `tu-*-aqui` con valores reales

### 1.4 Crear `.gitignore`

**Archivo:** `.gitignore`

```gitignore
# Variables de entorno
.env
.env.local
.env.*.local

# Entornos virtuales
venv/
venv_clean/
env/
ENV/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db
```

### 1.5 Crear `requirements.txt` Principal

**Archivo:** `requirements.txt`

```txt
# Backend
Flask==3.0.0
msal==1.26.0
requests==2.31.0
python-dotenv==1.0.0
gunicorn==21.2.0
flask-cors==4.0.0

# Frontend
flet==0.25.2

# Utilidades
PyJWT==2.8.0
```

---

## Paso 2: Crear Backend (Flask API)

### 2.1 Crear Estructura del Backend

```powershell
# Crear carpetas
New-Item -ItemType Directory -Path "backend"
New-Item -ItemType Directory -Path "backend\api"
```

### 2.2 Crear `backend/config.py`

**Archivo:** `backend/config.py`

```python
# Configuración global y clave secreta para JWT
import os

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
```

### 2.3 Crear `backend/goot.py`

**Archivo:** `backend/goot.py`

```python
import os
from dotenv import load_dotenv
from msal import ConfidentialClientApplication
import requests

# Cargar variables de entorno
load_dotenv()

# ========== VARIABLES DE ENTORNO ==========
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
DATAVERSE_URL = os.getenv("DATAVERSE_URL")
ENTITY_SET = os.getenv("ENTITY_SET", "cr321_chats")

PHONE_NUMBER_ID0 = os.getenv("PHONE_NUMBER_ID0")
PHONE_NUMBER_ID1 = os.getenv("PHONE_NUMBER_ID1")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

# ========== FUNCIONES AUXILIARES ==========
def clear_screen():
    """Limpiar la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_variables():
    """Mostrar variables de configuración de forma segura"""
    return f"""
    ========== CONFIGURACIÓN ==========
    TENANT_ID: {TENANT_ID[:8] + '...' if TENANT_ID else 'NO CONFIGURADO'}
    CLIENT_ID: {CLIENT_ID[:8] + '...' if CLIENT_ID else 'NO CONFIGURADO'}
    DATAVERSE_URL: {DATAVERSE_URL}
    ENTITY_SET: {ENTITY_SET}
    PHONE_NUMBER_ID: {PHONE_NUMBER_ID}
    VERIFY_TOKEN: {'Configurado' if VERIFY_TOKEN else 'NO CONFIGURADO'}
    ==================================
    """

def get_dataverse_token():
    """Obtener token de acceso para Dataverse"""
    authority = f"https://login.microsoftonline.com/{TENANT_ID}"
    scope = [f"{DATAVERSE_URL}/.default"]
    
    app = ConfidentialClientApplication(
        CLIENT_ID,
        authority=authority,
        client_credential=CLIENT_SECRET
    )
    
    result = app.acquire_token_for_client(scopes=scope)
    
    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception(f"Error al obtener token: {result.get('error_description', 'Unknown error')}")

def get_dataverse_headers():
    """Obtener headers para peticiones a Dataverse"""
    token = get_dataverse_token()
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0",
        "Prefer": "return=representation"
    }

def get_from_dataverse(entity_set, entity_id=None, filters=None, expand=None, select=None):
    """Obtener datos de Dataverse"""
    headers = get_dataverse_headers()
    url = f"{DATAVERSE_URL}/api/data/v9.2/{entity_set}"
    
    if entity_id:
        url += f"({entity_id})"
    
    # Construir query parameters
    params = []
    if filters:
        params.append(f"$filter={filters}")
    if expand:
        params.append(f"$expand={expand}")
    if select:
        params.append(f"$select={select}")
    
    if params:
        url += "?" + "&".join(params)
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def post_to_dataverse(entity_set, data):
    """Crear registro en Dataverse"""
    headers = get_dataverse_headers()
    url = f"{DATAVERSE_URL}/api/data/v9.2/{entity_set}"
    
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

def patch_to_dataverse(entity_set, entity_id, data):
    """Actualizar registro en Dataverse"""
    headers = get_dataverse_headers()
    url = f"{DATAVERSE_URL}/api/data/v9.2/{entity_set}({entity_id})"
    
    response = requests.patch(url, headers=headers, json=data)
    response.raise_for_status()
    return True

def delete_from_dataverse(entity_set, entity_id):
    """Eliminar registro de Dataverse"""
    headers = get_dataverse_headers()
    url = f"{DATAVERSE_URL}/api/data/v9.2/{entity_set}({entity_id})"
    
    response = requests.delete(url, headers=headers)
    response.raise_for_status()
    return True
```

### 2.4 Crear `backend/back.py` (Servidor Principal)

**Archivo:** `backend/back.py`

```python
# ============ IMPORTACIONES ============
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timezone
from msal import ConfidentialClientApplication
import requests
import os

# Importar configuración desde goot.py
import goot
from goot import (
    PHONE_NUMBER_ID0, PHONE_NUMBER_ID1, PHONE_NUMBER_ID, VERIFY_TOKEN, ACCESS_TOKEN, 
    TENANT_ID, CLIENT_ID, CLIENT_SECRET, DATAVERSE_URL, ENTITY_SET, clear_screen
)

# Importar Blueprints
from api.auth import bp_auth
from api.users import bp_users
from api.messages import bp_messages
from api.conversations import bp_conversations
from api.webhook import bp_webhook
from api.reportes import bp_reportes
from api.settings import bp_settings
from api.grupos import bp_grupos
from api.estados import bp_estados
from api.tickets import bp_tickets
from api.usuario_grupos import bp_usuario_grupos
from api.chatbots import bp_chatbots
from api.whatsapp_accounts import bp_whatsapp_accounts
from api.chats_extended import bp as bp_chats_extended
from api.dashboard import bp_dashboard

# ============ INICIALIZAR FLASK ============
app = Flask(__name__)

# CORS optimizado
CORS(app, 
     resources={r"/api/*": {"origins": "*"}},
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"])

# ============ INICIO ============
clear_screen()
print("--------------  Inicio ----------****------")
print(goot.mostrar_variables())

# ============ CONSTANTES ============
GROUP_TO_INT = {
    "SERVICIOS": 1,
    "COTIZACIONES": 2,
    "SOPORTE": 3,
    "GENERAL": None,
    "TODOS": None
}

INT_TO_GROUP = {
    1: "SERVICIOS",
    2: "COTIZACIONES",
    3: "SOPORTE",
    None: "GENERAL"
}

MESSAGE_TYPES = {
    "text": 462410000,
    "image": 462410001,
    "audio": 462410002
}

MESSAGE_DIRECTION = {
    "incoming": 462410000,
    "outgoing": 462410001
}

# ============ REGISTRAR BLUEPRINTS ============
app.register_blueprint(bp_auth, url_prefix='/api/auth')
app.register_blueprint(bp_users, url_prefix='/api/users')
app.register_blueprint(bp_messages, url_prefix='/api/messages')
app.register_blueprint(bp_conversations, url_prefix='/api/conversations')
app.register_blueprint(bp_webhook, url_prefix='/webhook')
app.register_blueprint(bp_reportes, url_prefix='/api/reportes')
app.register_blueprint(bp_settings, url_prefix='/api/settings')
app.register_blueprint(bp_grupos, url_prefix='/api/grupos')
app.register_blueprint(bp_estados, url_prefix='/api/estados')
app.register_blueprint(bp_tickets, url_prefix='/api/tickets')
app.register_blueprint(bp_usuario_grupos, url_prefix='/api/usuario-grupos')
app.register_blueprint(bp_chatbots, url_prefix='/api/chatbots')
app.register_blueprint(bp_whatsapp_accounts, url_prefix='/api/whatsapp-accounts')
app.register_blueprint(bp_chats_extended, url_prefix='/api/chats-extended')
app.register_blueprint(bp_dashboard, url_prefix='/api/dashboard')

print("✅ Blueprints registrados correctamente")

# ============ RUTAS BÁSICAS ============
@app.route('/')
def home():
    """Ruta principal"""
    return jsonify({
        "status": "ok",
        "message": "WhatsApp CRM API - Sistema Operacional",
        "version": "3.0.0",
        "date": datetime.now(timezone.utc).isoformat()
    })

@app.route('/health')
def health():
    """Health check para Azure"""
    return jsonify({"status": "healthy"}), 200

# ============ MANEJO DE ERRORES ============
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint no encontrado"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Error interno del servidor"}), 500

# ============ EJECUTAR SERVIDOR ============
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=True
    )
```

### 2.5 Crear Módulos API (Blueprints)

#### 2.5.1 `backend/api/__init__.py`

**Archivo:** `backend/api/__init__.py`

```python
# Paquete API - Módulos Blueprint para Flask
```

#### 2.5.2 `backend/api/auth.py` (Autenticación)

**Archivo:** `backend/api/auth.py`

```python
from flask import Blueprint, request, jsonify
from msal import ConfidentialClientApplication
import jwt
from datetime import datetime, timedelta
import goot
from config import SECRET_KEY

bp_auth = Blueprint('auth', __name__)

@bp_auth.route('/login', methods=['POST'])
def login():
    """Login con Azure AD"""
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        # Validar con Azure AD
        authority = f"https://login.microsoftonline.com/{goot.TENANT_ID}"
        app = ConfidentialClientApplication(
            goot.CLIENT_ID,
            authority=authority,
            client_credential=goot.CLIENT_SECRET
        )
        
        result = app.acquire_token_by_username_password(
            username=username,
            password=password,
            scopes=[f"{goot.DATAVERSE_URL}/.default"]
        )
        
        if "access_token" in result:
            # Generar JWT para el frontend
            token = jwt.encode({
                'user': username,
                'exp': datetime.utcnow() + timedelta(hours=24)
            }, SECRET_KEY, algorithm='HS256')
            
            return jsonify({
                "success": True,
                "token": token,
                "user": {
                    "email": username,
                    "name": username.split('@')[0]
                }
            })
        else:
            return jsonify({
                "success": False,
                "message": "Credenciales inválidas"
            }), 401
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@bp_auth.route('/verify', methods=['GET'])
def verify():
    """Verificar token JWT"""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return jsonify({"valid": True, "user": payload['user']})
    except:
        return jsonify({"valid": False}), 401
```

#### 2.5.3 `backend/api/conversations.py`

**Archivo:** `backend/api/conversations.py`

```python
from flask import Blueprint, request, jsonify
import goot

bp_conversations = Blueprint('conversations', __name__)

@bp_conversations.route('', methods=['GET'])
def get_conversations():
    """Obtener lista de conversaciones"""
    try:
        group_filter = request.args.get('group', 'TODOS')
        
        # Construir filtro OData
        filters = []
        if group_filter and group_filter != 'TODOS':
            filters.append(f"cr321_grupo eq '{group_filter}'")
        
        # Obtener conversaciones de Dataverse
        filter_str = " and ".join(filters) if filters else None
        result = goot.get_from_dataverse(
            goot.ENTITY_SET,
            filters=filter_str,
            select="cr321_chatid,cr321_phone,cr321_name,cr321_grupo,cr321_lastmessage,cr321_lastmessagetime"
        )
        
        conversations = []
        if "value" in result:
            for conv in result["value"]:
                conversations.append({
                    "id": conv.get("cr321_chatid"),
                    "phone": conv.get("cr321_phone"),
                    "name": conv.get("cr321_name", "Sin nombre"),
                    "grupo": conv.get("cr321_grupo", "GENERAL"),
                    "last_message": conv.get("cr321_lastmessage", ""),
                    "last_message_time": conv.get("cr321_lastmessagetime")
                })
        
        return jsonify({
            "success": True,
            "conversations": conversations,
            "total": len(conversations)
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
```

#### 2.5.4 `backend/api/messages.py`

**Archivo:** `backend/api/messages.py`

```python
from flask import Blueprint, request, jsonify
import requests
import goot

bp_messages = Blueprint('messages', __name__)

@bp_messages.route('/send', methods=['POST'])
def send_message():
    """Enviar mensaje de WhatsApp"""
    try:
        data = request.json
        phone = data.get('phone')
        message = data.get('message')
        
        # Enviar a WhatsApp Business API
        url = f"https://graph.facebook.com/v17.0/{goot.PHONE_NUMBER_ID}/messages"
        headers = {
            "Authorization": f"Bearer {goot.ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": phone,
            "type": "text",
            "text": {"body": message}
        }
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        # Guardar en Dataverse
        # ... (lógica para guardar mensaje)
        
        return jsonify({
            "success": True,
            "message": "Mensaje enviado correctamente"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@bp_messages.route('/history/<phone>', methods=['GET'])
def get_message_history(phone):
    """Obtener historial de mensajes de un contacto"""
    try:
        # Obtener mensajes de Dataverse
        filters = f"cr321_phone eq '{phone}'"
        result = goot.get_from_dataverse(
            "cr321_messages",
            filters=filters,
            select="cr321_messageid,cr321_text,cr321_timestamp,cr321_direction"
        )
        
        messages = []
        if "value" in result:
            for msg in result["value"]:
                messages.append({
                    "id": msg.get("cr321_messageid"),
                    "text": msg.get("cr321_text"),
                    "timestamp": msg.get("cr321_timestamp"),
                    "direction": msg.get("cr321_direction")
                })
        
        return jsonify({
            "success": True,
            "messages": messages
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
```

#### 2.5.5 `backend/api/webhook.py`

**Archivo:** `backend/api/webhook.py`

```python
from flask import Blueprint, request, jsonify
import goot

bp_webhook = Blueprint('webhook', __name__)

# Configuración del menú interactivo
MENU_OPTIONS = {
    "1": {"grupo": "SERVICIOS", "mensaje": "Has seleccionado: Servicios"},
    "2": {"grupo": "COTIZACIONES", "mensaje": "Has seleccionado: Cotizaciones"},
    "3": {"grupo": "SOPORTE", "mensaje": "Has seleccionado: Soporte Técnico"},
    "4": {"grupo": "GENERAL", "mensaje": "Has seleccionado: Información General"}
}

MENU_TEXT = """
🤖 *Menú Principal*

Selecciona una opción enviando el número:

1️⃣ Servicios
2️⃣ Cotizaciones
3️⃣ Soporte Técnico
4️⃣ Información General

Responde con el número de tu opción.
"""

@bp_webhook.route('', methods=['GET'])
def verify_webhook():
    """Verificación del webhook de WhatsApp"""
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode == 'subscribe' and token == goot.VERIFY_TOKEN:
        print("✅ Webhook verificado correctamente")
        return challenge, 200
    else:
        return 'Token inválido', 403

@bp_webhook.route('', methods=['POST'])
def handle_webhook():
    """Procesar mensajes entrantes de WhatsApp"""
    try:
        data = request.json
        
        # Extraer mensaje
        if 'messages' not in data.get('entry', [{}])[0].get('changes', [{}])[0].get('value', {}):
            return jsonify({"status": "ok"}), 200
        
        message_data = data['entry'][0]['changes'][0]['value']['messages'][0]
        phone = message_data['from']
        message_text = message_data.get('text', {}).get('body', '')
        
        # Detectar si es una opción del menú
        if message_text.strip() in MENU_OPTIONS:
            opcion = MENU_OPTIONS[message_text.strip()]
            
            # Actualizar grupo en Dataverse
            # ... (lógica para actualizar)
            
            # Enviar confirmación
            send_whatsapp_message(phone, opcion['mensaje'])
        
        # Guardar mensaje en Dataverse
        # ... (lógica para guardar)
        
        return jsonify({"status": "ok"}), 200
        
    except Exception as e:
        print(f"Error en webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

def send_whatsapp_message(phone, message):
    """Enviar mensaje de WhatsApp"""
    import requests
    url = f"https://graph.facebook.com/v17.0/{goot.PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {goot.ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": message}
    }
    requests.post(url, headers=headers, json=payload)
```

#### 2.5.6 Otros Blueprints (Plantillas Básicas)

Crear archivos con estructura similar para:
- `backend/api/users.py`
- `backend/api/reportes.py`
- `backend/api/settings.py`
- `backend/api/grupos.py`
- `backend/api/estados.py`
- `backend/api/tickets.py`
- `backend/api/usuario_grupos.py`
- `backend/api/chatbots.py`
- `backend/api/whatsapp_accounts.py`
- `backend/api/chats_extended.py`
- `backend/api/dashboard.py`

**Plantilla básica para cada Blueprint:**

```python
from flask import Blueprint, request, jsonify
import goot

bp_[NOMBRE] = Blueprint('[NOMBRE]', __name__)

@bp_[NOMBRE].route('', methods=['GET'])
def get_all():
    """Obtener todos los registros"""
    try:
        result = goot.get_from_dataverse('cr321_[TABLA]')
        return jsonify({"success": True, "data": result.get("value", [])})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@bp_[NOMBRE].route('', methods=['POST'])
def create():
    """Crear nuevo registro"""
    try:
        data = request.json
        result = goot.post_to_dataverse('cr321_[TABLA]', data)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
```

### 2.6 Crear `backend/requirements.txt`

**Archivo:** `backend/requirements.txt`

```txt
Flask==3.0.0
msal==1.26.0
requests==2.31.0
python-dotenv==1.0.0
gunicorn==21.2.0
flask-cors==4.0.0
PyJWT==2.8.0
```

### 2.7 Crear `backend/startup.txt` (para Azure)

**Archivo:** `backend/startup.txt`

```txt
gunicorn --bind=0.0.0.0:8000 --timeout 600 back:app
```

---

## Paso 3: Crear Frontend (Flet)

### 3.1 Crear Estructura del Frontend

```powershell
New-Item -ItemType Directory -Path "mobile"
New-Item -ItemType Directory -Path "mobile\components"
New-Item -ItemType Directory -Path "mobile\assets"
```

### 3.2 Crear `mobile/config.py`

**Archivo:** `mobile/config.py`

```python
import os

# Configuración de entorno
ENVIRONMENT = os.getenv("ENVIRONMENT", "LOCAL")

# URLs según entorno
ENVIRONMENTS = {
    "LOCAL": "http://localhost:5000",
    "AZURE": "https://whatsapp-flask-app-f4gsb7dhhybcg6f6.eastus-01.azurewebsites.net"
}

# API Base URL
API_BASE_URL = ENVIRONMENTS.get(ENVIRONMENT, ENVIRONMENTS["LOCAL"])

print(f"[CONFIG] Entorno: {ENVIRONMENT}")
print(f"[CONFIG] API URL: {API_BASE_URL}")
```

### 3.3 Crear `mobile/assets/styles.py`

**Archivo:** `mobile/assets/styles.py`

```python
import flet as ft

# Colores principales
PRIMARY_COLOR = "#25D366"  # Verde WhatsApp
SECONDARY_COLOR = "#128C7E"
BACKGROUND_COLOR = "#ECE5DD"
WHITE = "#FFFFFF"
GRAY_LIGHT = "#F0F0F0"
GRAY_DARK = "#3C3C3C"

# Estilos de texto
TITLE_STYLE = ft.TextStyle(
    size=24,
    weight=ft.FontWeight.BOLD,
    color=GRAY_DARK
)

SUBTITLE_STYLE = ft.TextStyle(
    size=16,
    weight=ft.FontWeight.W_500,
    color=GRAY_DARK
)

BODY_STYLE = ft.TextStyle(
    size=14,
    color=GRAY_DARK
)

# Estilos de botones
PRIMARY_BUTTON = ft.ButtonStyle(
    color=WHITE,
    bgcolor=PRIMARY_COLOR
)
```

### 3.4 Crear `mobile/main.py`

**Archivo:** `mobile/main.py`

```python
import flet as ft
from components.login import LoginView
from components.dashboard import DashboardView
from components.sidebar import SidebarView
from components.chats import ChatsView
from components.chat_detail import ChatDetailView
from components.users import UsersView
from components.settings import SettingsView
from assets import styles
import requests
from config import API_BASE_URL

class WhatsAppCRM:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "WhatsApp CRM"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 0
        
        self.token = None
        self.user = None
        self.current_view = None
        
        # Mostrar vista de login
        self.show_login()
    
    def show_login(self):
        """Mostrar pantalla de login"""
        login_view = LoginView(self.on_login_success)
        self.page.clean()
        self.page.add(login_view)
        self.page.update()
    
    def on_login_success(self, token, user):
        """Callback cuando login es exitoso"""
        self.token = token
        self.user = user
        self.show_dashboard()
    
    def show_dashboard(self):
        """Mostrar dashboard principal"""
        self.page.clean()
        
        # Crear sidebar
        sidebar = SidebarView(
            user=self.user,
            on_menu_click=self.navigate,
            on_logout=self.logout
        )
        
        # Crear contenido principal
        self.main_content = ft.Container(
            content=DashboardView(self.token),
            expand=True,
            padding=20
        )
        
        # Layout principal
        layout = ft.Row(
            controls=[sidebar, self.main_content],
            spacing=0,
            expand=True
        )
        
        self.page.add(layout)
        self.page.update()
    
    def navigate(self, view_name):
        """Navegar entre vistas"""
        if view_name == "dashboard":
            self.main_content.content = DashboardView(self.token)
        elif view_name == "chats":
            self.main_content.content = ChatsView(self.token)
        elif view_name == "users":
            self.main_content.content = UsersView(self.token)
        elif view_name == "settings":
            self.main_content.content = SettingsView(self.token)
        
        self.page.update()
    
    def logout(self):
        """Cerrar sesión"""
        self.token = None
        self.user = None
        self.show_login()

def main(page: ft.Page):
    app = WhatsAppCRM(page)

if __name__ == "__main__":
    ft.app(target=main)
```

### 3.5 Crear Componentes UI

#### 3.5.1 `mobile/components/login.py`

**Archivo:** `mobile/components/login.py`

```python
import flet as ft
import requests
from config import API_BASE_URL

class LoginView(ft.Container):
    def __init__(self, on_login_success):
        super().__init__()
        
        self.on_login_success = on_login_success
        
        # Input fields
        self.username_field = ft.TextField(
            label="Usuario",
            width=300,
            prefix_icon=ft.icons.PERSON
        )
        
        self.password_field = ft.TextField(
            label="Contraseña",
            width=300,
            password=True,
            can_reveal_password=True,
            prefix_icon=ft.icons.LOCK
        )
        
        self.error_text = ft.Text(
            value="",
            color=ft.colors.RED,
            size=12
        )
        
        # Login button
        self.login_btn = ft.ElevatedButton(
            text="Iniciar Sesión",
            width=300,
            on_click=self.handle_login
        )
        
        # Layout
        self.content = ft.Column(
            controls=[
                ft.Container(height=50),
                ft.Text("WhatsApp CRM", size=32, weight=ft.FontWeight.BOLD),
                ft.Container(height=30),
                self.username_field,
                self.password_field,
                self.error_text,
                ft.Container(height=20),
                self.login_btn
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        self.expand = True
        self.alignment = ft.alignment.center
    
    def handle_login(self, e):
        """Manejar login"""
        username = self.username_field.value
        password = self.password_field.value
        
        if not username or not password:
            self.error_text.value = "Por favor ingresa usuario y contraseña"
            self.update()
            return
        
        try:
            # Llamar a API de login
            response = requests.post(
                f"{API_BASE_URL}/api/auth/login",
                json={"username": username, "password": password},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.on_login_success(data["token"], data["user"])
                else:
                    self.error_text.value = data.get("message", "Error de autenticación")
            else:
                self.error_text.value = "Credenciales inválidas"
            
        except Exception as ex:
            self.error_text.value = f"Error de conexión: {str(ex)}"
        
        self.update()
```

#### 3.5.2 Crear Otros Componentes

Crear archivos similares para:
- `mobile/components/dashboard.py`
- `mobile/components/sidebar.py`
- `mobile/components/chats.py`
- `mobile/components/chat_detail.py`
- `mobile/components/users.py`
- `mobile/components/settings.py`
- `mobile/components/chatbots.py`

---

## Paso 4: Scripts de Inicialización

### 4.1 `init_dataverse.py`

**Archivo:** `init_dataverse.py`

```python
"""
Script para inicializar datos base en Dataverse
- Grupos tipo A (opciones del menú)
- Estados de tickets
"""
import requests
from backend import goot

def crear_grupos_iniciales():
    """Crear 4 grupos tipo A para el menú de WhatsApp"""
    grupos = [
        {"cr321_nombre": "SERVICIOS", "cr321_tipo": 462410000, "cr321_descripcion": "Grupo de Servicios"},
        {"cr321_nombre": "COTIZACIONES", "cr321_tipo": 462410000, "cr321_descripcion": "Grupo de Cotizaciones"},
        {"cr321_nombre": "SOPORTE", "cr321_tipo": 462410000, "cr321_descripcion": "Grupo de Soporte Técnico"},
        {"cr321_nombre": "GENERAL", "cr321_tipo": 462410000, "cr321_descripcion": "Grupo General"}
    ]
    
    for grupo in grupos:
        try:
            goot.post_to_dataverse("cr321_grupos", grupo)
            print(f"✅ Grupo creado: {grupo['cr321_nombre']}")
        except Exception as e:
            print(f"❌ Error creando {grupo['cr321_nombre']}: {e}")

def crear_estados_iniciales():
    """Crear estados de tickets"""
    estados = [
        {"cr321_nombre": "NUEVO", "cr321_descripcion": "Ticket nuevo"},
        {"cr321_nombre": "EN_PROCESO", "cr321_descripcion": "Ticket en proceso"},
        {"cr321_nombre": "ESPERANDO", "cr321_descripcion": "Esperando respuesta del cliente"},
        {"cr321_nombre": "RESUELTO", "cr321_descripcion": "Ticket resuelto"},
        {"cr321_nombre": "CERRADO", "cr321_descripcion": "Ticket cerrado"},
        {"cr321_nombre": "CANCELADO", "cr321_descripcion": "Ticket cancelado"}
    ]
    
    for estado in estados:
        try:
            goot.post_to_dataverse("cr321_estados", estado)
            print(f"✅ Estado creado: {estado['cr321_nombre']}")
        except Exception as e:
            print(f"❌ Error creando {estado['cr321_nombre']}: {e}")

if __name__ == "__main__":
    print("========== INICIANDO DATAVERSE ==========\n")
    
    print("1. Creando grupos...")
    crear_grupos_iniciales()
    
    print("\n2. Creando estados...")
    crear_estados_iniciales()
    
    print("\n✅ Inicialización completada")
```

### 4.2 Scripts PowerShell

#### 4.2.1 `iniciar_backend.ps1`

**Archivo:** `iniciar_backend.ps1`

```powershell
# Iniciar Backend (Flask API)
Write-Host "========== INICIANDO BACKEND ==========" -ForegroundColor Green

# Activar entorno virtual
& ".\venv_clean\Scripts\Activate.ps1"

# Cambiar a carpeta backend
Set-Location backend

# Iniciar servidor Flask
Write-Host "Iniciando servidor Flask en http://localhost:5000" -ForegroundColor Yellow
python back.py
```

#### 4.2.2 `iniciar.ps1`

**Archivo:** `iniciar.ps1`

```powershell
# Iniciar Frontend (Flet)
Write-Host "========== INICIANDO FRONTEND ==========" -ForegroundColor Green

# Activar entorno virtual
& ".\venv_clean\Scripts\Activate.ps1"

# Cambiar a carpeta mobile
Set-Location mobile

# Iniciar aplicación Flet
Write-Host "Iniciando aplicación Flet..." -ForegroundColor Yellow
python main.py
```

#### 4.2.3 `cambiar_entorno.ps1`

**Archivo:** `cambiar_entorno.ps1`

```powershell
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("LOCAL", "AZURE")]
    [string]$Entorno
)

Write-Host "========== CAMBIAR ENTORNO ==========" -ForegroundColor Cyan
Write-Host "Cambiando a entorno: $Entorno" -ForegroundColor Yellow

# Actualizar variable de entorno
[System.Environment]::SetEnvironmentVariable("ENVIRONMENT", $Entorno, "User")
$env:ENVIRONMENT = $Entorno

Write-Host "✅ Entorno cambiado a: $Entorno" -ForegroundColor Green
Write-Host "Reinicia la aplicación para aplicar los cambios." -ForegroundColor Yellow
```

---

## Paso 5: Tests

### 5.1 Crear Carpeta de Tests

```powershell
New-Item -ItemType Directory -Path "tests"
```

### 5.2 `tests/test_sistema.py`

**Archivo:** `tests/test_sistema.py`

```python
"""
Suite de pruebas completa del sistema
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_imports():
    """Test: Importación de módulos"""
    print("\n1. Testing imports...")
    try:
        from backend import goot
        from backend.back import app
        from backend.api import auth, users, conversations
        print("   ✅ Todos los módulos importados correctamente")
        return True
    except Exception as e:
        print(f"   ❌ Error en imports: {e}")
        return False

def test_blueprints():
    """Test: Blueprints registrados"""
    print("\n2. Testing blueprints...")
    try:
        from backend.back import app
        blueprints = [bp.name for bp in app.blueprints.values()]
        expected = ['auth', 'users', 'conversations', 'messages', 'webhook']
        
        for bp in expected:
            if bp in blueprints:
                print(f"   ✅ Blueprint '{bp}' registrado")
            else:
                print(f"   ❌ Blueprint '{bp}' NO registrado")
        
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_env_variables():
    """Test: Variables de entorno"""
    print("\n3. Testing variables de entorno...")
    try:
        from backend import goot
        required_vars = [
            'TENANT_ID', 'CLIENT_ID', 'CLIENT_SECRET',
            'DATAVERSE_URL', 'PHONE_NUMBER_ID', 'ACCESS_TOKEN'
        ]
        
        missing = []
        for var in required_vars:
            value = getattr(goot, var, None)
            if value:
                print(f"   ✅ {var} configurado")
            else:
                print(f"   ❌ {var} NO configurado")
                missing.append(var)
        
        return len(missing) == 0
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def run_all_tests():
    """Ejecutar todos los tests"""
    print("=" * 50)
    print("SUITE DE PRUEBAS - Sistema WhatsApp CRM")
    print("=" * 50)
    
    results = []
    results.append(("Imports", test_imports()))
    results.append(("Blueprints", test_blueprints()))
    results.append(("Variables de Entorno", test_env_variables()))
    
    print("\n" + "=" * 50)
    print("RESUMEN DE PRUEBAS")
    print("=" * 50)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ TODOS LOS TESTS PASARON")
    else:
        print("❌ ALGUNOS TESTS FALLARON")
    print("=" * 50)
    
    return all_passed

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
```

### 5.3 Crear `tests/README.md`

**Archivo:** `tests/README.md`

```markdown
# Tests - Sistema WhatsApp CRM

## Ejecutar Tests

```bash
# Suite completa
python tests/test_sistema.py

# Tests específicos
python tests/test_chats_extended.py
python tests/test_dashboard.py
```

## Tests Disponibles

- `test_sistema.py` - Suite completa
- `test_backend.py` - Tests del backend
- `test_chats_extended.py` - Tests de API extendida
- `test_dashboard.py` - Tests del dashboard
```

---

## Paso 6: Documentación

### 6.1 Crear Carpeta docs

```powershell
New-Item -ItemType Directory -Path "docs"
```

### 6.2 Crear `README.md` Principal

**Archivo:** `README.md`

```markdown
# 📱 Sistema de Chatbot WhatsApp - CRM/ERP

Sistema completo de gestión de conversaciones de WhatsApp Business con chatbot interactivo, sistema de tickets y gestión de grupos, integrado con Microsoft Dataverse.

## 🎯 Características Principales

- ✅ Múltiples conexiones WhatsApp simultáneas
- ✅ Sistema de menú interactivo para WhatsApp (4 opciones)
- ✅ Gestión de tickets desde conversaciones
- ✅ Grupos de categorización con permisos por rol
- ✅ Frontend responsive para móvil y desktop
- ✅ Roles y permisos (Administrador/Usuario)
- ✅ API REST completa para todas las entidades

## 📚 Documentación

Ver carpeta [docs/](docs/) para documentación completa.

## 🚀 Inicio Rápido

### 1. Clonar repositorio
```bash
git clone [URL_REPOSITORIO]
cd BIN
```

### 2. Configurar entorno virtual
```powershell
python -m venv venv_clean
.\venv_clean\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
Crear archivo `.env` con las credenciales necesarias (ver `.env.example`)

### 4. Iniciar backend
```powershell
.\iniciar_backend.ps1
```

### 5. Iniciar frontend
```powershell
.\iniciar.ps1
```

## 📖 Más Información

Ver [docs/INICIO_RAPIDO.md](docs/INICIO_RAPIDO.md) para guía detallada.

## 📄 Licencia

Propietario - Todos los derechos reservados
```

### 6.3 Crear Documentación Adicional

Ver estructura en carpeta `docs/` para crear:
- `INICIO_RAPIDO.md`
- `GUIA_SISTEMA_CHATBOT.md`
- `GUIA_CREAR_TABLAS_VISUAL.md`
- `INDICE_DOCUMENTACION.md`
- etc.

---

## Paso 7: Configurar Dataverse

### 7.1 Crear Tablas en Dataverse

Acceder a [Power Apps](https://make.powerapps.com) y crear las siguientes tablas:

#### Tabla 1: `cr321_chats` (Conversaciones)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| cr321_chatid | GUID (Primary Key) | ID único del chat |
| cr321_phone | Texto | Número de teléfono |
| cr321_name | Texto | Nombre del contacto |
| cr321_grupo | Texto | Grupo asignado |
| cr321_lastmessage | Texto | Último mensaje |
| cr321_lastmessagetime | Fecha/Hora | Timestamp del último mensaje |

#### Tabla 2: `cr321_grupos` (Grupos)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| cr321_grupoid | GUID (Primary Key) | ID único del grupo |
| cr321_nombre | Texto | Nombre del grupo |
| cr321_tipo | Opción | Tipo A/B (462410000/462410001) |
| cr321_descripcion | Texto | Descripción del grupo |

#### Tabla 3: `cr321_estados` (Estados de Tickets)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| cr321_estadoid | GUID (Primary Key) | ID único del estado |
| cr321_nombre | Texto | Nombre del estado |
| cr321_descripcion | Texto | Descripción del estado |

#### Tabla 4: `cr321_tickets` (Sistema de Tickets)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| cr321_ticketid | GUID (Primary Key) | ID único del ticket |
| cr321_titulo | Texto | Título del ticket |
| cr321_descripcion | Texto Multilínea | Descripción del ticket |
| cr321_chatid | Lookup → cr321_chats | Chat relacionado |
| cr321_estadoid | Lookup → cr321_estados | Estado actual |
| cr321_prioridad | Opción | Alta/Media/Baja |

#### Tabla 5: `cr321_usuario_grupos` (Relaciones Usuario-Grupo)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| cr321_usuariogrupoid | GUID (Primary Key) | ID único |
| cr321_usuarioid | Lookup → systemuser | Usuario |
| cr321_grupoid | Lookup → cr321_grupos | Grupo |

### 7.2 Ejecutar Script de Inicialización

```powershell
python init_dataverse.py
```

Esto creará:
- 4 grupos tipo A (SERVICIOS, COTIZACIONES, SOPORTE, GENERAL)
- 6 estados de tickets (NUEVO, EN_PROCESO, ESPERANDO, RESUELTO, CERRADO, CANCELADO)

---

## Paso 8: Iniciar Sistema

### 8.1 Instalar Dependencias

```powershell
# Activar entorno virtual
.\venv_clean\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
```

### 8.2 Iniciar Backend

```powershell
# Terminal 1
.\iniciar_backend.ps1
```

El backend estará disponible en: `http://localhost:5000`

### 8.3 Iniciar Frontend

```powershell
# Terminal 2
.\iniciar.ps1
```

### 8.4 Configurar Webhook de WhatsApp

1. Ir a [Meta for Developers](https://developers.facebook.com)
2. Seleccionar tu app de WhatsApp Business
3. Configurar webhook:
   - **URL:** `https://tu-dominio.com/webhook`
   - **Verify Token:** El valor de `VERIFY_TOKEN` en `.env`
   - **Eventos:** Marcar `messages`
4. Guardar y verificar

### 8.5 Probar el Sistema

1. **Login:** Acceder con credenciales de Azure AD
2. **Ver Conversaciones:** Lista de chats activos
3. **Enviar Mensaje:** Enviar mensaje de prueba
4. **Probar Menú:** Enviar mensaje al webhook y responder con opciones 1-4

---

## ✅ Checklist de Implementación

- [ ] Configuración inicial
  - [ ] Crear entorno virtual
  - [ ] Crear archivo `.env`
  - [ ] Instalar dependencias
- [ ] Backend
  - [ ] Crear `goot.py` con variables de entorno
  - [ ] Crear `back.py` servidor principal
  - [ ] Crear todos los Blueprints en `api/`
  - [ ] Probar servidor: `python backend/back.py`
- [ ] Frontend
  - [ ] Crear `main.py`
  - [ ] Crear componentes UI
  - [ ] Configurar `config.py`
  - [ ] Probar frontend: `python mobile/main.py`
- [ ] Dataverse
  - [ ] Crear 5 tablas en Power Apps
  - [ ] Ejecutar `init_dataverse.py`
  - [ ] Verificar datos iniciales
- [ ] WhatsApp
  - [ ] Configurar webhook en Meta for Developers
  - [ ] Probar verificación de webhook
  - [ ] Probar envío/recepción de mensajes
  - [ ] Probar menú interactivo
- [ ] Tests
  - [ ] Ejecutar `test_sistema.py`
  - [ ] Verificar que todos los tests pasen
- [ ] Documentación
  - [ ] Crear README.md
  - [ ] Crear guías en `docs/`
  - [ ] Documentar APIs

---

## 📞 Soporte

Para más información, consultar:
- [INICIO_RAPIDO.md](docs/INICIO_RAPIDO.md)
- [GUIA_SISTEMA_CHATBOT.md](docs/GUIA_SISTEMA_CHATBOT.md)
- [INDICE_DOCUMENTACION.md](docs/INDICE_DOCUMENTACION.md)

---

**Última actualización:** Febrero 2026  
**Versión del sistema:** 3.0.0
