# 📋 Guía Visual: Crear Tablas en Dataverse

## 🎯 Objetivo
Crear 4 tablas nuevas en Microsoft Dataverse para el sistema de chatbot.

---

## 📍 Paso 1: Acceder a Power Apps

1. Ir a: https://make.powerapps.com
2. Iniciar sesión con tu cuenta
3. Seleccionar tu entorno (arriba a la derecha)

---

## 🗂️ Paso 2: Crear las Tablas

### Tabla 1: cr321_grupos

**Navegación:** Tablas → Nueva tabla → Crear tabla

**Información básica:**
```
Nombre para mostrar: Grupos
Nombre plural: Grupos
Nombre: cr321_grupos
```

**Campos a crear:**

| Campo | Tipo | Longitud | ¿Obligatorio? | Descripción |
|-------|------|----------|---------------|-------------|
| cr321_idgrupo | Número entero | - | ✅ Sí | ID consecutivo del grupo |
| cr321_nombre | Texto | 100 | ✅ Sí | Nombre del grupo |
| cr321_tipo | Conjunto de opciones | - | ✅ Sí | Ver opciones abajo |
| cr321_descripcion | Texto | 500 | ❌ No | Descripción del grupo |

**Opciones para cr321_tipo:**
```
Etiqueta: Tipo A    Valor: 462410000
Etiqueta: Tipo B    Valor: 462410001
Etiqueta: Tipo C    Valor: 462410002
```

✅ **Guardar y publicar**

---

### Tabla 2: cr321_estados

**Información básica:**
```
Nombre para mostrar: Estados
Nombre plural: Estados
Nombre: cr321_estados
```

**Campos a crear:**

| Campo | Tipo | Longitud | ¿Obligatorio? | Descripción |
|-------|------|----------|---------------|-------------|
| cr321_idestado | Número entero | - | ✅ Sí | ID consecutivo del estado |
| cr321_nombre | Texto | 100 | ✅ Sí | Nombre del estado |
| cr321_descripcion | Texto | 500 | ❌ No | Descripción del estado |

✅ **Guardar y publicar**

---

### Tabla 3: cr321_tickets

**Información básica:**
```
Nombre para mostrar: Tickets
Nombre plural: Tickets
Nombre: cr321_tickets
```

**Campos a crear:**

| Campo | Tipo | Longitud/Relación | ¿Obligatorio? | Descripción |
|-------|------|-------------------|---------------|-------------|
| cr321_idticket | Número entero | - | ✅ Sí | ID consecutivo del ticket |
| cr321_fromnombre | Texto | 100 | ✅ Sí | Nombre del contacto |
| cr321_telefono | Texto | 20 | ✅ Sí | Teléfono del contacto |
| cr321_empresa | Texto | 200 | ❌ No | Empresa del contacto |
| cr321_descripcion | Texto multilínea | 2000 | ❌ No | Descripción del problema |
| cr321_tipo | Conjunto de opciones | - | ✅ Sí | Ver opciones abajo |
| cr321_estado | Número entero | - | ✅ Sí | Estado actual |
| cr321_grupoid | Búsqueda | → cr321_grupos | ❌ No | Grupo asignado |
| cr321_fechacreacion | Fecha y hora | - | ✅ Sí | Fecha de creación |
| cr321_fechaactualizacion | Fecha y hora | ✅ Sí | Fecha de actualización |

**Opciones para cr321_tipo:**
```
Etiqueta: Soporte            Valor: 462410000
Etiqueta: Cotización         Valor: 462410001
Etiqueta: Información        Valor: 462410002
Etiqueta: Atención Agente    Valor: 462410003
```

**Para cr321_grupoid (Campo de búsqueda):**
- Tipo: Búsqueda
- Tabla relacionada: cr321_grupos
- Relación: Muchos a uno (N:1)

✅ **Guardar y publicar**

---

### Tabla 4: cr321_usuario_grupos

**Información básica:**
```
Nombre para mostrar: Usuario Grupos
Nombre plural: Usuario Grupos
Nombre: cr321_usuario_grupos
```

**Campos a crear:**

| Campo | Tipo | Relación | ¿Obligatorio? | Descripción |
|-------|------|----------|---------------|-------------|
| cr321_usuarioid | Búsqueda | → cr321_usuarios | ✅ Sí | Usuario asignado |
| cr321_grupoid | Búsqueda | → cr321_grupos | ✅ Sí | Grupo asignado |

**Para cr321_usuarioid (Campo de búsqueda):**
- Tipo: Búsqueda
- Tabla relacionada: cr321_usuarios
- Relación: Muchos a uno (N:1)

**Para cr321_grupoid (Campo de búsqueda):**
- Tipo: Búsqueda
- Tabla relacionada: cr321_grupos
- Relación: Muchos a uno (N:1)

✅ **Guardar y publicar**

---

## 🎯 Paso 3: Verificar

Después de crear las 4 tablas, verificar que todas están publicadas:

```
✅ cr321_grupos
✅ cr321_estados
✅ cr321_tickets
✅ cr321_usuario_grupos
```

---

## 🚀 Paso 4: Inicializar Datos

Una vez creadas las tablas, ejecutar:

```bash
python init_dataverse.py
```

Esto creará:
- ✅ 4 grupos tipo A (opciones del menú WhatsApp)
- ✅ 6 estados de tickets

---

## 📸 Capturas de Pantalla de Ayuda

### Crear campo de Texto:
```
1. En la tabla, clic en "Agregar campo"
2. Nombre para mostrar: [nombre del campo]
3. Tipo de datos: Texto
4. Longitud máxima: [según tabla arriba]
5. ¿Obligatorio?: [según tabla arriba]
6. Guardar
```

### Crear campo de Conjunto de opciones:
```
1. En la tabla, clic en "Agregar campo"
2. Nombre para mostrar: [nombre del campo]
3. Tipo de datos: Conjunto de opciones
4. Conjunto de opciones: Nuevo conjunto de opciones
5. Agregar cada opción con su etiqueta y valor
6. Guardar
```

### Crear campo de Búsqueda:
```
1. En la tabla, clic en "Agregar campo"
2. Nombre para mostrar: [nombre del campo]
3. Tipo de datos: Búsqueda
4. Tabla relacionada: [seleccionar tabla]
5. Tipo de relación: Muchos a uno (N:1)
6. Guardar
```

---

## 🆘 Solución de Problemas

**Problema:** No puedo crear campos con prefijo cr321_
- **Solución:** Asegúrate de que tu editor de soluciones tiene el prefijo "cr321" configurado

**Problema:** No encuentro la opción "Conjunto de opciones"
- **Solución:** Busca "Choice" en inglés, es el mismo tipo de campo

**Problema:** Error al crear relación de búsqueda
- **Solución:** Asegúrate de que la tabla relacionada ya existe y está publicada

---

## ✅ Checklist Final

Antes de continuar, verificar:

- [ ] Las 4 tablas están creadas
- [ ] Todos los campos están agregados
- [ ] Los conjuntos de opciones tienen los valores correctos (462410000, etc.)
- [ ] Las relaciones de búsqueda están configuradas
- [ ] Todas las tablas están publicadas

---

## ➡️ Siguiente Paso

Una vez completado todo:

```bash
python init_dataverse.py
```

---

**Nota:** Este proceso toma aproximadamente 20-30 minutos la primera vez.

**Tip:** Puedes usar la opción "Importar desde Excel" para crear múltiples campos a la vez.
