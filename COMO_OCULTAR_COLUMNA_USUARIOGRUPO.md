# OCULTAR COLUMNA "Usuario Grupo" (cr321_usuariogrupo1)

## ❌ Por qué NO se puede eliminar

Dataverse bloquea la eliminación de columnas cuando:
1. ✓ Tienen datos existentes (tu caso)
2. ✓ Están en vistas/formularios
3. ✓ Sistema las marca como no eliminables

## ✅ SOLUCIÓN: Ocultarla

### Paso 1: Quitar de vistas

1. Ve a [make.powerapps.com](https://make.powerapps.com)
2. **Tablas** → `Usuario Grupo` (`cr321_usuariogrupos`)
3. Pestaña **"Vistas"** → Abre cada vista
4. Busca la columna **"Usuario Grupo"**
5. Clic en **X** para quitarla de la vista
6. **Guardar y publicar**

### Paso 2: Quitar de formularios

1. En la misma tabla, pestaña **"Formularios"**
2. Abre el formulario principal
3. Busca el campo **"Usuario Grupo"**
4. Selecciónalo → **Eliminar**
5. **Guardar y publicar**

### Paso 3: Marcar como oculta (opcional)

1. **Tablas** → `Usuario Grupo` → **Columnas**
2. Busca **"Usuario Grupo"** (`cr321_usuariogrupo1`)
3. Clic en **⋮** → **Editar**
4. En **"Configuración avanzada"**:
   - Desactiva **"Aparece en búsquedas globales"**
   - Marca como **"Oculta"** si está disponible
5. **Guardar**

### Paso 4: Agregar descripción

En la misma ventana de edición:
- **Descripción**: `⚠️ DEPRECATED - Ya no se usa. Se migró a lookup _cr321_grupo_value`

## 📝 Resultado Final

La columna:
- ✅ No aparece en vistas
- ✅ No aparece en formularios  
- ✅ No se puede buscar
- ✅ Está documentada como DEPRECATED
- ✅ Los datos siguen ahí (no se pierden)
- ✅ No interfiere con la aplicación

## 🔍 Estado Actual

**Backend** ya NO usa este campo:
```python
# backend/api/usuario_grupos.py (línea 70)
url += "&$select=cr321_usuariogrupoid,_cr321_grupo_value"
# ← Ya no incluye cr321_usuariogrupo1
```

**Dataverse** ahora usa el lookup correcto:
```
_cr321_grupo_value → cr321_grups
```

## ⚠️ NOTA

**NUNCA** elimines columnas con datos en producción.
Ocultarlas es la práctica recomendada por Microsoft.
