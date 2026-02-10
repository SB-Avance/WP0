# Nueva Estructura: chats00 con Campo de Categoría/Intención

**Fecha:** 7 de febrero de 2026  
**Cambio:** Agregar campo Lookup para relacionar chats con categorías de chatbot

---

## 📋 Resumen del Cambio

Se agregará un **nuevo campo Lookup** en la tabla `chats00` (cr321_adatawp0s) que apunte a la tabla `grup` (cr321_grups) para identificar la **intención/categoría** de cada conversación.

### ¿Por qué este cambio?

Actualmente hay confusión entre dos conceptos:
- **Estados** del chat (Sin atender, En curso, Resueltas)
- **Categorías/Intenciones** del chatbot (Ticket, Cotización, Información, Agente)

---

## 🎯 Estructura Nueva vs Actual

### ANTES (Actual)
```
chats00
├─ cr321_grupo (Integer)
│  └─ Valores: 1, 2, 3, 4
│     └─ Significado ambiguo: ¿estados o categorías?
```

### DESPUÉS (Nuevo)
```
chats00
├─ cr321_grupo (Integer) - MANTENER
│  └─ Estados del chat:
│     ├─ 1 = Sin atender
│     ├─ 2 = En curso
│     └─ 3 = Resueltas
│
├─ cr321_categoria_chatbot (Lookup) - NUEVO ✨
   └─ Relación → grup
      ├─ Solicitud Ticket (ID: 0001, Tipo: 462410000)
      ├─ Cotización (ID: 0002, Tipo: 462410001)
      ├─ Información (ID: 0003, Tipo: 462410002)
      └─ Solicitar Agente (ID: 0004, Tipo: 462410003)
```

---

## 🔧 Implementación en Power Apps

### Paso 1: Crear Campo Lookup

1. **Power Apps** → https://make.powerapps.com
2. **Tablas** → Buscar `cr321_adatawp0` (chats00)
3. **Columnas** → **+ Nueva columna**
4. Configurar:
   ```
   Nombre para mostrar: Categoría Chatbot
   Nombre: cr321_categoria_chatbot
   Tipo de datos: Búsqueda (Lookup)
   Tabla relacionada: cr321_grup
   ```
5. **Guardar**

### Paso 2: Agregar a Formularios (Opcional)

Si quieres que sea visible en Power Apps:
1. **Formularios** → Abrir el formulario principal
2. Arrastrar campo "Categoría Chatbot" al diseño
3. **Guardar** → **Publicar**

---

## 💻 Cambios en el Código Backend

### Archivos a Actualizar

#### 1. `backend/back.py` - Lista de conversaciones

**ANTES:**
```python
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$top={limit}"
```

**DESPUÉS:**
```python
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$top={limit}"
url += "&$expand=cr321_categoria_chatbot($select=cr321_nombre,cr321_tipo)"
```

**Respuesta incluirá:**
```json
{
  "cr321_adatawp0id": "...",
  "cr321_grupo": 1,
  "cr321_categoria_chatbot": {
    "cr321_nombre": "Solicitud Ticket",
    "cr321_tipo": 462410000
  }
}
```

#### 2. `backend/goot.py` - Mensajes por conversación

Similar al cambio anterior, agregar `$expand` en la consulta.

#### 3. `backend/api/conversations.py` - Si existe

Actualizar para incluir el nuevo campo en las respuestas.

---

## 📊 Datos de Ejemplo

### Registros de chats00 con nuevo campo:

| Teléfono | cr321_grupo (Estado) | cr321_categoria_chatbot (Intención) |
|----------|----------------------|-------------------------------------|
| +1234567890 | 1 (Sin atender) | Cotización |
| +0987654321 | 2 (En curso) | Solicitud Ticket |
| +1122334455 | 3 (Resueltas) | Información |

---

## 🔄 Migración de Datos

### Estrategia de Migración

Dado que ya tienes 88 registros con valores en `cr321_grupo`, necesitas decidir:

**Opción A: Asignar categoría por defecto**
- Todos los chats antiguos → "Información" (o el más común)
- Scripts nuevo: asigna categoría correcta

**Opción B: Analizar histórico**
- Revisar el contenido de los mensajes
- Intentar clasificar automáticamente
- Usar IA/reglas para inferir la intención

**Opción C: Dejar NULL**
- Chats antiguos sin categoría
- Solo chats nuevos tendrán categoría asignada

### Script Incluido

Ver: `asignar_categorias_chats.py` para migración automática.

---

## 🎯 Uso en Aplicación

### Frontend (mobile/components/chats.py)

```python
def mostrar_chat(chat):
    estado = chat['cr321_grupo']  # 1, 2, 3
    categoria = chat.get('cr321_categoria_chatbot', {}).get('cr321_nombre', 'Sin categoría')
    
    # Badge de estado
    color_estado = {1: 'red', 2: 'yellow', 3: 'green'}[estado]
    
    # Icono de categoría
    icono_categoria = {
        'Solicitud Ticket': '🎫',
        'Cotización': '💰',
        'Información': 'ℹ️',
        'Solicitar Agente': '👤'
    }.get(categoria, '❓')
    
    print(f"{icono_categoria} {categoria} - Estado: {color_estado}")
```

### Filtros Avanzados

Ahora podrás filtrar por:
- **Estado**: Sin atender / En curso / Resueltas
- **Categoría**: Ticket / Cotización / Información / Agente
- **Combinación**: "Tickets sin atender", "Cotizaciones en curso"

```python
# API endpoint con filtros combinados
GET /api/conversations?estado=1&categoria=Ticket
GET /api/conversations?estado=2&categoria=Cotizacion
```

---

## ✅ Checklist de Implementación

- [ ] 1. Crear campo `cr321_categoria_chatbot` en Power Apps
- [ ] 2. Actualizar `backend/back.py` para incluir $expand
- [ ] 3. Actualizar `backend/goot.py` para incluir $expand
- [ ] 4. Ejecutar script de migración de datos (opcional)
- [ ] 5. Actualizar frontend para mostrar categorías
- [ ] 6. Agregar filtros por categoría en la UI
- [ ] 7. Modificar webhook para asignar categoría automáticamente
- [ ] 8. Probar con datos reales

---

## 🚀 Mejoras Futuras

Con este cambio, podrás implementar:

1. **Dashboard mejorado**
   - Gráfico: Tickets por estado
   - Gráfico: Conversaciones por categoría
   - KPIs: Tiempo promedio por categoría

2. **Enrutamiento inteligente**
   - Tickets → Agente especializado en soporte
   - Cotizaciones → Equipo de ventas
   - Información → Bot automático

3. **Análisis de chatbot**
   - ¿Qué intención es más común?
   - ¿Qué categoría tiene mejor conversión?
   - ¿Dónde el bot falla más?

---

## 📚 Referencias

- Ver grupos disponibles: `python analizar_relacion_chats_grupo.py`
- Script de asignación: `asignar_categorias_chats.py`
- Documentación API: `docs/MAPA_APLICACION.md`
