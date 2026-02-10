# 📝 Cambio de Nombre de Campo: cr321_id → cr321_idusuario

**Fecha:** 7 de febrero de 2026  
**Tipo:** Refactorización de nomenclatura  
**Prioridad:** Media  

---

## 🎯 Objetivo del Cambio

Renombrar el campo `cr321_id` en la tabla `cr321_usuarios` a `cr321_idusuario` para:
- ✅ Mantener consistencia con otros campos consecutivos (`cr321_idgrupo`, `cr321_idestado`, `cr321_idticket`)
- ✅ Mejorar la claridad del código
- ✅ Evitar confusiones con el campo GUID `cr321_usuariosid`

---

## 📊 Cambios Realizados en Código

### 1. Backend - Core (backend/goot.py)
**Función:** `create_user()`
- ✅ Línea 103: Query SELECT actualizada
- ✅ Línea 109: Lectura del campo actualizada  
- ✅ Línea 115: Mensaje de warning actualizado
- ✅ Línea 123: Payload de creación actualizado

```python
# ANTES:
url_get = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuarioses?$select=cr321_id"
val = int(user.get("cr321_id", 0))
user_data = {"cr321_id": nuevo_id}

# DESPUÉS:
url_get = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuarioses?$select=cr321_idusuario"
val = int(user.get("cr321_idusuario", 0))
user_data = {"cr321_idusuario": nuevo_id}
```

### 2. Backend - API Usuario-Grupos (backend/api/usuario_grupos.py)
**Función:** `get_usuarios_by_grupo()`
- ✅ Línea 104: $expand actualizado con nuevo campo
- ✅ Línea 118: Mapeo de respuesta JSON actualizado

```python
# ANTES:
url += "&$expand=cr321_usuarioid($select=cr321_usuariosid,cr321_id,cr321_nombre...)"
"idusuario": usuario_data.get("cr321_id")

# DESPUÉS:
url += "&$expand=cr321_usuarioid($select=cr321_usuariosid,cr321_idusuario,cr321_nombre...)"
"idusuario": usuario_data.get("cr321_idusuario")
```

---

## 📄 Cambios Realizados en Documentación

### 1. VERIFICACION_REQ010_USUARIO_GRUPOS.md
✅ Actualizada definición de tabla `cr321_usuarios`

### 2. GUIA_SISTEMA_CHATBOT.md
✅ Actualizada sección de arquitectura de tablas

### 3. MAPA_APLICACION.md
✅ Actualizado diagrama de tabla usuarios

---

## ⚠️ Cambios Pendientes en Dataverse

**IMPORTANTE:** Este cambio también requiere actualización en Dataverse:

### Pasos para aplicar en Dataverse:

1. **Acceder a Power Apps** (https://make.powerapps.com)
2. **Seleccionar entorno** (dev, prod, etc.)
3. **Navegar a:** Tablas → cr321_usuarios → Columnas
4. **Buscar columna:** `cr321_id`
5. **Editar propiedades:**
   - Cambiar **Nombre para mostrar** a: "ID Usuario"
   - Cambiar **Nombre** a: `cr321_idusuario`
6. **Guardar cambios**
7. **Publicar personalizaciones**

### Verificación Post-Cambio:
```bash
# Verificar que el campo fue renombrado correctamente
GET {{DATAVERSE_URL}}/api/data/v9.2/cr321_usuarioses?$select=cr321_idusuario&$top=1

# Debe retornar el valor numérico consecutivo
```

---

## 📋 Checklist de Validación

### Cambios en Código: ✅ COMPLETADOS
- [x] backend/goot.py actualizado
- [x] backend/api/usuario_grupos.py actualizado
- [x] Documentación técnica actualizada

### Cambios en Dataverse: ⏳ PENDIENTE
- [ ] Campo renombrado en Power Apps
- [ ] Personalizaciones publicadas
- [ ] Verificación con query OData
- [ ] Pruebas de creación de usuario
- [ ] Pruebas de consulta de grupos por usuario

---

## 🔍 Impacto del Cambio

### Archivos de Código Afectados: 2
- `backend/goot.py` (4 cambios)
- `backend/api/usuario_grupos.py` (2 cambios)

### Archivos de Documentación Actualizados: 3
- `docs/VERIFICACION_REQ010_USUARIO_GRUPOS.md`
- `docs/GUIA_SISTEMA_CHATBOT.md`
- `docs/MAPA_APLICACION.md`

### APIs Afectadas:
- ✅ `POST /api/users` (crear usuario)
- ✅ `GET /api/usuario-grupos/grupo/<grupo_id>` (listar usuarios de grupo)

### Tablas de Dataverse Afectadas:
- `cr321_usuarios` (tabla principal)
- `cr321_usuario_gruposes` (relaciones - indirectamente)

---

## 🧪 Pruebas Recomendadas

Después de aplicar cambios en Dataverse:

### 1. Crear Usuario
```python
POST /api/users
{
  "nombre": "Usuario Test",
  "correo": "test@example.com",
  "clave": "password123",
  "rol": "Agente"
}
# Verificar que cr321_idusuario se asigna correctamente
```

### 2. Consultar Usuarios de Grupo
```python
GET /api/usuario-grupos/grupo/{grupo_id}
# Verificar que el campo "idusuario" retorna el valor numérico
```

### 3. Query Directa Dataverse
```
GET /api/data/v9.2/cr321_usuarioses?$select=cr321_usuariosid,cr321_idusuario,cr321_nombre
# Verificar que cr321_idusuario existe y contiene valores
```

---

## 📚 Referencias

- **Convención de nombres:** Campos consecutivos usan formato `cr321_id{tabla}`
  - `cr321_idgrupo` (tabla grup)
  - `cr321_idestado` (tabla estado)
  - `cr321_idticket` (tabla ticket)
  - `cr321_idusuario` (tabla usuarios) ← NUEVO

- **Diferenciación de IDs:**
  - `cr321_usuariosid` = GUID (Primary Key único de Dataverse)
  - `cr321_idusuario` = Integer (ID consecutivo legible por humanos)

---

## ✅ Estado

- **Código:** ✅ COMPLETADO (2026-02-07)
- **Documentación:** ✅ COMPLETADO (2026-02-07)
- **Dataverse:** ⏳ PENDIENTE (requiere acción manual)

---

## 🔄 Próximos Pasos

1. ⏳ Aplicar cambio en Dataverse (Power Apps)
2. ⏳ Publicar personalizaciones
3. ⏳ Ejecutar pruebas de validación
4. ⏳ Marcar como completado en BACKLOG

---

**Nota:** Este cambio NO es breaking si se hace correctamente en Dataverse antes de ejecutar el backend actualizado. El código antiguo dejará de funcionar si Dataverse tiene el campo renombrado pero el código no está actualizado (ya está actualizado).
