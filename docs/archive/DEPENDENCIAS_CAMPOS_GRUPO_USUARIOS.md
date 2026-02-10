# 🔍 Dependencias de Campos de Grupo en Usuarios

**Fecha:** 7 de febrero de 2026  
**Problema:** No se pueden eliminar los campos `cr321_1`, `cr321_3`, `cr321_4` de la tabla `cr321_usuarios`  
**Causa:** Tienen dependencias activas en el sistema  

---

## 📊 Campos Afectados

### Tabla: `cr321_usuarios` (cr321_usuarioses)

| Campo | Tipo | Descripción | Estado Actual |
|-------|------|-------------|---------------|
| `cr321_1` | Boolean (Sí/No) | Pertenece al Grupo 1 | ⚠️ En desuso |
| `cr321_3` | Boolean (Sí/No) | Pertenece al Grupo 3 | ⚠️ En desuso |
| `cr321_4` | Boolean (Sí/No) | Pertenece al Grupo 4 | ⚠️ En desuso |

**Nota:** Estos campos representaban un sistema **antiguo** de asignación de grupos mediante campos booleanos individuales.

---

## 🏗️ Historia del Sistema

### Sistema Antiguo (Campos Booleanos)
```
Usuario Juan:
  cr321_1 = true   → Pertenece al Grupo 1
  cr321_3 = true   → Pertenece al Grupo 3
  cr321_4 = false  → NO pertenece al Grupo 4
```

**Limitaciones:**
- ❌ Solo se podían manejar grupos predefinidos (1, 3, 4)
- ❌ No escalable (agregar nuevo grupo = agregar nueva columna)
- ❌ Sin información adicional del grupo (nombre, tipo, descripción)

### Sistema Nuevo (Tabla de Relaciones) ✅
```
Tabla: cr321_usuario_gruposes
- Relación Many-to-Many
- Escalable infinitamente
- Incluye toda la información del grupo
```

**Usuario Juan:**
```
Relación 1: usuario_id=Juan → grupo_id=Ventas
Relación 2: usuario_id=Juan → grupo_id=Soporte
Relación 3: usuario_id=Juan → grupo_id=Marketing
```

---

## ⚠️ Por Qué No Se Pueden Borrar

Dataverse bloquea la eliminación de columnas cuando existen:

### 1. **Vistas que Usan los Campos**
Las vistas (views) de Dataverse pueden estar mostrando estos campos:
- Vista "Usuarios Activos"
- Vista "Usuarios por Grupo"
- Vistas personalizadas del sistema

### 2. **Formularios (Forms)**
Los formularios de edición/creación de usuarios pueden incluir estos campos:
- Formulario principal de Usuario
- Formularios personalizados
- Formularios de Quick Create

### 3. **Flujos de Power Automate**
Pueden existir flujos que:
- Leen estos campos al crear/actualizar usuarios
- Toman decisiones basadas en estos valores
- Asignan tareas según grupo del usuario

### 4. **Reglas de Negocio (Business Rules)**
Reglas que validan o establecen valores automáticamente:
- "Si cr321_1 = true, entonces..."
- "Validar que al menos un grupo esté seleccionado"

### 5. **Campos Calculados o Rollup**
Otros campos que calculan valores basados en estos:
- Conteo de usuarios por grupo
- Validaciones agregadas

### 6. **Aplicaciones de Canvas o Model-Driven**
Apps de Power Apps que:
- Muestran estos campos en pantallas
- Los usan en fórmulas
- Filtran por estos valores

### 7. **Permisos y Seguridad**
Roles de seguridad con permisos específicos sobre estos campos

---

## 🔍 Cómo Identificar las Dependencias

### Método 1: Desde Power Apps (Interfaz)
1. Ir a **Power Apps** → **Tablas** → `cr321_usuarios`
2. Seleccionar **Columnas** → Buscar `cr321_1` (o `cr321_3`, `cr321_4`)
3. Click derecho → **Ver dependencias**
4. Aparecerá una lista completa de:
   - Vistas que lo usan
   - Formularios que lo incluyen
   - Flujos que lo referencian
   - Etc.

### Método 2: Desde Solution Explorer
1. **Power Apps** → **Soluciones**
2. Seleccionar la solución que contiene la tabla
3. **Advanced** → **Dependency checker**
4. Buscar dependencias de la columna específica

### Método 3: Consulta API
```http
GET {{DATAVERSE_URL}}/api/data/v9.2/EntityDefinitions(LogicalName='cr321_usuarios')/Attributes(LogicalName='cr321_1')/Dependencies
Authorization: Bearer {token}
```

---

## ✅ Pasos para Eliminar los Campos (Migración)

### FASE 1: Identificar Dependencias (1-2 horas)

1. **Revisar Vistas**
   ```
   Power Apps → Tablas → cr321_usuarios → Vistas
   Para cada vista:
     - Abrir editor
     - Ver si cr321_1, cr321_3, cr321_4 están en columnas
     - Si están: Remover de la vista
   ```

2. **Revisar Formularios**
   ```
   Power Apps → Tablas → cr321_usuarios → Formularios
   Para cada formulario:
     - Abrir editor de formularios
     - Buscar campos cr321_1, cr321_3, cr321_4
     - Removerlos del formulario
     - Guardar y publicar
   ```

3. **Revisar Flujos de Power Automate**
   ```
   Power Automate → Mis flujos
   Buscar flujos que usen "cr321_usuarios"
   Revisar cada paso:
     - ¿Lee cr321_1, cr321_3 o cr321_4?
     - ¿Los asigna?
     - Si sí: Modificar flujo para usar nueva tabla cr321_usuario_gruposes
   ```

4. **Revisar Reglas de Negocio**
   ```
   Power Apps → Tablas → cr321_usuarios → Reglas de negocio
   Desactivar o modificar reglas que usen estos campos
   ```

5. **Revisar Apps**
   ```
   Power Apps → Aplicaciones
   Para cada app que use cr321_usuarios:
     - Abrir en editor
     - Buscar referencias a cr321_1, cr321_3, cr321_4
     - Actualizar fórmulas para usar API de usuario_grupos
   ```

### FASE 2: Migrar Datos (30 minutos)

**Script de migración:**
```python
# Script: migrar_grupos_booleanos_a_relaciones.py

import requests
from backend.goot import get_token, DATAVERSE_URL

def migrar_grupos_usuarios():
    """
    Migra datos de campos booleanos (cr321_1, cr321_3, cr321_4)
    a la tabla de relaciones cr321_usuario_gruposes
    """
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    
    # 1. Obtener todos los usuarios con sus grupos booleanos
    url_usuarios = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuarioses?$select=cr321_usuariosid,cr321_nombre,cr321_1,cr321_3,cr321_4"
    
    response = requests.get(url_usuarios, headers=headers)
    usuarios = response.json().get("value", [])
    
    # 2. Mapeo: Los grupos 1, 3, 4 deben estar creados en cr321_grup
    # Asumiendo que existen grupos con cr321_idgrupo = 1, 3, 4
    url_grupos = f"{DATAVERSE_URL}/api/data/v9.2/cr321_grups?$filter=cr321_idgrupo in (1,3,4)"
    response = requests.get(url_grupos, headers=headers)
    grupos = response.json().get("value", [])
    
    grupo_map = {g["cr321_idgrupo"]: g["cr321_grupoid"] for g in grupos}
    print(f"Grupos mapeados: {grupo_map}")
    
    # 3. Crear relaciones
    url_crear = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuario_gruposes"
    headers["Content-Type"] = "application/json"
    
    for usuario in usuarios:
        usuario_id = usuario["cr321_usuariosid"]
        nombre = usuario.get("cr321_nombre", "Sin nombre")
        
        # Si cr321_1 = true, crear relación con grupo 1
        if usuario.get("cr321_1") == True and 1 in grupo_map:
            payload = {
                "cr321_usuarioid@odata.bind": f"/cr321_usuarioses({usuario_id})",
                "cr321_grupoid@odata.bind": f"/cr321_grups({grupo_map[1]})"
            }
            # Verificar que no exista
            check_url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuario_gruposes?$filter=_cr321_usuarioid_value eq {usuario_id} and _cr321_grupoid_value eq {grupo_map[1]}"
            if requests.get(check_url, headers=headers).json().get("value", []) == []:
                requests.post(url_crear, json=payload, headers=headers)
                print(f"✅ {nombre} → Grupo 1")
        
        # Repetir para cr321_3
        if usuario.get("cr321_3") == True and 3 in grupo_map:
            payload = {
                "cr321_usuarioid@odata.bind": f"/cr321_usuarioses({usuario_id})",
                "cr321_grupoid@odata.bind": f"/cr321_grups({grupo_map[3]})"
            }
            check_url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuario_gruposes?$filter=_cr321_usuarioid_value eq {usuario_id} and _cr321_grupoid_value eq {grupo_map[3]}"
            if requests.get(check_url, headers=headers).json().get("value", []) == []:
                requests.post(url_crear, json=payload, headers=headers)
                print(f"✅ {nombre} → Grupo 3")
        
        # Repetir para cr321_4
        if usuario.get("cr321_4") == True and 4 in grupo_map:
            payload = {
                "cr321_usuarioid@odata.bind": f"/cr321_usuarioses({usuario_id})",
                "cr321_grupoid@odata.bind": f"/cr321_grups({grupo_map[4]})"
            }
            check_url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuario_gruposes?$filter=_cr321_usuarioid_value eq {usuario_id} and _cr321_grupoid_value eq {grupo_map[4]}"
            if requests.get(check_url, headers=headers).json().get("value", []) == []:
                requests.post(url_crear, json=payload, headers=headers)
                print(f"✅ {nombre} → Grupo 4")
    
    print("\n✅ Migración completada")

if __name__ == "__main__":
    migrar_grupos_usuarios()
```

### FASE 3: Validar Migración (15 minutos)

1. **Verificar que todos los usuarios tienen sus grupos:**
   ```python
   # Para cada usuario, verificar que tiene las mismas relaciones
   GET /api/usuario-grupos/usuario/{usuario_id}
   ```

2. **Comparar conteos:**
   ```sql
   -- Usuarios con cr321_1 = true
   SELECT COUNT(*) FROM cr321_usuarios WHERE cr321_1 = true
   
   -- Debe ser igual a:
   SELECT COUNT(*) FROM cr321_usuario_gruposes WHERE cr321_grupoid = {grupo_1_guid}
   ```

### FASE 4: Eliminar Dependencias (1-2 horas)

1. ✅ Confirmar que TODAS las dependencias están removidas
2. ✅ Verificar que ningún flujo usa los campos
3. ✅ Verificar que ninguna app usa los campos
4. ✅ Publicar todas las personalizaciones

### FASE 5: Eliminar Campos (5 minutos)

```
Power Apps → Tablas → cr321_usuarios → Columnas
Para cada campo (cr321_1, cr321_3, cr321_4):
  1. Seleccionar el campo
  2. Click "Eliminar"
  3. Si aparece error: Revisar "Ver dependencias" nuevamente
  4. Si no hay error: Confirmar eliminación
  
Publicar personalizaciones
```

---

## 🎯 Solución Rápida (Sin Migración)

Si NO necesitas los datos históricos y solo quieres limpiar:

### Opción 1: Establecer como NULL
```python
# Establecer todos los valores en null/false
for usuario in usuarios:
    payload = {
        "cr321_1": False,
        "cr321_3": False,
        "cr321_4": False
    }
    PATCH /api/data/v9.2/cr321_usuarioses({usuario_id})
```

### Opción 2: Ocultar en Lugar de Eliminar
```
1. Mantener los campos en Dataverse
2. Removerlos de todas las vistas
3. Removerlos de todos los formularios
4. Marcarlos como "Ocultos" en definición de campo
5. Agregar descripción: "DEPRECATED - Usar cr321_usuario_gruposes"
```

---

## 📋 Checklist de Eliminación

Antes de intentar eliminar los campos, verificar:

- [ ] Todos los usuarios migrados a `cr321_usuario_gruposes`
- [ ] Ninguna vista usa `cr321_1`, `cr321_3`, `cr321_4`
- [ ] Ningún formulario incluye estos campos
- [ ] Ningún flujo de Power Automate los referencia
- [ ] Ninguna regla de negocio los usa
- [ ] Ninguna app de Canvas/Model-Driven los usa
- [ ] Sin campos calculados que dependan de ellos
- [ ] Sin roles de seguridad específicos sobre ellos
- [ ] Backup de datos creado (por si acaso)
- [ ] Script de migración probado en entorno DEV

---

## 🔗 Referencias

- **Tabla nueva:** `cr321_usuario_gruposes` - [VERIFICACION_REQ010_USUARIO_GRUPOS.md](VERIFICACION_REQ010_USUARIO_GRUPOS.md)
- **API de relaciones:** `backend/api/usuario_grupos.py`
- **Documentación Dataverse:** [Learn.microsoft.com - Delete columns](https://learn.microsoft.com/en-us/power-apps/maker/data-platform/delete-fields)

---

## 📞 Soporte

Si necesitas ayuda para identificar dependencias específicas:

1. Compartir screenshot del error al intentar borrar
2. Ejecutar "Ver dependencias" y compartir resultado
3. Revisar logs de Power Automate en busca de flujos activos

---

**Última actualización:** 7 de febrero de 2026  
**Estado:** Documento informativo - Acción pendiente del usuario
