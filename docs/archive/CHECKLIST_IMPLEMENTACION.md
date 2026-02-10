# ✅ Checklist de Implementación - Sistema Chatbot WhatsApp

## 📋 Pre-requisitos

### Accesos y Credenciales
- [ ] Cuenta de WhatsApp Business API activa
- [ ] Access Token de WhatsApp
- [ ] Phone Number ID(s) de WhatsApp
- [ ] Verify Token configurado
- [ ] Acceso a Microsoft Dataverse
- [ ] Azure AD App Registration (Client ID, Client Secret, Tenant ID)
- [ ] URL de Dataverse

### Herramientas
- [ ] Python 3.8+ instalado
- [ ] Git instalado
- [ ] Editor de código (VS Code recomendado)
- [ ] Postman o similar para pruebas de API
- [ ] Acceso a Power Apps (para crear tablas)

---

## 🗄️ Paso 1: Configurar Dataverse

### Crear Tablas Nuevas
Seguir instrucciones en `crear_tablas_dataverse.ps1`

#### Tabla: cr321_grupos
- [ ] Crear tabla en Power Apps
- [ ] Campo: cr321_idgrupo (int)
- [ ] Campo: cr321_nombre (text, 100)
- [ ] Campo: cr321_tipo (choice: 462410000=A, 462410001=B, 462410002=C)
- [ ] Campo: cr321_descripcion (text, 500)
- [ ] Publicar tabla

#### Tabla: cr321_estados
- [ ] Crear tabla en Power Apps
- [ ] Campo: cr321_idestado (int)
- [ ] Campo: cr321_nombre (text, 100)
- [ ] Campo: cr321_descripcion (text, 500)
- [ ] Publicar tabla

#### Tabla: cr321_tickets
- [ ] Crear tabla en Power Apps
- [ ] Campo: cr321_idticket (int)
- [ ] Campo: cr321_fromnombre (text, 100)
- [ ] Campo: cr321_telefono (text, 20)
- [ ] Campo: cr321_empresa (text, 200)
- [ ] Campo: cr321_descripcion (text multilínea, 2000)
- [ ] Campo: cr321_tipo (choice: 462410000=soporte, 462410001=cotizacion, 462410002=informacion, 462410003=atencion_agente)
- [ ] Campo: cr321_estado (int)
- [ ] Campo: cr321_grupoid (lookup a cr321_grupos)
- [ ] Campo: cr321_fechacreacion (datetime)
- [ ] Campo: cr321_fechaactualizacion (datetime)
- [ ] Publicar tabla

#### Tabla: cr321_usuario_grupos
- [ ] Crear tabla en Power Apps
- [ ] Campo: cr321_usuarioid (lookup a cr321_usuarios)
- [ ] Campo: cr321_grupoid (lookup a cr321_grupos)
- [ ] Publicar tabla

### Verificar Tablas Existentes
- [ ] cr321_usuarios (debe existir)
- [ ] cr321_chats00 (debe existir)
- [ ] cr321_contactos (debe existir)
- [ ] cr321_chatboots (debe existir)

---

## ⚙️ Paso 2: Configurar Backend

### Variables de Entorno
Crear/editar archivo `.env` en la raíz del proyecto:

```env
# WhatsApp Business API
ACCESS_TOKEN=tu_token_whatsapp
PHONE_NUMBER_ID=tu_phone_id_principal
PHONE_NUMBER_ID0=id_conexion_1
PHONE_NUMBER_ID1=id_conexion_2
PHONE_NUMBER_ID2=id_conexion_3  # Opcional
VERIFY_TOKEN=tu_verify_token_secreto

# Azure AD / Dataverse
TENANT_ID=tu_tenant_azure
CLIENT_ID=tu_client_id
CLIENT_SECRET=tu_client_secret
DATAVERSE_URL=https://tu-entorno.crm.dynamics.com

# Otros
ENTITY_SET=cr321_chats00es
ENTITY_SET_USR=cr321_usuarioses
AZURE_REGION=tu_region
```

Checklist de configuración:
- [ ] Archivo .env creado
- [ ] ACCESS_TOKEN configurado
- [ ] PHONE_NUMBER_ID configurado
- [ ] VERIFY_TOKEN configurado (debe ser seguro/aleatorio)
- [ ] TENANT_ID configurado
- [ ] CLIENT_ID configurado
- [ ] CLIENT_SECRET configurado
- [ ] DATAVERSE_URL configurado

### Instalar Dependencias
```powershell
pip install -r requirements.txt
```

- [ ] Dependencias instaladas sin errores

---

## 🔧 Paso 3: Inicializar Datos

### Ejecutar Script de Inicialización
```powershell
python init_dataverse.py
```

Verificar que se crearon:
- [ ] 4 grupos tipo A (Solicitud Ticket, Cotizaciones, Información, Atención Agente)
- [ ] 6 estados (Nuevo, En Proceso, Pendiente Cliente, Resuelto, Cerrado, Cancelado)

### Crear Usuario Administrador
Si no existe, crear en Dataverse o usar API:
```powershell
# POST /register (si la ruta está habilitada)
# O crear directamente en Power Apps
```

- [ ] Usuario administrador creado
- [ ] Usuario de prueba creado

### Asignar Usuarios a Grupos
Usando Postman o similar:
```json
POST http://localhost:5000/api/usuario-grupos
{
  "usuario_id": "guid-del-usuario-admin",
  "grupo_id": "guid-del-grupo-1"
}
```

- [ ] Usuario admin asignado a grupo 1
- [ ] Usuario admin asignado a grupo 2
- [ ] Usuario admin asignado a grupo 3
- [ ] Usuario admin asignado a grupo 4
- [ ] Usuario de prueba asignado a grupo 1 (solo)

---

## 🌐 Paso 4: Configurar Webhook de WhatsApp

### En Meta for Developers (developers.facebook.com)

1. **Ir a tu App de WhatsApp Business**
   - [ ] Abrir app en Meta for Developers
   - [ ] Ir a sección "WhatsApp" → "Configuration"

2. **Configurar Webhook**
   - [ ] Callback URL: `https://tu-dominio.com/webhook`
   - [ ] Verify Token: Mismo que VERIFY_TOKEN en .env
   - [ ] Hacer clic en "Verify and save"
   - [ ] Verificación exitosa ✅

3. **Suscribirse a Eventos**
   - [ ] Seleccionar "messages"
   - [ ] Seleccionar "messaging_postbacks" (si está disponible)
   - [ ] Guardar

### Probar Webhook

Opción A: Usar ngrok para desarrollo local
```powershell
ngrok http 5000
# Usar URL de ngrok como Callback URL
```

Opción B: Usar Azure/servidor en producción
- [ ] Backend desplegado en servidor
- [ ] URL HTTPS configurada
- [ ] Webhook configurado con URL de producción

**Prueba:**
- [ ] Enviar mensaje de prueba desde WhatsApp
- [ ] Verificar en logs del backend que se recibió
- [ ] Verificar que bot responde con menú

---

## 🚀 Paso 5: Iniciar Sistema

### Backend
```powershell
cd backend
python back.py
```

Verificaciones:
- [ ] Backend inicia sin errores
- [ ] Mensaje de inicio muestra todas las variables
- [ ] Puerto 5000 está escuchando
- [ ] No hay errores de autenticación con Dataverse

### Frontend
```powershell
cd mobile
python main.py
```

Verificaciones:
- [ ] Frontend abre en navegador
- [ ] Pantalla de login se muestra
- [ ] Se puede iniciar sesión con usuario admin
- [ ] Dashboard se carga correctamente

---

## 🧪 Paso 6: Pruebas Funcionales

### Prueba de Login
- [ ] Login con usuario admin exitoso
- [ ] Login con usuario normal exitoso
- [ ] Login con credenciales incorrectas muestra error

### Prueba de Grupos
- [ ] Admin ve selector con TODOS los grupos
- [ ] Usuario normal ve solo sus grupos asignados
- [ ] Filtrar por grupo funciona correctamente

### Prueba de Chats
- [ ] Se muestran conversaciones existentes
- [ ] Al hacer clic en chat, se abre detalle
- [ ] Historial de mensajes se carga
- [ ] Enviar mensaje funciona

### Prueba de Webhook WhatsApp
- [ ] Enviar "hola" desde WhatsApp → Recibe menú
- [ ] Seleccionar opción "1" → Sistema hace primera pregunta
- [ ] Responder pregunta → Sistema hace siguiente pregunta
- [ ] Completar flujo → Sistema confirma ticket creado
- [ ] Verificar en Dataverse que ticket se creó

### Prueba de APIs

**Grupos:**
```bash
GET http://localhost:5000/api/grupos
GET http://localhost:5000/api/grupos?tipo=A
```
- [ ] Lista de grupos devuelta correctamente

**Tickets:**
```bash
GET http://localhost:5000/api/tickets
GET http://localhost:5000/api/tickets?grupo=1
```
- [ ] Lista de tickets devuelta correctamente
- [ ] Filtros funcionan

**Estados:**
```bash
GET http://localhost:5000/api/estados
```
- [ ] Lista de estados devuelta correctamente

---

## 📊 Paso 7: Validación Final

### Flujo Completo End-to-End

1. **Cliente en WhatsApp:**
   - [ ] Cliente envía primer mensaje
   - [ ] Recibe menú con 4 opciones
   - [ ] Selecciona opción 1 (Solicitud Ticket)
   - [ ] Responde a pregunta 1 (Nombre)
   - [ ] Responde a pregunta 2 (Empresa)
   - [ ] Responde a pregunta 3 (Descripción)
   - [ ] Recibe confirmación con número de ticket

2. **En Dataverse:**
   - [ ] Ticket existe en tabla cr321_tickets
   - [ ] idticket es consecutivo
   - [ ] Todos los campos están llenos
   - [ ] Estado es 1 (Nuevo)
   - [ ] Tipo es 462410000 (Soporte)

3. **Agente en Frontend:**
   - [ ] Ve el nuevo chat en la lista
   - [ ] Puede abrir el chat
   - [ ] Ve todo el historial
   - [ ] Puede responder
   - [ ] Su respuesta llega a WhatsApp del cliente

### Verificar Logs
- [ ] Backend logs sin errores
- [ ] Frontend logs sin errores
- [ ] No hay excepciones no manejadas

---

## 🎓 Paso 8: Capacitación

### Documentación para Usuarios
- [ ] Leer [GUIA_SISTEMA_CHATBOT.md](GUIA_SISTEMA_CHATBOT.md)
- [ ] Leer [README.md](README.md)
- [ ] Leer [RESUMEN_EJECUTIVO.md](RESUMEN_EJECUTIVO.md)

### Capacitación de Agentes
- [ ] Cómo iniciar sesión
- [ ] Cómo usar selector de grupos
- [ ] Cómo ver y responder chats
- [ ] Cómo interpretar estados de tickets

### Capacitación de Administradores
- [ ] Gestión de usuarios
- [ ] Asignación de usuarios a grupos
- [ ] Creación de nuevos grupos
- [ ] Gestión de estados

---

## 🚨 Paso 9: Monitoreo y Mantenimiento

### Configurar Monitoreo
- [ ] Logs del backend guardándose correctamente
- [ ] Sistema de alertas configurado (opcional)
- [ ] Backup de Dataverse programado

### Verificaciones Diarias
- [ ] Backend está corriendo
- [ ] Frontend accesible
- [ ] Webhook respondiendo
- [ ] Mensajes de WhatsApp llegando

### Verificaciones Semanales
- [ ] Revisar logs por errores
- [ ] Verificar tickets creados vs resueltos
- [ ] Revisar tiempos de respuesta

---

## 📝 Paso 10: Mejoras Futuras

Ver archivo [MEJORAS_SUGERIDAS.md](MEJORAS_SUGERIDAS.md) para:
- [ ] Redis para estados persistentes
- [ ] Notificaciones por email
- [ ] Dashboard con métricas
- [ ] Sistema de asignación de agentes
- [ ] Soporte multimedia
- [ ] Integración con IA

---

## 🆘 Troubleshooting

### Problema: Backend no inicia
- [ ] Verificar que Python 3.8+ está instalado
- [ ] Verificar que todas las dependencias están instaladas
- [ ] Verificar que .env tiene todas las variables
- [ ] Verificar logs de error en consola

### Problema: Webhook no recibe mensajes
- [ ] Verificar que URL está correcta en Meta for Developers
- [ ] Verificar que VERIFY_TOKEN coincide
- [ ] Verificar que backend está accesible públicamente (usar ngrok para pruebas)
- [ ] Verificar logs del backend al enviar mensaje

### Problema: No se pueden ver chats
- [ ] Verificar que usuario está asignado a al menos un grupo
- [ ] Verificar que token JWT es válido
- [ ] Verificar logs del backend
- [ ] Verificar que hay datos en cr321_chats00

### Problema: No se crean tickets
- [ ] Verificar que tabla cr321_tickets existe
- [ ] Verificar logs del backend al completar flujo
- [ ] Verificar permisos de Dataverse
- [ ] Verificar que función create_ticket_from_conversation no tiene errores

---

## ✅ Checklist Final

- [ ] ✅ Todas las tablas creadas en Dataverse
- [ ] ✅ Datos iniciales cargados (grupos y estados)
- [ ] ✅ Usuarios creados y asignados a grupos
- [ ] ✅ Backend corriendo sin errores
- [ ] ✅ Frontend accesible y funcional
- [ ] ✅ Webhook configurado y respondiendo
- [ ] ✅ Flujo completo de ticket probado y funcional
- [ ] ✅ Documentación leída y comprendida
- [ ] ✅ Capacitación completada

---

## 🎉 ¡Sistema Listo para Producción!

Una vez completados todos los pasos, el sistema está **completamente operativo** y listo para:
- Recibir mensajes de WhatsApp 24/7
- Crear tickets automáticamente
- Gestionar múltiples agentes por grupos
- Monitorear conversaciones en tiempo real

**¡Felicidades por implementar un sistema empresarial completo de chatbot WhatsApp!** 🚀

---

**Última actualización:** Febrero 2026  
**Versión del checklist:** 1.0
