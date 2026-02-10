# Guía Rápida: Crear Campo Lookup en Power Apps

**Tabla:** chats00 (cr321_adatawp0s)  
**Campo nuevo:** cr321_categoria_chatbot  **Tipo:** Lookup → cr321_grup

---

## ⚡ Pasos Rápidos

### 1️⃣ Abrir Power Apps
```
https://make.powerapps.com
```

### 2️⃣ Navegar a la Tabla
```
Tablas → Buscar "cr321_adatawp0" o "chats00"
→ Click en la tabla
→ Columnas (panel lateral)
```

### 3️⃣ Crear Nueva Columna

Click en **"+ Nueva columna"** (arriba a la derecha)

**Configuración:**
```
┌─────────────────────────────────────────┐
│ Nombre para mostrar: Categoría Chatbot │
│ Nombre: cr321_categoria_chatbot         │
│ Tipo de datos: Búsqueda (Lookup) ▼     │
│ Tabla relacionada: cr321_grup           │
│                                         │
│ [ ] Requerido (dejar sin marcar)       │
│ [ ] Buscable (marcar opcional)         │
└─────────────────────────────────────────┘
```

### 4️⃣ Guardar
```
Click en "Guardar" (esquina inferior derecha)
```

---

## ✅ Verificación

Para verificar que el campo se creó correctamente:

1. **En Power Apps:**
   - Ve a la lista de columnas
   - Busca "cr321_categoria_chatbot"
   - Tipo debe decir: "Búsqueda"
   - Relacionado con: "cr321_grup"

2. **Con Script:**
   ```powershell
   python ver_campos_tabla.py
   ```
   Debe aparecer "cr321_categoria_chatbot" tipo Lookup

---

## 🎯 Siguiente Paso

Una vez creado el campo:

```powershell
# Ejecutar script de migración
python asignar_categorias_chats.py
```

El script:
- Detectará automáticamente el nuevo campo
- Clasificará los 88 chats existentes
- Asignará categorías basándose en palabras clave

---

## 📝 Notas Importantes

⚠️ **ANTES de crear el campo:**
- Ya tienes 88 registros en chats00
- El campo será NULL para todos inicialmente
- Usa el script de migración después de crear

⚠️ **El campo es opcional (no requerido):**
- Chats antiguos pueden no tener categoría
- Chats nuevos deberán asignarse en el webhook

⚠️ **Nombre exacto del campo:**
- Debe ser: `cr321_categoria_chatbot`
- Si usas otro nombre, actualiza:
  - `asignar_categorias_chats.py` (línea 115)
  - `backend/back.py` (líneas con $expand)
  - `backend/goot.py` (líneas con $expand)

---

## 🔗 Referencias

- **Documentación completa:** `docs/NUEVA_ESTRUCTURA_CHATS_CATEGORIA.md`
- **Script de migración:** `asignar_categorias_chats.py`
- **Análisis inicial:** `analizar_relacion_chats_grupo.py`

---

## 💡 Troubleshooting

### Error: "El nombre ya existe"
→ El campo ya fue creado antes. Verifica en la lista de columnas.

### Error: "No se puede relacionar con cr321_grup"
→ Verifica que la tabla cr321_grup existe (debe tener 4 grupos).

### Script da error: "Campo no encontrado"
→ El nombre del campo es diferente. Ajusta el script con el nombre correcto.

### Chats no muestran categoría
→ Ejecuta el script de migración: `python asignar_categorias_chats.py`

---

## ⏱️ Tiempo Estimado

- Crear campo: **2 minutos**
- Verificar: **1 minuto**
- Ejecutar migración: **5 minutos** (incluye clasificación de 88 chats)
- Actualizar frontend (opcional): **15 minutos**

**Total:** ~20-25 minutos para implementación completa
