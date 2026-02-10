# 🎯 Sugerencias - Próximos Pasos

**Fecha:** Febrero 2026  
**Estado después de migración Lookup:** ✅ Completada

---

## 🚀 Prioridad ALTA (Implementar esta semana)

### 1. **API de Consulta de Relaciones** ⭐⭐⭐
**Descripción:** Crear endpoints que aprovechen los nuevos Lookups

**Implementación:**
```python
# Archivo: backend/api/chats_extended.py

@bp.route('/api/chats/con-contacto', methods=['GET'])
def get_chats_con_contacto():
    """Obtener chats expandiendo relación de contacto"""
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s"
    params = {
        "$select": "cr321_mensaje,cr321_fechahora",
        "$expand": "cr321_contactorelacion($select=cr321_fromnombre,cr321_telefono,cr321_correo)",
        "$filter": "_cr321_contactorelacion_value ne null",
        "$orderby": "cr321_fechahora desc",
        "$top": 50
    }
    # ... implementar

@bp.route('/api/chats/por-grupo/<grupo_id>', methods=['GET'])
def get_chats_por_grupo(grupo_id):
    """Obtener todos los chats de un grupo específico"""
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s"
    params = {
        "$select": "cr321_mensaje,cr321_fechahora",
        "$expand": "cr321_grupoid($select=cr321_nombre,cr321_tipo)",
        "$filter": f"_cr321_grupoid_value eq {grupo_id}",
        "$orderby": "cr321_fechahora desc"
    }
    # ... implementar
```

**Beneficios:**
- ✅ Consultas más eficientes con $expand
- ✅ Un solo request en vez de múltiples
- ✅ Datos relacionados automáticamente

**Tiempo estimado:** 2-3 horas

---

### 2. **Dashboard de Métricas por Grupo** ⭐⭐⭐
**Descripción:** Panel que muestre estadísticas usando las relaciones Lookup

**Métricas sugeridas:**
```python
# backend/api/reportes.py

@bp.route('/api/reportes/metricas-grupos', methods=['GET'])
def get_metricas_grupos():
    """
    Retorna:
    - Total mensajes por grupo
    - Contactos únicos por grupo
    - Tiempo promedio de respuesta por grupo
    - Distribución horaria por grupo
    """
    # Usar groupby en OData o procesar en Python
    return {
        "grupos": [
            {
                "grupo_id": "xxx",
                "nombre": "Ventas",
                "total_mensajes": 1250,
                "contactos_unicos": 85,
                "tiempo_respuesta_avg": "2.5 horas",
                "mensajes_hoy": 45
            }
        ]
    }
```

**UI en Frontend:**
```python
# mobile/components/dashboard.py
# Agregar gráficos:
# - Barras: mensajes por grupo
# - Pie: distribución de contactos
# - Línea: tendencia diaria
```

**Tiempo estimado:** 4-5 horas

---

### 3. **Creación Automática de Contactos Mejorada** ⭐⭐
**Descripción:** Optimizar el proceso de auto-creación usando Lookup

**Mejora actual:**
```python
# En backend/api/webhook.py
# ACTUAL: Crear contacto y luego asociar por ID numérico
# MEJORAR: Asociar directamente usando Lookup

def procesar_mensaje_entrante(mensaje):
    telefono = mensaje['from']
    
    # Buscar o crear contacto
    contacto_id = buscar_o_crear_contacto(telefono)
    
    # Guardar mensaje con relación Lookup directa
    nuevo_mensaje = {
        "cr321_mensaje": mensaje['text'],
        "cr321_telefono": telefono,
        "cr321_contactorelacion@odata.bind": f"/cr321_contactos({contacto_id})",  # ✅ Lookup directo
        "cr321_grupoid@odata.bind": f"/cr321_grups({grupo_id})"  # ✅ Lookup directo
    }
    
    # Un solo POST, todo relacionado
    requests.post(url, json=nuevo_mensaje)
```

**Beneficios:**
- ✅ Relación atómica en una sola operación
- ✅ No hay posibilidad de inconsistencias
- ✅ Más rápido (menos requests)

**Tiempo estimado:** 2 horas

---

## 🔧 Prioridad MEDIA (Próximas 2 semanas)

### 4. **API de Categorización de Chats** ⭐⭐
**Descripción:** Endpoint para cambiar grupo de mensajes masivamente

```python
# backend/api/chats_categories.py

@bp.route('/api/chats/cambiar-categoria', methods=['PATCH'])
def cambiar_categoria_masiva():
    """
    Body: {
        "chat_ids": ["id1", "id2", ...],
        "nuevo_grupo_id": "guid-del-grupo"
    }
    """
    # Actualizar en batch usando Lookup
    for chat_id in chat_ids:
        update_data = {
            "cr321_grupoid@odata.bind": f"/cr321_grups({nuevo_grupo_id})"
        }
        # PATCH individual o usar $batch
```

**Caso de uso:**
- Usuario selecciona múltiples chats
- Cambia categoría de "Sin Atender" → "En Curso"
- Sistema actualiza Lookup de todos

**Tiempo estimado:** 3 horas

---

### 5. **Reportes Power BI Ready** ⭐⭐
**Descripción:** Preparar vistas/consultas optimizadas para Power BI

**Crear vistas virtuales:**
```sql
-- En Dataverse o via API personalizada

VIEW vw_mensajes_completos AS
SELECT 
    m.cr321_mensaje,
    m.cr321_fechahora,
    c.cr321_fromnombre as contacto_nombre,
    c.cr321_telefono,
    g.cr321_nombre as grupo_nombre,
    g.cr321_tipo as grupo_tipo
FROM cr321_adatawp0 m
LEFT JOIN cr321_contacto c ON m.cr321_contactorelacion = c.cr321_contactoid
LEFT JOIN cr321_grup g ON m.cr321_grupoid = g.cr321_grupoid
```

**Script helper:**
```python
# reportes_powerbi.py
# Generar JSON con estructura plana para Power BI
# Export a CSV con relaciones resueltas
```

**Tiempo estimado:** 3-4 horas

---

### 6. **Historial de Conversaciones por Contacto** ⭐⭐
**Descripción:** Vista completa del historial usando Lookup

```python
# backend/api/contactos.py

@bp.route('/api/contactos/<contacto_id>/historial', methods=['GET'])
def get_historial_contacto(contacto_id):
    """Todos los mensajes de un contacto con info de grupos"""
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s"
    params = {
        "$select": "cr321_mensaje,cr321_fechahora,cr321_direccion",
        "$expand": "cr321_grupoid($select=cr321_nombre)",
        "$filter": f"_cr321_contactorelacion_value eq {contacto_id}",
        "$orderby": "cr321_fechahora asc"
    }
    # Retornar timeline completo
```

**UI Frontend:**
```python
# mobile/components/contacto_detalle.py
# Mostrar línea de tiempo con:
# - Todos los mensajes históricos
# - En qué grupos ha participado
# - Fechas de primera/última interacción
```

**Tiempo estimado:** 4 horas

---

## 🎨 Prioridad BAJA (Mejoras futuras)

### 7. **Editor Visual de Reglas de Categorización** ⭐
**Descripción:** UI para definir reglas automáticas de asignación a grupos

**Funcionalidad:**
```
Si [mensaje contiene] "precio" O "cotización"
→ Asignar a grupo "Ventas"

Si [hora] entre 22:00 y 08:00
→ Asignar a grupo "Fuera de horario"

Si [contacto nuevo] = Sí
→ Asignar a grupo "Sin atender"
```

**Tiempo estimado:** 8-10 horas

---

### 8. **Sincronización Bidireccional con CRM Externo** ⭐
Si se usa otro CRM además de Dataverse:
- Webhook que sincronice contactos
- Mapeo de campos Lookup a IDs externos
- Cola de sincronización con retry

**Tiempo estimado:** 10-15 horas

---

### 9. **Tests Automatizados** ⭐
```python
# tests/test_lookups.py

def test_crear_mensaje_con_lookup_contacto():
    """Verificar que Lookup se asocia correctamente"""
    # Crear contacto de prueba
    # Crear mensaje asociado
    # Verificar relación en Dataverse
    pass

def test_query_expand_contacto():
    """Verificar $expand funciona"""
    # Query con $expand
    # Verificar que trae datos relacionados
    pass
```

**Tiempo estimado:** 6-8 horas

---

## 📊 Tabla Resumen

| Tarea | Prioridad | Tiempo | Beneficio | Dependencias |
|-------|-----------|--------|-----------|--------------|
| 1. API Relaciones | 🔴 Alta | 2-3h | Alto | Ninguna |
| 2. Dashboard Métricas | 🔴 Alta | 4-5h | Alto | #1 |
| 3. Auto-contactos mejorado | 🔴 Alta | 2h | Medio | Ninguna |
| 4. Categorización masiva | 🟡 Media | 3h | Medio | #1 |
| 5. Reportes Power BI | 🟡 Media | 3-4h | Alto | Ninguna |
| 6. Historial Contacto | 🟡 Media | 4h | Medio | #1 |
| 7. Editor reglas | 🟢 Baja | 8-10h | Medio | #4 |
| 8. Sync CRM externo | 🟢 Baja | 10-15h | Bajo | Depende CRM |
| 9. Tests | 🟢 Baja | 6-8h | Alto | Ninguna |

---

## 🎯 Plan de Acción Recomendado

### Sprint 1 (Esta semana)
```
Día 1-2: Implementar #1 (API Relaciones)
Día 3-4: Implementar #3 (Auto-contactos mejorado)
Día 5: Implementar #2 (Dashboard) - Parte 1
```

### Sprint 2 (Próxima semana)
```
Día 1-2: Completar #2 (Dashboard) - Parte 2
Día 3: Implementar #4 (Categorización masiva)
Día 4-5: Implementar #5 (Reportes Power BI)
```

### Sprint 3 (Semana 3)
```
Día 1-3: Implementar #6 (Historial Contacto)
Día 4-5: Documentación y refinamiento
```

---

## 🔍 Verificaciones Post-Implementación

Después de cada tarea, ejecutar:

```powershell
# Verificar estructura
python verificar_cambios_tabla.py

# Verificar datos
python ver_estado_migracion.py

# Test manual API
curl http://localhost:5000/api/chats/con-contacto

# Verificar logs
# (revisar terminal backend)
```

---

## 📚 Recursos Adicionales

- [OData $expand documentation](https://docs.microsoft.com/odata/concepts/queryoptions-overview)
- [Dataverse Web API](https://docs.microsoft.com/power-apps/developer/data-platform/webapi/overview)
- [Lookup Attributes](https://docs.microsoft.com/power-apps/developer/data-platform/webapi/associate-disassociate-entities-using-web-api)

---

## 💡 Ideas Adicionales

1. **Notificaciones Push:** Cuando mensaje entra a grupo asignado al usuario
2. **SLA Tracking:** Medir tiempo "Sin Atender" → "Resuelta" por grupo
3. **Plantillas de Respuesta:** Por grupo/categoría
4. **Etiquetas adicionales:** Además de grupos, tags personalizados
5. **Búsqueda full-text:** En mensajes con filtros por grupo/contacto

---

**🎉 ¡El sistema está listo para crecer!**  
Con las relaciones Lookup implementadas, ahora el cielo es el límite.
