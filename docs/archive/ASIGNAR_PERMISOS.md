# GUIA RAPIDA: ASIGNAR PERMISOS AL APPLICATION USER

## PASO 1: Abrir Power Platform Admin Center

1. Abrir navegador
2. Ir a: `https://admin.powerplatform.microsoft.com`
3. Iniciar sesión con tu cuenta de administrador

---

## PASO 2: Seleccionar tu Entorno

1. En el menú izquierdo, click en **"Environments"**
2. Buscar y click en tu entorno (donde están las tablas cr321_*)
3. Click en **"Settings"** (arriba a la derecha)

---

## PASO 3: Ir a Application Users

1. En la ventana de Settings, buscar la sección:
   **"Users + permissions"**
2. Click en **"Application users"**
3. Esperar a que cargue la lista

---

## PASO 4: Encontrar tu Application User

Buscar por cualquiera de estos datos:
- **Application ID:** `d05fd904-f1fb-4fe3-89e9-1779d914c828`
- **Name:** `# WP0`
- **AAD Object ID:** `d7782081-fb6a-4a53-8d6a-d7d2104dd757`

---

## PASO 5: Asignar Rol de Seguridad

1. Click en el Application User (toda la fila)
2. En la parte superior, click en **"Manage security roles"**
3. En la ventana emergente, buscar: **"System Administrator"**
4. ✅ Activar el checkbox de **"System Administrator"**
5. Click en **"Save"** (abajo a la derecha)
6. Cerrar la ventana

---

## PASO 6: Verificar (Importante)

1. El Application User ahora debe mostrar:
   - **Security roles:** System Administrator
2. Cerrar todas las ventanas
3. **Esperar 5 minutos** (importante para propagación)

---

## PASO 7: Probar Permisos

Ejecutar en PowerShell:

```powershell
# Verificar permisos nuevamente
python verificar_permisos.py
```

**Resultado esperado:**
```
Grupos               ✅          ✅
Estados              ✅          ✅
Tickets              ✅          ✅
Usuario Grupo        ✅          ✅
Usuarios             ✅          ✅
Chats00              ✅          ✅
Contacto             ✅          ✅
Chatbots             ✅          ✅
```

---

## PASO 8: Ejecutar Inicialización

Si todos los permisos están OK (✅ en Crear):

```powershell
python init_dataverse.py
```

**Resultado esperado:**
```
✅ Grupo 'Solicitud Ticket' creado (ID: 1)
✅ Grupo 'Cotizaciones' creado (ID: 2)
✅ Grupo 'Información' creado (ID: 3)
✅ Grupo 'Atención de Agente' creado (ID: 4)
✅ Estado 'Nuevo' creado (ID: 1)
✅ Estado 'En Proceso' creado (ID: 2)
✅ Estado 'Pendiente Cliente' creado (ID: 3)
✅ Estado 'Resuelto' creado (ID: 4)
✅ Estado 'Cerrado' creado (ID: 5)
✅ Estado 'Cancelado' creado (ID: 6)
```

---

## TROUBLESHOOTING

### Problema: No encuentro el Application User
**Solución:** 
- Verifica que estás en el entorno correcto
- Busca por "WP0" o "d05fd904"
- Si no existe, créalo desde Azure Portal

### Problema: No veo "System Administrator" en la lista
**Solución:**
- Verifica que eres administrador del entorno
- Busca roles alternativos: "Basic User" + permisos custom
- Contacta al administrador de Power Platform

### Problema: Después de asignar rol, sigue sin permisos
**Solución:**
- Espera 10-15 minutos (propagación de permisos)
- Refresca el token: reinicia el script
- Verifica que el rol se asignó correctamente

### Problema: Error 403 persiste
**Solución:**
- Verifica que las tablas no estén bloqueadas
- Revisa que el Application User está activo
- Comprueba que CLIENT_ID y CLIENT_SECRET sean correctos

---

## ALTERNATIVA: Crear Datos Manualmente

Si los permisos son complejos de configurar, puedes crear los registros manualmente:

1. Ir a: `https://make.powerapps.com`
2. Tables → **cr321_grupos** → + New row
3. Crear 4 registros:
   - ID: 1, Nombre: "Solicitud Ticket", Tipo: 462410000
   - ID: 2, Nombre: "Cotizaciones", Tipo: 462410000
   - ID: 3, Nombre: "Información", Tipo: 462410000
   - ID: 4, Nombre: "Atención de Agente", Tipo: 462410000

4. Tables → **cr321_estados** → + New row
5. Crear 6 registros (IDs 1-6 con nombres: Nuevo, En Proceso, etc.)

**Tiempo:** 10 minutos manual vs 5 min + espera con permisos

---

## SIGUIENTE PASO DESPUÉS DE PERMISOS

Una vez que los grupos y estados estén creados:

```powershell
# Iniciar backend
.\iniciar_backend.ps1

# En otra terminal: Iniciar frontend
.\iniciar.ps1 LOCAL
```

¡El sistema estará 100% funcional!
