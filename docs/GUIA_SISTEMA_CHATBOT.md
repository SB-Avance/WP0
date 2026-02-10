# 📱 Sistema de Chatbot WhatsApp - Guía Completa

## 🎯 Descripción General

Sistema completo de chatbot multicanal WhatsApp integrado con Dataverse, desarrollado con:
- **Backend**: Python + Flask
- **Frontend**: Python + Flet
- **Base de Datos**: Microsoft Dataverse
- **API Externa**: WhatsApp Business API

## 🏗️ Arquitectura del Sistema

### Tablas en Dataverse

#### 1. **cr321_usuarios** (Existente)
Gestión de usuarios del sistema
- `cr321_usuariosid` (PK, GUID)
- `cr321_idusuario` (int, consecutivo)
- `cr321_nombre` (string)
- `cr321_correo` (string)
- `cr321_clave` (string, hash)
- `cr321_rol` (int: 462410000=usuario, 462410001=administrador)

#### 2. **cr321_grupos** (Nueva)
Grupos de categorización de chats
- `cr321_grupoid` (PK, GUID)
- `cr321_idgrupo` (int, consecutivo)
- `cr321_nombre` (string)
- `cr321_tipo` (int: 462410000=A, 462410001=B, 462410002=C)
- `cr321_descripcion` (string)

**Grupos Tipo A** (Opciones de menú principal):
1. Solicitud Ticket
2. Cotizaciones
3. Información
4. Atención de Agente

#### 3. **cr321_usuario_grupos** (Nueva)
Relación muchos a muchos entre usuarios y grupos
- `cr321_usuario_grupoid` (PK, GUID)
- `cr321_usuarioid` (FK a cr321_usuarios)
- `cr321_grupoid` (FK a cr321_grupos)

#### 4. **cr321_tickets** (Nueva)
Sistema de tickets generados desde WhatsApp
- `cr321_ticketid` (PK, GUID)
- `cr321_idticket` (int, consecutivo)
- `cr321_fromnombre` (string)
- `cr321_telefono` (string)
- `cr321_empresa` (string)
- `cr321_descripcion` (string)
- `cr321_tipo` (int: 462410000=soporte, 462410001=cotización, 462410002=información, 462410003=atención agente)
- `cr321_estado` (int, FK a cr321_estados)
- `cr321_grupoid` (GUID, FK a cr321_grupos)
- `cr321_fechacreacion` (datetime)
- `cr321_fechaactualizacion` (datetime)

#### 5. **cr321_estados** (Nueva)
Estados de tickets
- `cr321_estadoid` (PK, GUID)
- `cr321_idestado` (int, consecutivo)
- `cr321_nombre` (string)
- `cr321_descripcion` (string)

**Estados iniciales**:
1. Nuevo
2. En Proceso
3. Pendiente Cliente
4. Resuelto
5. Cerrado
6. Cancelado

#### 6. **cr321_chats00** (Existente)
Almacén de mensajes de WhatsApp

#### 7. **cr321_contactos** (Existente)
Contactos de WhatsApp

#### 8. **cr321_chatboots** (Existente)
Configuración de chatbots

## 🔌 APIs Backend

### Grupos
- `GET /api/grupos` - Listar grupos (filtro opcional: ?tipo=A)
- `GET /api/grupos/<idgrupo>` - Obtener grupo específico
- `POST /api/grupos` - Crear grupo
  ```json
  {
    "nombre": "Soporte Técnico",
    "tipo": "A",
    "descripcion": "Grupo para soporte"
  }
  ```
- `PUT /api/grupos/<idgrupo>` - Actualizar grupo
- `DELETE /api/grupos/<idgrupo>` - Eliminar grupo

### Estados
- `GET /api/estados` - Listar estados
- `POST /api/estados` - Crear estado
  ```json
  {
    "nombre": "Nuevo",
    "descripcion": "Ticket nuevo"
  }
  ```
- `PUT /api/estados/<idestado>` - Actualizar estado
- `DELETE /api/estados/<idestado>` - Eliminar estado

### Tickets
- `GET /api/tickets` - Listar tickets (filtros: ?grupo=1&estado=1&tipo=soporte)
- `GET /api/tickets/<idticket>` - Obtener ticket específico
- `POST /api/tickets` - Crear ticket
  ```json
  {
    "fromnombre": "Juan Pérez",
    "telefono": "+525512345678",
    "empresa": "ACME Corp",
    "descripcion": "Problema con servidor",
    "tipo": "soporte",
    "grupo_id": "guid-del-grupo",
    "estado": 1
  }
  ```
- `PUT /api/tickets/<idticket>` - Actualizar ticket
- `DELETE /api/tickets/<idticket>` - Eliminar ticket

### Usuario-Grupos
- `GET /api/usuario-grupos` - Listar relaciones
- `GET /api/usuario-grupos/usuario/<usuario_id>` - Grupos de un usuario
- `GET /api/usuario-grupos/grupo/<grupo_id>` - Usuarios de un grupo
- `POST /api/usuario-grupos` - Asignar usuario a grupo
  ```json
  {
    "usuario_id": "guid-usuario",
    "grupo_id": "guid-grupo"
  }
  ```
- `DELETE /api/usuario-grupos/<relacion_id>` - Eliminar relación

### Webhook WhatsApp
- `GET /webhook` - Verificación de webhook
- `POST /webhook` - Recibir mensajes de WhatsApp

## 🤖 Sistema de Menú Interactivo

### Flujo de Conversación

1. **Usuario inicia conversación** → Recibe menú principal
2. **Usuario selecciona opción** (1-4) → Inicia flujo específico
3. **Sistema hace preguntas** → Recopila información
4. **Sistema crea ticket** → Confirma con número de ticket
5. **Regresa al menú** → Usuario puede hacer otra solicitud

### Menú Principal

```
¡Bienvenido! Por favor seleccione una opción:

1. Solicitud Ticket
2. Cotizaciones
3. Información
4. Solicitar atención de agente
```

### Opción 1: Solicitud Ticket
1. Pregunta: "Por favor, indique su nombre completo:"
2. Pregunta: "¿De qué empresa nos contacta?"
3. Pregunta: "Describa su solicitud de soporte:"
4. Respuesta: "¡Gracias! Su solicitud ha sido registrada con el ticket #123..."

### Opción 2: Cotizaciones
1. Pregunta: "Por favor, indique su nombre completo:"
2. Pregunta: "¿De qué empresa nos contacta?"
3. Pregunta: "Describa el producto, marca y modelo si lo tiene:"
4. Respuesta: "¡Gracias! Su cotización ha sido registrada con el ticket #124..."

### Opción 3: Información
- Respuesta inmediata con información general
- No crea ticket
- Regresa al menú

### Opción 4: Atención de Agente
1. Pregunta: "Por favor, indique su nombre para conectarlo con un agente:"
2. Crea ticket tipo "atención_agente"
3. Notifica al sistema para asignación de agente

## 🎨 Frontend - Roles y Permisos

### ROL: Administrador
- **Vista de grupos**: Puede ver TODOS los grupos o filtrar por grupo específico
- **Selector de grupos**: Dropdown con todos los grupos disponibles
- **Gestión de usuarios**: Acceso completo a administración de usuarios
- **Chats visibles**: Todos los chats de todos los grupos

### ROL: Usuario
- **Vista de grupos**: Solo ve chats de los grupos asignados
- **Selector de grupos**: Solo grupos a los que pertenece
- **Chats visibles**: Solo chats de sus grupos asignados

### Interfaz
```
┌─────────────────────────────────────┐
│ Sidebar (izq)    │ Área Principal   │
│                  │                  │
│ - Cambiar usuario│ [Filtro Grupos]  │
│ - Dashboard      │  ┌──────────────┐│
│ - Chats          │  │ Chat 1       ││
│ - Usuarios       │  │ Chat 2       ││
│ - Configuración  │  │ Chat 3       ││
│ - Cerrar Sesión  │  └──────────────┘│
└─────────────────────────────────────┘
```

## 🚀 Instalación y Configuración

### 1. Configurar Variables de Entorno (.env)
```env
ACCESS_TOKEN=tu_token_whatsapp
PHONE_NUMBER_ID=tu_phone_id
PHONE_NUMBER_ID0=id_conexion_1
PHONE_NUMBER_ID1=id_conexion_2
VERIFY_TOKEN=tu_verify_token
TENANT_ID=tu_tenant_azure
CLIENT_ID=tu_client_id
CLIENT_SECRET=tu_client_secret
DATAVERSE_URL=https://tu-entorno.crm.dynamics.com
```

### 2. Crear Tablas en Dataverse

**Opción A: Power Platform Admin Center**
1. Crear entidades personalizadas con prefijo `cr321_`
2. Agregar campos según especificaciones arriba
3. Configurar relaciones entre tablas

**Opción B: API Web de Dataverse**
(Usar herramientas como Postman o scripts PowerShell)

### 3. Inicializar Datos Base
```bash
cd c:\VS\BIN
python init_dataverse.py
```

Este script crea:
- 4 grupos tipo A (opciones del menú)
- 6 estados de tickets

### 4. Asignar Usuarios a Grupos
```bash
# Usando cURL o Postman
POST http://localhost:5000/api/usuario-grupos
{
  "usuario_id": "guid-del-usuario",
  "grupo_id": "guid-del-grupo"
}
```

### 5. Configurar Webhook de WhatsApp

1. En Meta for Developers, configurar webhook:
   - URL: `https://tu-dominio.com/webhook`
   - Token de verificación: Mismo que VERIFY_TOKEN en .env

2. Suscribirse a eventos:
   - messages
   - messaging_postbacks

### 6. Iniciar Backend
```bash
cd backend
python back.py
```

El servidor iniciará en `http://localhost:5000`

### 7. Iniciar Frontend
```bash
cd mobile
python main.py
```

La aplicación abrirá en navegador en `http://localhost:8501`

## 📊 Flujo de Datos

### Mensaje entrante de WhatsApp
```
WhatsApp → Webhook → back.py/webhook.py → 
process_menu_response() → create_ticket_from_conversation() → 
Dataverse (cr321_tickets) → send_whatsapp_message() → WhatsApp
```

### Usuario visualiza chats en Frontend
```
Frontend → GET /api/conversations?group=X → 
back.py → Dataverse (cr321_chats00) → 
Filtrar por grupo y rol → JSON → Frontend
```

## 🔧 Mejoras Implementadas

### Backend
1. ✅ APIs completas para CRUD de grupos, estados, tickets y relaciones
2. ✅ Sistema de menú conversacional automático
3. ✅ Creación automática de tickets desde WhatsApp
4. ✅ Manejo de estado de conversaciones
5. ✅ Filtros por grupo y rol

### Frontend
1. ✅ Selector de grupos con filtrado
2. ✅ Interfaz responsive para móvil
3. ✅ Control de permisos por rol (admin/usuario)
4. ✅ Visualización de chats por grupo
5. ✅ Sistema de notificaciones

### Webhook
1. ✅ Verificación de webhook
2. ✅ Procesamiento de mensajes entrantes
3. ✅ Sistema de menú interactivo con 4 opciones
4. ✅ Recopilación de datos por pasos
5. ✅ Creación automática de tickets

## 📝 Próximas Mejoras Sugeridas

### Corto Plazo
1. 🔄 Implementar Redis para gestión de estados de conversación (escalabilidad)
2. 📧 Notificaciones por email cuando se crea un ticket
3. 🔔 Notificaciones push en frontend para nuevos mensajes
4. 📎 Soporte para adjuntos (imágenes, documentos) en WhatsApp

### Mediano Plazo
1. 🤖 Integración con IA (Azure OpenAI/GPT) para respuestas automáticas
2. 📊 Dashboard con métricas y KPIs de tickets
3. 🎫 Sistema de asignación automática de tickets a agentes
4. 🔍 Búsqueda avanzada de tickets y conversaciones

### Largo Plazo
1. 📱 App móvil nativa (iOS/Android)
2. 🌐 Soporte multiidioma
3. 📈 Análisis de sentimientos en conversaciones
4. 🔗 Integración con CRM/ERP externos (Salesforce, SAP, etc.)

## 🐛 Solución de Problemas

### Error: "No se pudo autenticar con Dataverse"
- Verificar variables en .env (TENANT_ID, CLIENT_ID, CLIENT_SECRET)
- Verificar permisos de la aplicación en Azure AD
- Regenerar CLIENT_SECRET si expiró

### Error: "Webhook no recibe mensajes"
- Verificar URL del webhook en Meta for Developers
- Verificar que VERIFY_TOKEN coincida
- Revisar logs del backend: `python back.py`

### Error: "Usuario no puede ver chats de su grupo"
- Verificar asignación de usuario a grupo en `cr321_usuario_grupos`
- Verificar rol del usuario (debe estar correctamente asignado)

### Frontend no se conecta al backend
- Verificar API_BASE_URL en `mobile/config.py`
- Verificar que backend esté corriendo
- Revisar configuración de CORS en `back.py`

## 📞 Contacto y Soporte

Para más información o soporte, contactar al equipo de desarrollo.

---

**Versión del Sistema**: 2.0  
**Última Actualización**: Febrero 2026  
**Desarrollado con**: Python, Flask, Flet, Dataverse, WhatsApp API
