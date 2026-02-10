# 🛡️ EVITAR COLUMNAS AUTOMÁTICAS EN VISTAS - DATAVERSE

## ❌ EL PROBLEMA

Cuando creas una columna en Dataverse, **automáticamente se agrega a:**
- 🔴 Vista "Active [Nombre Tabla]"  
- 🔴 Formulario principal
- 🔴 Búsqueda global

**Esto NO se puede desactivar a nivel de sistema**, pero puedes minimizarlo.

---

## ✅ MEJORES PRÁCTICAS (Crear columnas correctamente)

### **1. Configuración al crear columna**

```
Power Apps → Tablas → [Tu Tabla] → "+ Nueva columna"

┌─────────────────────────────────────────┐
│ Nombre para mostrar: [Tu Nombre]       │
│ Nombre: cr321_[nombre]                  │
│ Tipo de datos: [Seleccionar]           │
│                                         │
│ ⚠️ EXPANDIR "Opciones avanzadas" ⚠️     │
│                                         │
│ [ ] Aparece en búsquedas globales      │ ← DESACTIVAR ✓
│ [ ] Se puede buscar                    │ ← DESACTIVAR (si no es clave) ✓
│ [x] Auditoría                          │ ← Según necesites
│                                         │
│ Descripción: [Propósito del campo]     │ ← Documentar ✓
│                                         │
│         [Guardar]                       │
└─────────────────────────────────────────┘
```

### **2. Inmediatamente después de crear**

Sigue estos pasos **EN EL MOMENTO** de crear la columna:

```
A. Ir a pestaña "Vistas"
B. Abrir vista "Active [Tabla]"
C. Buscar tu columna recién creada
D. Click [X] para quitarla
E. Guardar y Publicar

⏱️ Tiempo: 30 segundos
💰 Ahorro: Evita confusión futura
```

---

## 🔧 SOLUCIÓN RÁPIDA (Ya tengo columnas en vistas)

### **Script automático** (USA EL QUE CREAMOS):

```powershell
.\limpiar_columnas_vistas.ps1
```

### **Manual rápido** (5 min por tabla):

1. **Listar columnas problemáticas:**
   ```powershell
   # En tu proyecto, identifica columnas obsoletas
   cr321_1, cr321_3, cr321_4  # Campos viejos
   cr321_usuariogrupo1         # Campo migrado
   ```

2. **Quitar de vistas:**
   - `make.powerapps.com` → Tabla → **Vistas**
   - Editar cada vista
   - Quitar columnas no deseadas
   - Guardar + Publicar

3. **Quitar de formularios:**
   - Misma tabla → **Formularios**
   - Editar formulario principal
   - Quitar campos no deseados
   - Guardar + Publicar

---

## 📊 CHECKLIST POR CADA COLUMNA NUEVA

Usa esta lista cada vez que crees un campo:

```
[ ] 1. Configurar "Opciones avanzadas" (búsquedas OFF)
[ ] 2. Agregar descripción clara del propósito
[ ] 3. Quitar de vista "Active..." inmediatamente
[ ] 4. Agregar SOLO a las vistas necesarias manualmente
[ ] 5. Documentar en tu código/README si es importante
```

---

## 💡 TIPS ADICIONALES

### **A. Campos de sistema vs. business:**

```python
# Campos que NO necesitan estar en vistas:
- IDs técnicos (cr321_...id)
- Fechas de sistema (createdon, modifiedon)
- Campos de lookup internos (_cr321_..._value)
- Campos de migración/deprecated
- Campos calculados internos

# Campos que SÍ van en vistas:
- Nombre/título
- Estado/status
- Fechas relevantes para negocio
- Campos principales de búsqueda
```

### **B. Organizar vistas por rol:**

En lugar de una vista con todo, crea vistas específicas:

```
✓ Vista "Admin - Todas las columnas"
✓ Vista "Usuario - Solo lectura"
✓ Vista "Contabilidad - Filtrada"
✓ Vista "Soporte - Activas"
```

### **C. Marcas de deprecated:**

Si migraste campos pero no puedes eliminarlos:

```
Descripción del campo:
"⚠️ DEPRECATED - Migrado a _cr321_grupo_value. No usar."

Nombre de columna:
"❌ [OLD] Usuario Grupo"  ← Prefijo visual
```

---

## 🚫 CAMPOS QUE DEBES QUITAR DE VISTAS (Tu proyecto)

Basado en tu código actual:

```
cr321_usuarios:
  ✗ cr321_1          → Migrado a relaciones
  ✗ cr321_3          → Migrado a relaciones
  ✗ cr321_4          → Migrado a relaciones

cr321_usuariogrupos:
  ✗ cr321_usuariogrupo1  → Migrado a _cr321_grupo_value
```

---

## 📞 CUANDO NO PUEDES ELIMINAR

Si Dataverse no te deja eliminar la columna:

```
ERROR: "Esta columna tiene dependencias"

ACCIÓN:
1. Ver dependencias en Power Apps
2. Remover de vistas/formularios/flujos
3. Si persiste error:
   → OCULTAR en lugar de eliminar
   → Marcar como DEPRECATED
   → Documentar en código

✅ RESULTADO: Campo no visible, pero datos preservados
```

---

## 🎯 RESULTADO FINAL

Siguiendo estas prácticas:
- ✅ Vistas limpias con solo columnas relevantes
- ✅ UI más rápida y menos confusa
- ✅ Datos organizados
- ✅ Búsquedas más precisas
- ✅ Mantenimiento más fácil

---

**Ejecuta ahora:**
```powershell
cd c:/VS/BIN
.\limpiar_columnas_vistas.ps1
```
