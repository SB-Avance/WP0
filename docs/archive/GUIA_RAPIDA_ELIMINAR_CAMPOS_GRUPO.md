# ⚡ Guía Rápida: Eliminar Campos cr321_1, cr321_3, cr321_4

## 🎯 Problema
No puedes eliminar los campos `cr321_1`, `cr321_3`, `cr321_4` de la tabla de usuarios porque tienen dependencias activas.

## 📋 Solución en 3 Pasos

### PASO 0: Ver Dependencias Rápido (2 minutos) ⚡ RECOMENDADO

#### Opción A: Script Automático (MÁS RÁPIDO) ⚡
```bash
# Ejecuta este script para ver dependencias instantáneamente
python ver_dependencias_campos.py
```

**El script te mostrará:**
- ✅ Listado completo de dependencias de cr321_1, cr321_3, cr321_4
- ✅ Tipo de cada dependencia (Vista, Formulario, Flujo, etc.)
- ✅ Cantidad exacta de componentes que usan cada campo
- ✅ Acciones específicas recomendadas

**Ventajas:**
- ⚡ 2 minutos vs 10-15 minutos manual
- 📊 Información detallada y estructurada
- 🎯 Te dice exactamente qué hacer

#### Opción B: Interfaz de Power Apps (Manual)
```
1. Abrir Power Apps (https://make.powerapps.com)
2. Ir a: Tablas → cr321_usuarios → Columnas
3. Click en campo "cr321_1" (o cr321_3, cr321_4)
4. Click en "..." → "Ver dependencias"
5. Anotar qué componentes lo usan:
   - ¿Vistas?
   - ¿Formularios?
   - ¿Flujos de Power Automate?
   - ¿Apps?
   - ¿Reglas de negocio?
```

**Captura de pantalla recomendada:** Tomar screenshot de la ventana de dependencias

---

### PASO 1: Ver Dependencias (5 minutos)
```
1. Abrir Power Apps (https://make.powerapps.com)
2. Ir a: Tablas → cr321_usuarios → Columnas
3. Click en campo "cr321_1" (o cr321_3, cr321_4)
4. Click en "..." → "Ver dependencias"
5. Anotar qué componentes lo usan:
   - ¿Vistas?
   - ¿Formularios?
   - ¿Flujos de Power Automate?
   - ¿Apps?
   - ¿Reglas de negocio?
```

**Captura de pantalla recomendada:** Tomar screenshot de la ventana de dependencias

---

### PASO 2: Remover de Vistas y Formularios (15-30 min)

#### A. Vistas
```
1. Power Apps → Tablas → cr321_usuarios → Vistas
2. Para cada vista:
   a. Abrir en editor
   b. Si tiene columnas cr321_1, cr321_3 o cr321_4:
      - Seleccionar columna
      - Click "Remover"
   c. Guardar y cerrar
3. Publicar todas las vistas
```

#### B. Formularios
```
1. Power Apps → Tablas → cr321_usuarios → Formularios
2. Para cada formulario:
   a. Abrir editor de formularios
   b. Buscar campos cr321_1, cr321_3, cr321_4 en el diseño
   c. Si están presentes:
      - Seleccionar el campo
      - Click derecho → "Remover"
   d. Guardar
   e. Publicar
```

---

### PASO 3: Migrar Datos (30 minutos)

#### Opción A: Script Automático (Recomendado)
```bash
# Ejecutar el script de migración
python migrar_grupos_booleanos_a_relaciones.py
```

El script:
- ✅ Lee todos los usuarios con cr321_1/3/4 = true
- ✅ Crea relaciones en cr321_usuario_gruposes
- ✅ Valida que todo fue migrado correctamente

#### Opción B: Manual (Solo si tienes pocos usuarios)
```
Para cada usuario con cr321_1=true:
  POST /api/usuario-grupos
  {
    "usuario_id": "{guid_del_usuario}",
    "grupo_id": "{guid_del_grupo_1}"
  }

Repetir para cr321_3 y cr321_4
```

---

## ✅ Después de Completar los 3 Pasos

1. **Intentar eliminar el campo nuevamente:**
   ```
   Power Apps → Tablas → cr321_usuarios → Columnas → cr321_1
   Click "..." → "Eliminar"
   ```

2. **Si aún da error:**
   - Click en "Ver dependencias" nuevamente
   - Verificar qué componente falta actualizar
   - Repetir PASO 2 para ese componente

3. **Una vez eliminado:**
   - Repetir para `cr321_3`
   - Repetir para `cr321_4`
   - **Publicar todas las personalizaciones**

---

## 🚨 Si No Puedes Eliminar Aún

### Solución Temporal: Ocultar
```
1. Power Apps → Tablas → cr321_usuarios → Columnas → cr321_1
2. Click "..." → "Editar"
3. Cambiar "Nombre para mostrar" a: "DEPRECATED - No usar"
4. En "Descripción" agregar: "Usar cr321_usuario_gruposes"
5. Marcar como "Oculto" (si la opción está disponible)
6. Guardar
```

Esto impide que aparezcan en nuevas vistas/formularios.

---

## 📞 Errores Comunes

### Error: "Este campo está siendo usado en 1 o más vistas"
**Solución:** Ir a cada vista y remover la columna (PASO 2A)

### Error: "Este campo está siendo usado en 1 o más formularios"
**Solución:** Editar formularios y remover el campo (PASO 2B)

### Error: "Este campo está siendo usado por un proceso"
**Solución:** 
1. Ir a Power Automate → Mis flujos
2. Buscar flujos que usan "cr321_usuarios"
3. Desactivar o modificar esos flujos

### Error: "Este campo tiene dependencias de seguridad"
**Solución:** Contactar administrador para revisar roles de seguridad

---

## 📄 Documentación Completa

Ver guía detallada: [DEPENDENCIAS_CAMPOS_GRUPO_USUARIOS.md](DEPENDENCIAS_CAMPOS_GRUPO_USUARIOS.md)

---

## ⏱️ Tiempo Estimado Total

- **Mínimo:** 30 minutos (sin dependencias complejas)
- **Típico:** 1-2 horas (con vistas/formularios/flujos)
- **Máximo:** 4 horas (si hay muchas apps o flujos dependientes)

---

## ✅ Checklist Final

- [ ] Dependencias identificadas (Ver dependencias en Power Apps)
- [ ] Campos removidos de todas las vistas
- [ ] Campos removidos de todos los formularios
- [ ] Datos migrados a cr321_usuario_gruposes
- [ ] Flujos de Power Automate actualizados (si aplica)
- [ ] Reglas de negocio actualizadas (si aplica)
- [ ] Apps actualizadas (si aplica)
- [ ] Campo cr321_1 eliminado ✅
- [ ] Campo cr321_3 eliminado ✅
- [ ] Campo cr321_4 eliminado ✅
- [ ] Personalizaciones publicadas ✅

---

**Última actualización:** 7 de febrero de 2026  
**Autor:** Sistema automatizado
