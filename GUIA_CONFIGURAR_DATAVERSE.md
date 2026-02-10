# 🚀 GUÍA: Configurar Dataverse Paso a Paso

**Fecha:** 9 de febrero de 2026  
**Objetivo:** Configurar Microsoft Dataverse desde cero para el CRM WhatsApp

---

## 📋 PASO 1: Crear Cuenta de Azure

### 1.1 Registro
1. Ir a: https://azure.microsoft.com
2. Clic en "Cuenta gratuita" o "Iniciar sesión"
3. Usar cuenta Microsoft (Outlook, Hotmail, etc.)
4. **IMPORTANTE:** Apuntar el **email** usado

### 1.2 Suscripción
- Azure te da **$200 USD gratis** por 30 días
- Suficiente para desarrollo y pruebas
- No se cobra hasta que actives pago

---

## 📋 PASO 2: Crear App Registration (Azure AD)

### 2.1 Ir a Azure Portal
1. Abrir: https://portal.azure.com
2. Buscar: "Azure Active Directory" o "Microsoft Entra ID"
3. En el menú lateral: **App registrations**

### 2.2 Crear nueva aplicación
1. Clic en **"+ New registration"**
2. Llenar formulario:
   ```
   Name: WhatsAppCRM-App
   Supported account types: Single tenant
   Redirect URI: (dejar vacío por ahora)
   ```
3. Clic en **"Register"**

### 2.3 Obtener credenciales (GUARDAR)
Una vez creada la app, verás:

```
Application (client) ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
Directory (tenant) ID: yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy
```

**✏️ COPIAR ESTOS VALORES** → Los necesitarás en el .env

### 2.4 Crear Client Secret
1. En el menú lateral de la app: **Certificates & secrets**
2. Clic en **"+ New client secret"**
3. Descripción: "WhatsAppCRM Secret"
4. Expires: 24 meses
5. Clic en **"Add"**
6. **⚠️ IMPORTANTE:** Copiar el **VALUE** (no el Secret ID)
   - Solo se muestra UNA VEZ
   - Si lo pierdes, debes crear otro

```
Value: ABC123def456ghi789jkl012mno345pqr678stu901
```

**✏️ COPIAR ESTE VALOR** → CLIENT_SECRET en .env

---

## 📋 PASO 3: Crear Entorno de Dataverse

### 3.1 Ir a Power Platform Admin Center
1. Abrir: https://admin.powerplatform.microsoft.com
2. Iniciar sesión con la misma cuenta de Azure

### 3.2 Crear Environment
1. En el menú lateral: **Environments**
2. Clic en **"+ New"**
3. Llenar formulario:
   ```
   Name: WhatsAppCRM-Dev
   Type: Sandbox (para desarrollo)
   Region: (seleccionar tu región, ej: United States)
   Purpose: Desarrollo del CRM WhatsApp
   Create a database: YES ✅
   ```
4. En la sección de base de datos:
   ```
   Language: Spanish
   Currency: USD o tu moneda local
   Enable Dynamics 365 apps: NO
   Deploy sample apps and data: NO
   ```
5. Clic en **"Save"**

⏳ **Esperar 5-10 minutos** mientras se crea el entorno

### 3.3 Obtener URL de Dataverse
Una vez creado:
1. Entrar al entorno (clic en el nombre)
2. Ir a **"Settings"** → **"Resources"** → **"All legacy settings"**
3. O más fácil: Ir a **Environments** y copiar la **Environment URL**

```
URL: https://org12345678.crm.dynamics.com
```

**✏️ COPIAR ESTA URL** → DATAVERSE_URL en .env

---

## 📋 PASO 4: Dar Permisos a la App

### 4.1 Volver a Azure Portal
1. Ir a: https://portal.azure.com
2. Buscar: **Azure Active Directory**
3. **App registrations** → Tu app "WhatsAppCRM-App"

### 4.2 Agregar permisos de Dataverse
1. En el menú lateral: **API permissions**
2. Clic en **"+ Add a permission"**
3. Tab: **APIs my organization uses**
4. Buscar: **"Dynamics CRM"** o **"Dataverse"**
5. Seleccionar: **Dynamics CRM**
6. Tipo de permiso: **Delegated permissions**
7. Marcar: **user_impersonation**
8. Clic en **"Add permissions"**

### 4.3 Grant admin consent
1. Clic en **"Grant admin consent for [tu organización]"**
2. Confirmar: **Yes**
3. Esperar que aparezca checkmark verde ✅

---

## 📋 PASO 5: Configurar Usuario en Dataverse

### 5.1 Ir a Power Platform Admin Center
1. Abrir: https://admin.powerplatform.microsoft.com
2. **Environments** → Tu entorno "WhatsAppCRM-Dev"
3. Clic en **"Settings"**

### 5.2 Agregar tu usuario
1. **Users + permissions** → **Users**
2. Clic en **"+ Add user"**
3. Buscar tu email de Azure
4. Seleccionar y agregar
5. Asignar rol: **System Administrator**

---

## 📋 PASO 6: Actualizar archivo .env

Ahora que tienes todos los valores, edita el archivo `.env`:

```bash
# ========== MICROSOFT AZURE AD ==========
TENANT_ID=yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy    # Del PASO 2.3
CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx    # Del PASO 2.3
CLIENT_SECRET=ABC123def456ghi789jkl012mno345pqr678stu901  # Del PASO 2.4

# ========== MICROSOFT DATAVERSE ==========
DATAVERSE_URL=https://org12345678.crm.dynamics.com  # Del PASO 3.3
ENTITY_SET=cr321_adatawp0
ENTITY_SET_USR=cr321_usuarios
```

**Guardar el archivo**

---

## 📋 PASO 7: Probar Conexión

### 7.1 Ejecutar script de prueba
```powershell
python -c "from backend.goot import get_token; token = get_token(); print('✅ Token obtenido!' if token else '❌ Error')"
```

Si ves `✅ Token obtenido!` → ¡Éxito! Conexión funciona

### 7.2 Si hay error
1. Verificar que las credenciales en .env son correctas
2. Verificar que el usuario tiene rol de System Administrator
3. Verificar que la app tiene permisos de Dataverse
4. Esperar 5-10 minutos (propagación de cambios)

---

## 📋 PASO 8: Crear las 12 Tablas en Dataverse

### 8.1 Método automático (Recomendado)
1. Usar el script PowerShell:
   ```powershell
   .\crear_tablas_dataverse.ps1
   ```
   ⚠️ **NOTA:** Este script aún está en desarrollo

### 8.2 Método manual (Paso a paso)
Seguir la guía detallada:
```
Ver: docs\GUIA_COMPLETA_CREAR_TABLAS_DATAVERSE.md
```

Esta guía tiene:
- Instrucciones visuales con capturas
- 12 tablas definidas campo por campo
- Tipos de datos y configuraciones
- Relaciones (Lookups) entre tablas
- Diagramas ER completos

### 8.3 Lista de tablas a crear
```
1.  cr321_usuarios          → Usuarios del sistema
2.  cr321_grupos            → Grupos/Categorías
3.  cr321_estados           → Estados de tickets
4.  cr321_contacto          → Contactos de WhatsApp
5.  cr321_cuentadewhatsapp  → Cuentas de WhatsApp Business
6.  cr321_chatbot           → Configuración de chatbots
7.  cr321_template          → Templates de mensajes
8.  cr321_automatizaciones  → Reglas de automatización
9.  cr321_usuariogrupo      → Relación N:M usuarios-grupos
10. cr321_flows             → Flujos de conversación
11. cr321_ticket            → Tickets de soporte
12. cr321_adatawp0          → Mensajes de WhatsApp
```

---

## 📋 PASO 9: Inicializar Datos

Una vez creadas las tablas:

```powershell
python init_dataverse.py
```

Esto crea:
- ✅ 6 estados iniciales (NUEVO, EN_PROCESO, etc.)
- ✅ 4 grupos iniciales (SERVICIOS, COTIZACIONES, SOPORTE, GENERAL)
- ✅ Configuración básica del sistema

---

## 📋 PASO 10: Verificar Todo Funciona

### 10.1 Iniciar backend
```powershell
python backend\back.py
```

### 10.2 Probar endpoint
```powershell
curl http://localhost:5000/api/estados
```

Deberías ver:
```json
{
  "estados": [
    {"nombre": "NUEVO", "color": "#2196F3", ...},
    {"nombre": "EN_PROCESO", "color": "#FF9800", ...},
    ...
  ]
}
```

✅ **Si ves esto → ¡TODO FUNCIONA!**

---

## 📋 PASO 11: Configurar WhatsApp Business (Opcional)

Si quieres conectar WhatsApp real:

### 11.1 Crear cuenta Business
1. Ir a: https://business.facebook.com
2. Crear cuenta de negocio
3. Agregar producto: WhatsApp

### 11.2 Obtener credenciales
1. En Meta for Developers: https://developers.facebook.com
2. Crear app tipo "Business"
3. Agregar producto WhatsApp
4. Obtener:
   ```
   PHONE_NUMBER_ID=123456789012345
   ACCESS_TOKEN=tu-token-aqui
   ```

### 11.3 Actualizar .env
```bash
PHONE_NUMBER_ID=123456789012345
ACCESS_TOKEN=EAABsb...tu-token-largo-aqui
VERIFY_TOKEN=mi_token_secreto_webhook_2024  # Inventar uno propio
```

### 11.4 Configurar Webhook
1. En la app de Facebook: WhatsApp → Configuration
2. Webhook URL: `https://tu-dominio.com/webhook`
3. Verify Token: el mismo que pusiste en VERIFY_TOKEN
4. Subscribe to: `messages`

---

## ✅ CHECKLIST FINAL

Marca cada paso al completarlo:

```
☐ PASO 1: Cuenta de Azure creada
☐ PASO 2: App Registration creada y credenciales guardadas
☐ PASO 3: Entorno de Dataverse creado y URL obtenida
☐ PASO 4: Permisos de Dataverse agregados a la app
☐ PASO 5: Usuario agregado con rol System Administrator
☐ PASO 6: Archivo .env actualizado con todas las credenciales
☐ PASO 7: Conexión probada exitosamente (token obtenido)
☐ PASO 8: 12 tablas creadas en Dataverse
☐ PASO 9: Datos iniciales creados (estados y grupos)
☐ PASO 10: Backend funcionando y endpoints respondiendo
☐ PASO 11: WhatsApp Business configurado (opcional)
```

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### Error: "Invalid client secret"
- Verificar que copiaste el VALUE, no el Secret ID
- Crear un nuevo secret si es necesario

### Error: "Unauthorized" o "401"
- Verificar que el usuario tiene rol System Administrator
- Verificar que la app tiene permisos user_impersonation
- Esperar 10 minutos para propagación

### Error: "Dataverse 400"
- Verificar que DATAVERSE_URL es correcta
- Verificar que el entorno está activo
- Verificar que las tablas existen

### Error: "Table not found"
- Verificar que completaste el PASO 8 (crear tablas)
- Verificar nombres de tablas (deben empezar con cr321_)

---

## 📚 RECURSOS ADICIONALES

- Documentación de Azure AD: https://docs.microsoft.com/azure/active-directory
- Documentación de Dataverse: https://docs.microsoft.com/power-apps/maker/data-platform
- WhatsApp Business API: https://developers.facebook.com/docs/whatsapp
- Guía completa de tablas: `docs/GUIA_COMPLETA_CREAR_TABLAS_DATAVERSE.md`

---

## 🎯 TIEMPO ESTIMADO

- Experiencia previa con Azure: **1-2 horas**
- Primera vez con Azure: **3-4 horas**
- Crear las 12 tablas manualmente: **2-3 horas**
- **TOTAL:** 5-7 horas para setup completo

---

_Generado: 9 de febrero de 2026_  
_Si tienes dudas, revisa los logs del servidor o contacta soporte_
