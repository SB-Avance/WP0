# 🔍 Guía de Uso: verificar_permisos.py

## 📋 Descripción

Script de diagnóstico para verificar que el **Application User** tiene los permisos necesarios para acceder a todas las tablas personalizadas del sistema en Microsoft Dataverse.

---

## 🎯 Propósito

- ✅ Verificar permisos de **lectura** (GET) en cada tabla
- ✅ Verificar permisos de **creación** (POST) en cada tabla  
- ✅ Validar conectividad y autenticación con Dataverse
- ✅ Diagnosticar problemas antes de inicializar datos

---

## 🔧 Requisitos Previos

1. **Application User creado** en Power Platform Admin Center
2. **Rol "System Administrator"** asignado al Application User
3. **Variables de entorno** configuradas en `backend/.env`:
   ```env
   CLIENT_ID=tu-application-id
   CLIENT_SECRET=tu-client-secret
   TENANT_ID=tu-tenant-id
   DATAVERSE_URL=https://tu-entorno.crm.dynamics.com
   ```
4. **Tablas creadas** en Dataverse (las 8 tablas cr321_*)

---

## 🚀 Uso

### Ejecución básica:
```powershell
python verificar_permisos.py
```

### Desde cualquier ubicación:
```powershell
cd C:\VS\BIN
python verificar_permisos.py
```

---

## 📊 Interpretación de Resultados

### ✅ Resultado Exitoso
```
======================================================================
🔍 VERIFICACIÓN DE PERMISOS EN DATAVERSE
======================================================================
✅ Token obtenido correctamente

Tabla                     Leer       Crear
----------------------------------------------------------------------
Grupos                    ✅          ✅
Estados                   ✅          ✅
Tickets                   ✅          ✅
Usuario Grupo             ✅          ✅
Usuarios                  ✅          ✅
Chats00                   ✅          ✅
Contacto                  ✅          ✅
Chatbots                  ✅          ✅

======================================================================
✅ TODOS LOS PERMISOS ESTÁN CORRECTOS
```

**Significado:** El sistema está listo para usar. Puedes ejecutar `python init_dataverse.py`

---

### ❌ Resultado con Errores

#### Error: No se pudo obtener token
```
❌ No se pudo obtener token
```

**Causas posibles:**
- CLIENT_ID incorrecto
- CLIENT_SECRET incorrecto o expirado
- TENANT_ID incorrecto
- DATAVERSE_URL incorrecto

**Solución:** Revisa las credenciales en `backend/.env`

---

#### Error: HTTP 404 - Tabla no encontrada
```
❌ Estados (cr321_estadoses)
   └─ HTTP 404: Resource not found for the segment 'cr321_estadoses'
```

**Causas posibles:**
- La tabla no existe en Dataverse
- El nombre de la tabla es incorrecto
- Usaste LogicalName en lugar de EntitySetName

**Solución:** 
1. Verifica que las tablas existen en Power Apps
2. Confirma que usas EntitySetName (plural)

---

#### Error: HTTP 403 - Sin permisos
```
❌ Tickets (cr321_tickets)
   └─ HTTP 403: Forbidden
```

**Causas posibles:**
- El Application User no tiene rol "System Administrator"
- Los permisos no se han propagado (espera 5-10 minutos)

**Solución:** 
1. Asigna el rol "System Administrator" (ver `ASIGNAR_PERMISOS.md`)
2. Espera 5-10 minutos después de asignar el rol
3. Ejecuta el script nuevamente

---

## 📚 Tablas Verificadas

| Tabla | EntitySetName | Descripción |
|-------|---------------|-------------|
| Grupos | cr321_gruposes | Opciones del menú principal del chatbot |
| Estados | cr321_estadoses | Estados del ciclo de vida de tickets |
| Tickets | cr321_tickets | Conversaciones/solicitudes de usuarios |
| Usuario Grupo | cr321_usuariogrupos | Relación usuarios ↔ grupos |
| Usuarios | cr321_usuarioses | Usuarios del sistema (clientes WhatsApp) |
| Chats00 | cr321_adatawp0s | Historial completo de mensajes |
| Contacto | cr321_contactos | Información de contacto |
| Chatbots | cr321_chatbotses | Configuración de bots |

---

## ⚠️ Nota Importante sobre Nombres

**Dataverse usa DOS nombres diferentes para cada tabla:**

1. **LogicalName** (singular) → Lo que ves en Power Apps
   - Ejemplo: `cr321_ticket`, `cr321_contacto`

2. **EntitySetName** (plural) → Lo que usas en código/API
   - Ejemplo: `cr321_tickets`, `cr321_contactos`

Este script usa **EntitySetName** porque interactúa con la API Web de Dataverse.

---

## 🔄 Relación con Otros Scripts

### Flujo de trabajo típico:

1. **Crear tablas** (si no existen)
   ```powershell
   python crear_tablas_auto.py
   ```

2. **Asignar permisos** (manual en Power Platform)
   - Ver: `ASIGNAR_PERMISOS.md`

3. **Verificar permisos** ← **ESTE SCRIPT**
   ```powershell
   python verificar_permisos.py
   ```

4. **Inicializar datos** (si permisos OK)
   ```powershell
   python init_dataverse.py
   ```

5. **Iniciar backend**
   ```powershell
   python backend/back.py
   ```

---

## 🐛 Troubleshooting

### El script tarda mucho
- **Causa:** Timeout de red o Dataverse lento
- **Solución:** Aumenta el timeout en la línea 122 del script

### Error de importación (ModuleNotFoundError)
- **Causa:** Dependencias no instaladas
- **Solución:** 
  ```powershell
  pip install -r requirements.txt
  ```

### Token válido pero permisos fallan
- **Causa:** Los permisos recién asignados no se han propagado
- **Solución:** Espera 5-10 minutos y ejecuta nuevamente

---

## 📝 Notas de Desarrollo

- **Versión:** 2.0
- **Última actualización:** 2026-02-06
- **Compatibilidad:** Python 3.8+
- **Dependencias:** msal, requests, python-dotenv
- **Seguridad:** No almacena tokens en disco

---

## 📞 Soporte

Si después de seguir esta guía sigues teniendo problemas:

1. Verifica `ASIGNAR_PERMISOS.md` para configuración de permisos
2. Revisa `ESTADO_REAL_PROYECTO.md` para contexto del sistema
3. Consulta los logs de error detallados en la salida del script

---

✅ **Script documentado y listo para producción**
