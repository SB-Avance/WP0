# 🚀 Guía Rápida: Sistema Usuario-Grupos

## 📌 Resumen Rápido
Los usuarios **SÍ pueden** pertenecer a **múltiples grupos**. El sistema está completamente funcional.

---

## 🔌 API Endpoints

### 1. Ver grupos de un usuario
```bash
GET /api/usuario-grupos/usuario/{usuario_id}
```
**Respuesta:** Lista de todos los grupos del usuario

### 2. Ver usuarios de un grupo
```bash
GET /api/usuario-grupos/grupo/{grupo_id}
```
**Respuesta:** Lista de todos los usuarios en el grupo

### 3. Asignar usuario a grupo
```bash
POST /api/usuario-grupos
Content-Type: application/json

{
  "usuario_id": "guid-del-usuario",
  "grupo_id": "guid-del-grupo"
}
```
**Resultado:** Usuario agregado al grupo (permite múltiples grupos)

### 4. Remover usuario de grupo
```bash
DELETE /api/usuario-grupos/{relacion_id}
```
**Resultado:** Elimina la relación específica

### 5. Listar todas las relaciones
```bash
GET /api/usuario-grupos
GET /api/usuario-grupos?usuario_id={id}
GET /api/usuario-grupos?grupo_id={id}
```
**Respuesta:** Lista de relaciones con filtros opcionales

---

## 📊 Tipos de Grupos

| Tipo | Código Dataverse | Descripción |
|------|------------------|-------------|
| **A** | 462410000 | Opciones de menú principal |
| **B** | 462410001 | Grupos secundarios |
| **C** | 462410002 | Grupos especiales |

---

## 💡 Ejemplos de Uso

### Ejemplo 1: Usuario en múltiples grupos
```javascript
// Usuario "Juan" puede estar en:
- Grupo Ventas (Tipo A)
- Grupo Soporte (Tipo B)
- Grupo Admin (Tipo C)

// Para agregar a cada grupo:
POST /api/usuario-grupos { usuario_id: "juan-id", grupo_id: "ventas-id" }
POST /api/usuario-grupos { usuario_id: "juan-id", grupo_id: "soporte-id" }
POST /api/usuario-grupos { usuario_id: "juan-id", grupo_id: "admin-id" }

// Resultado: Juan tiene 3 grupos ✅
```

### Ejemplo 2: Ver grupos de usuario
```javascript
// Consultar grupos de Juan
GET /api/usuario-grupos/usuario/juan-id

// Respuesta:
{
  "grupos": [
    { "id": "...", "nombre": "Ventas", "tipo": "A" },
    { "id": "...", "nombre": "Soporte", "tipo": "B" },
    { "id": "...", "nombre": "Admin", "tipo": "C" }
  ]
}
```

### Ejemplo 3: Ver usuarios de un grupo
```javascript
// Consultar usuarios del grupo Ventas
GET /api/usuario-grupos/grupo/ventas-id

// Respuesta:
{
  "usuarios": [
    { "id": "...", "nombre": "Juan Pérez", "correo": "juan@..." },
    { "id": "...", "nombre": "María García", "correo": "maria@..." },
    { "id": "...", "nombre": "Carlos López", "correo": "carlos@..." }
  ]
}
```

---

## 🔒 Validaciones Automáticas

- ✅ **No permite duplicados:** No se puede agregar la misma combinación usuario-grupo dos veces
- ✅ **Múltiples grupos:** Un usuario puede estar en tantos grupos como sea necesario
- ✅ **Múltiples usuarios:** Un grupo puede tener tantos usuarios como sea necesario
- ✅ **Campos requeridos:** usuario_id y grupo_id son obligatorios

---

## 📁 Estructura de Base de Datos

```
cr321_usuarios (tabla de usuarios)
    └─ cr321_usuariosid (PK)

cr321_grup (tabla de grupos)
    └─ cr321_grupoid (PK)
    └─ cr321_tipo (OptionSet: A, B, C)

cr321_usuario_gruposes (tabla de relaciones)
    ├─ cr321_usuario_grupoid (PK)
    ├─ cr321_usuarioid (FK → cr321_usuarios)
    └─ cr321_grupoid (FK → cr321_grup)
```

**Relación:** Many-to-Many (Muchos a Muchos)

---

## 🛠️ Código de Referencia

**Archivo:** `backend/api/usuario_grupos.py`

**Funciones principales:**
- `get_usuario_grupos()` - Lista general
- `get_grupos_by_usuario(usuario_id)` - Grupos de usuario
- `get_usuarios_by_grupo(grupo_id)` - Usuarios de grupo
- `create_usuario_grupo()` - Crear relación
- `delete_usuario_grupo(relacion_id)` - Eliminar relación

---

## ✅ Estado: FUNCIONAL

Verificado el 7 de febrero de 2026  
✅ Todos los requisitos cumplidos  
✅ API completa y operativa  
✅ Validaciones implementadas  

**Ver documentación completa:** [VERIFICACION_REQ010_USUARIO_GRUPOS.md](VERIFICACION_REQ010_USUARIO_GRUPOS.md)
