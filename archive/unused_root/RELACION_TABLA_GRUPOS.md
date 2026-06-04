# 🔗 RELACIÓN: JSON ↔ Tabla cr321_grupos

## 📊 TUS DATOS REALES

### Tabla cr321_grupos (Actual en Dataverse)

```
┌──────────┬─────────────────┬──────┬─────────────┬────────────────────────────────────────┐
│ groupid  │ nombre          │ tipo │ descripcion │ grup* (cr321_grupoid - GUID)           │
├──────────┼─────────────────┼──────┼─────────────┼────────────────────────────────────────┤
│ 0000     │ General         │  A   │             │ 3fc21e02-1c06-f111-8d07-7ced8c         │
├──────────┼─────────────────┼──────┼─────────────┼────────────────────────────────────────┤
│ 0001     │ Soporte         │  A   │ aa          │ 067c7ba2-9f03-f111-8d07-7ced8          │
├──────────┼─────────────────┼──────┼─────────────┼────────────────────────────────────────┤
│ 0002     │ Ventas          │  B   │ bb          │ 32dc7358-5704-f111-8d07-7ced8          │
├──────────┼─────────────────┼──────┼─────────────┼────────────────────────────────────────┤
│ 0003     │ Administracion  │  C   │ cc          │ e2927859-5704-f111-8d07-7ced8          │
├──────────┼─────────────────┼──────┼─────────────┼────────────────────────────────────────┤
│ 0004     │ Contabilidad    │  D   │ dd          │ 9b8a9262-5704-f111-8d07-0022d          │
└──────────┴─────────────────┴──────┴─────────────┴────────────────────────────────────────┘
```

**Campo Clave:** `grup*` (cr321_grupoid) = GUID único de cada grupo

---

## 🎯 CONEXIÓN: JSON → Tabla

### Ejemplo 1: Menú → Grupo "Soporte"

```json
{
  "numero": "1.1",
  "nombre": "Incidente Técnico",
  "handler": "A001",
  "grupo_id": "{067c7ba2-9f03-f111-8d07-7ced8}"  ← Este GUID
}
```

**Se conecta con:**

```
Tabla cr321_grupos
┌──────────┬─────────┬──────┬────────────────────────────────────────┐
│ groupid  │ nombre  │ tipo │ cr321_grupoid (GUID)                   │
├──────────┼─────────┼──────┼────────────────────────────────────────┤
│ 0001     │ Soporte │  A   │ 067c7ba2-9f03-f111-8d07-7ced8  ← MATCH │
└──────────┴─────────┴──────┴────────────────────────────────────────┘
```

✅ **Resultado:** Ticket asignado al grupo **"Soporte"** (0001)

---

### Ejemplo 2: Menú → Grupo "Ventas"

```json
{
  "numero": "2.1",
  "nombre": "Solicitar Cotización",
  "handler": "C001",
  "grupo_id": "{32dc7358-5704-f111-8d07-7ced8}"  ← Este GUID
}
```

**Se conecta con:**

```
Tabla cr321_grupos
┌──────────┬────────┬──────┬────────────────────────────────────────┐
│ groupid  │ nombre │ tipo │ cr321_grupoid (GUID)                   │
├──────────┼────────┼──────┼────────────────────────────────────────┤
│ 0002     │ Ventas │  B   │ 32dc7358-5704-f111-8d07-7ced8  ← MATCH │
└──────────┴────────┴──────┴────────────────────────────────────────┘
```

✅ **Resultado:** Ticket asignado al grupo **"Ventas"** (0002)

---

### Ejemplo 3: Menú → Grupo "Contabilidad"

```json
{
  "numero": "4.1",
  "nombre": "Consulta Contable",
  "handler": "F001",
  "grupo_id": "{9b8a9262-5704-f111-8d07-0022d}"  ← Este GUID
}
```

**Se conecta con:**

```
Tabla cr321_grupos
┌──────────┬──────────────┬──────┬────────────────────────────────────────┐
│ groupid  │ nombre       │ tipo │ cr321_grupoid (GUID)                   │
├──────────┼──────────────┼──────┼────────────────────────────────────────┤
│ 0004     │ Contabilidad │  D   │ 9b8a9262-5704-f111-8d07-0022d  ← MATCH │
└──────────┴──────────────┴──────┴────────────────────────────────────────┘
```

✅ **Resultado:** Ticket asignado al grupo **"Contabilidad"** (0004)

---

## 🔄 FLUJO COMPLETO

```
┌────────────────────────────────────────────────────────────────────┐
│ 1. Usuario en WhatsApp                                             │
│    Mensaje: "1.1"                                                  │
└────────────────────┬───────────────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────────────┐
│ 2. Sistema carga JSON desde cr321_chatbots.cr321_config           │
│    Encuentra submenu "1.1": "Incidente Técnico"                   │
│    Lee: "grupo_id": "{067c7ba2-9f03-f111-8d07-7ced8}"             │
└────────────────────┬───────────────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────────────┐
│ 3. Sistema ejecuta Handler A001                                   │
│    Captura información del usuario (nombre, asunto, empresa)       │
└────────────────────┬───────────────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────────────┐
│ 4. Sistema crea ticket en Dataverse                               │
│                                                                    │
│    cr321_conversaciones (nuevo registro)                           │
│    ├─ cr321_conversacionid: [auto-generado]                       │
│    ├─ cr321_titulo: "Incidente Técnico"                           │
│    ├─ cr321_estado: "Abierto"                                     │
│    │                                                               │
│    └─ cr321_grupoid (Lookup): {067c7ba2-9f03-f111-8d07-7ced8} ◄──┐│
│                                                                    ││
└────────────────────────────────────────────────────────────────────┘│
                                                                      │
                     ┌────────────────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────────────┐
│ 5. Lookup resuelve el grupo en cr321_grupos                       │
│                                                                    │
│    cr321_grupos                                                    │
│    ├─ cr321_grupoid: {067c7ba2-9f03-f111-8d07-7ced8} ← MATCH!    │
│    ├─ groupid: "0001"                                             │
│    ├─ nombre: "Soporte"                                           │
│    ├─ tipo: "A"                                                   │
│    └─ descripcion: "aa"                                           │
└────────────────────┬───────────────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────────────┐
│ 6. RESULTADO FINAL                                                │
│                                                                    │
│    ✅ Ticket creado y asignado a grupo "Soporte" (0001)           │
│    ✅ Agentes del grupo "Soporte" pueden ver el ticket            │
│    ✅ Usuario recibe confirmación                                 │
└────────────────────────────────────────────────────────────────────┘
```

---

## 📋 MAPEO COMPLETO: Submenus → Grupos

### Configuración Recomendada

```
┌─────────┬──────────────────────────┬────────────────────────────┬──────────────────┐
│ Submenu │ Nombre                   │ Grupo Asignado             │ GUID             │
├─────────┼──────────────────────────┼────────────────────────────┼──────────────────┤
│ 1.1     │ Incidente Técnico        │ Soporte (0001)             │ 067c7ba2-9f03... │
│ 1.2     │ Consulta General         │ General (0000)             │ 3fc21e02-1c06... │
├─────────┼──────────────────────────┼────────────────────────────┼──────────────────┤
│ 2.1     │ Solicitar Cotización     │ Ventas (0002)              │ 32dc7358-5704... │
│ 2.2     │ Información Productos    │ Ventas (0002)              │ 32dc7358-5704... │
├─────────┼──────────────────────────┼────────────────────────────┼──────────────────┤
│ 3.1     │ Solicitud Administrativa │ Administracion (0003)      │ e2927859-5704... │
├─────────┼──────────────────────────┼────────────────────────────┼──────────────────┤
│ 4.1     │ Consulta Contable        │ Contabilidad (0004)        │ 9b8a9262-5704... │
│ 4.2     │ Reporte de Pagos         │ Contabilidad (0004)        │ 9b8a9262-5704... │
└─────────┴──────────────────────────┴────────────────────────────┴──────────────────┘
```

---

## 🔍 VALIDACIÓN DE LA RELACIÓN

### Script: validar_grupos_menu.py

```bash
python validar_grupos_menu.py
```

**Qué hace:**
1. ✅ Lee JSON de cr321_chatbots.cr321_config
2. ✅ Extrae todos los `grupo_id` de cada submenu
3. ✅ Consulta tabla cr321_grupos
4. ✅ Verifica que cada GUID exista
5. ✅ Muestra nombre del grupo para cada submenu

**Salida esperada:**

```
============================================================
VALIDACIÓN DE GRUPOS DEL MENÚ
============================================================

→ Consultando grupos válidos en cr321_grupos...
  ✓ 5 grupos disponibles (General, Soporte, Ventas, Administracion, Contabilidad)

→ Validando grupos del menú...

✅ GRUPOS VÁLIDOS (7):
┌──────────────────────────────────────────────────────────┐
│ 1.1    Incidente Técnico                                 │
│        → Grupo: Soporte (0001)                           │
│        → GUID: 067c7ba2-9f03-f111-8d07-7ced8             │
├──────────────────────────────────────────────────────────┤
│ 1.2    Consulta General                                  │
│        → Grupo: General (0000)                           │
│        → GUID: 3fc21e02-1c06-f111-8d07-7ced8c            │
├──────────────────────────────────────────────────────────┤
│ 2.1    Solicitar Cotización                              │
│        → Grupo: Ventas (0002)                            │
│        → GUID: 32dc7358-5704-f111-8d07-7ced8             │
├──────────────────────────────────────────────────────────┤
│ 4.1    Consulta Contable                                 │
│        → Grupo: Contabilidad (0004)                      │
│        → GUID: 9b8a9262-5704-f111-8d07-0022d             │
└──────────────────────────────────────────────────────────┘

RESUMEN
✅ Válidos:   7
❌ Inválidos: 0
⚪ Sin grupo: 0
📊 Total:     7

✅ Todos los grupos son válidos y conectados correctamente
```

---

## ⚠️ ERRORES COMUNES

### Error 1: GUID Incorrecto

```json
❌ "grupo_id": "{12345678-1234-1234-1234-123456789ABC}"
```

**Problema:** Este GUID no existe en tu tabla cr321_grupos

**Solución:** Usar uno de tus GUIDs reales:
- `{3fc21e02-1c06-f111-8d07-7ced8c}` → General
- `{067c7ba2-9f03-f111-8d07-7ced8}` → Soporte
- `{32dc7358-5704-f111-8d07-7ced8}` → Ventas
- `{e2927859-5704-f111-8d07-7ced8}` → Administracion
- `{9b8a9262-5704-f111-8d07-0022d}` → Contabilidad

---

### Error 2: Formato Incorrecto

```json
❌ "grupo_id": "067c7ba2-9f03-f111-8d07-7ced8"  // Sin llaves
✅ "grupo_id": "{067c7ba2-9f03-f111-8d07-7ced8}"  // Con llaves
```

---

### Error 3: GUID Parcial

```json
❌ "grupo_id": "{067c7ba2-9f03}"  // Incompleto
✅ "grupo_id": "{067c7ba2-9f03-f111-8d07-7ced8}"  // Completo
```

**Nota:** En la captura veo GUIDs parciales. Asegúrate de copiar el GUID completo de 36 caracteres.

---

## 📝 CHECKLIST DE IMPLEMENTACIÓN

```
□ 1. Copiar GUIDs completos desde Dataverse
   └─► Ir a cr321_grupos → Ver campo cr321_grupoid completo

□ 2. Actualizar JSON con GUIDs reales
   └─► Usar archivo: ejemplo_json_con_tus_grupos_reales.json

□ 3. Insertar JSON en cr321_chatbots
   └─► Campo: cr321_config
   └─► Registro: "Chatbot1"

□ 4. Validar relación
   └─► python validar_grupos_menu.py
   └─► Verificar: "✅ Todos los grupos válidos"

□ 5. Probar sistema
   └─► python sistema_menu_json.py
   └─► Simular selección de menú
```

---

## 🎯 RESUMEN VISUAL

```
cr321_chatbots                          cr321_grupos
     │                                       │
     │  cr321_config (JSON)                  │  cr321_grupoid (PK)
     │  {                                    │
     │    "grupo_id":                        │
     │    "{067c7ba2-9f03...}"  ─────────────┼──► {067c7ba2-9f03...}
     │  }                                    │      ↓
     │                                       │   nombre: "Soporte"
     │                                       │   groupid: "0001"
     │                                       │   tipo: "A"
     │
   REFERENCIA                             TABLA REAL
   en JSON                                con datos
```

**Regla:** El `grupo_id` en el JSON debe ser un GUID válido de `cr321_grupoid` en tu tabla `cr321_grupos`.

---

¿Quieres que genere el JSON final con todos tus GUIDs reales y completos? 🚀
