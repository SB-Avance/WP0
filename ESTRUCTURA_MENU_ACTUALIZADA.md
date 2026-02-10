# ESTRUCTURA DEL MENÚ ACTUALIZADA
**Fecha:** Febrero 9, 2026

## CAMBIOS IMPLEMENTADOS

### ✅ Eliminado
- ❌ Dropdown de grupos en el sidebar
- ❌ Vista "Dashboard" (no se usa)
- ❌ Vista "Settings" (reemplazada por "Salir")

### ✅ Agregado
- ✅ Botón "Salir" al final del menú
- ✅ Menú dinámico desde tabla `cr321_chatbots`
- ✅ Filtrado automático de chats por grupo del usuario

---

## ESTRUCTURA DEL MENÚ

### Elementos Dinámicos (desde chatbots activos)
```
Posición: 0 hasta N-1
Origen: Campos elemento1-5 de chatbots con cr321_active = true
Visible: Todos los usuarios
```

**Ejemplo actual:**
- "Solicitar atención de agente"
- "Página Web"

### Chats
```
Posición: N
Vista: ChatsView
Visible: Todos los usuarios
Filtrado: Automático por grupos del usuario
```

### Opciones Administrativas (solo admin)
```
Posiciones: N+1 hasta N+5
Visible: Solo rol = 'administrador'
```

1. **Usuarios** - CRUD completo
   - Vista: UsersView
   - Tabla: cr321_usuarios
   - Operaciones: Crear, Leer, Actualizar, Eliminar

2. **Chatbots** - CRUD completo
   - Vista: ChatbotsView
   - Tabla: cr321_chatbots
   - Operaciones: Crear, Leer, Actualizar, Eliminar
   - Campos: nombre, tipo, activo, config, elemento1-5

3. **Templates** - CRUD completo
   - Vista: TemplatesView
   - Tabla: cr321_template
   - Operaciones: Crear, Leer, Actualizar, Eliminar

4. **Cuentas WA** - CRUD completo
   - Vista: WhatsAppAccountsView
   - Tabla: cr321_cuentadewhatsapp
   - Operaciones: Crear, Leer, Actualizar, Eliminar

### Salir
```
Posición: Última
Acción: on_logout() - cierra sesión
Visible: Todos los usuarios
```

---

## CÓMO FUNCIONA EL MENÚ DINÁMICO

### 1. Al iniciar sesión
```python
load_menu_elements()
  ↓
GET /api/chatbots (filtrar activos)
  ↓
Extraer elemento1-5 de cada chatbot activo
  ↓
Construir lista menu_elements
```

### 2. En el sidebar
```python
menu_elements = ["Solicitar atención", "Página Web"]
  ↓
Por cada elemento, crear NavigationRailDestination
  ↓
Agregar "Chats"
  ↓
Si admin: Agregar Usuarios, Chatbots, Templates, Cuentas WA
  ↓
Agregar "Salir"
```

### 3. Navegación
```python
on_nav_change(idx)
  ↓
Si idx < len(menu_elements): Elemento dinámico → Dashboard
  ↓
Si idx == len(menu_elements): Chats
  ↓
Si idx > len(menu_elements): Opciones admin o Salir
```

---

## PERMISOS POR ROL

### Usuario Normal
```
Menú visible:
  • [Elementos dinámicos]
  • Chats
  • Salir
```

### Administrador
```
Menú visible:
  • [Elementos dinámicos]
  • Chats
  • Usuarios
  • Chatbots
  • Templates
  • Cuentas WA
  • Salir
```

---

## FILTRADO DE CHATS POR GRUPO

### Lógica implementada
```python
# En main.py, vista "chats"
if user_rol != 'administrador':
    # Obtener grupos del usuario
    user_groups = api.get_user_groups(user_id)
    user_group_names = [g['nombre'] for g in user_groups]
    
    # Filtrar conversaciones
    conversations = [c for c in conversations 
                    if c['group'] in user_group_names]
else:
    # Admin ve todos los chats
    conversations = api.get_conversations()
```

---

## TABLAS DATAVERSE INVOLUCRADAS

### cr321_chatbots
```
Campos usados:
  • cr321_chatbotid (PK)
  • cr321_name (nombre del chatbot)
  • cr321_active (filtro para menú)
  • cr321_elemento1 (opción menú 1)
  • cr321_elemento2 (opción menú 2)
  • cr321_elemento3 (opción menú 3)
  • cr321_elemento4 (opción menú 4)
  • cr321_elemento5 (opción menú 5)
```

### cr321_adatawp0 (Chats)
```
Filtrado por: cr321_grupo (lookup a cr321_grup)
```

### cr321_usuarios
```
CRUD completo - solo admin
```

### cr321_template
```
CRUD completo - solo admin
```

### cr321_cuentadewhatsapp
```
CRUD completo - solo admin
```

---

## ARCHIVOS MODIFICADOS

### mobile/components/sidebar.py
- Eliminado dropdown de grupos
- Simplificada firma de función: `SidebarView(on_nav, on_logout, user_name, user_rol, menu_elements)`
- Agregado botón "Salir" con icono `ft.icons.LOGOUT`
- Nueva estructura de construcción del menú

### mobile/main.py
- Actualizado `on_nav_change()` con nueva lógica de índices
- Eliminados parámetros de grupos en `SidebarView()`
- Simplificado render de vistas
- Botón Salir llama a `on_logout()` directamente

---

## EJEMPLO DE USO

### Chatbot en Dataverse
```json
{
  "cr321_name": "Soporte",
  "cr321_active": true,
  "cr321_elemento1": "Solicitud Ticket",
  "cr321_elemento2": "Estado Ticket",
  "cr321_elemento3": "Contactar Agente",
  "cr321_elemento4": null,
  "cr321_elemento5": null
}
```

### Menú generado (Usuario normal)
```
1. Solicitud Ticket
2. Estado Ticket
3. Contactar Agente
4. Chats
5. Salir
```

### Menú generado (Administrador)
```
1. Solicitud Ticket
2. Estado Ticket
3. Contactar Agente
4. Chats
5. Usuarios
6. Chatbots
7. Templates
8. Cuentas WA
9. Salir
```

---

## PRÓXIMOS PASOS SUGERIDOS

1. **Implementar vistas para elementos dinámicos**
   - Actualmente van a Dashboard
   - Crear vistas específicas según el elemento
   
2. **Agregar asignación de chatbots a grupos**
   - Tabla `cr321_chatbotgrupo` (N:N)
   - Campo JSON en `cr321_config` con grupos asignados
   
3. **Mejorar filtrado de menú por grupo**
   - Solo mostrar elementos de chatbots asignados al grupo del usuario
   - Combinar elementos de múltiples chatbots

---

## COMANDOS ÚTILES

### Iniciar sistema
```powershell
cd c:/VS/BIN
.\iniciar.ps1
```

### Ver chatbots activos
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/chatbots" -Method GET | 
    Select-Object -ExpandProperty chatbots | 
    Where-Object { $_.activo } | 
    Format-Table nombre, elemento1, elemento2, elemento3
```

### Cambiar elementos del menú
1. Ir a Power Apps: https://make.powerapps.com
2. Abrir tabla "chatbot" (cr321_chatbots)
3. Editar chatbot activo
4. Modificar campos elemento1-5
5. Guardar
6. Hacer logout/login en el frontend
