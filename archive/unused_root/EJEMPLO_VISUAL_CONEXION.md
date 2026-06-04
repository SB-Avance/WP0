# 📊 EJEMPLO VISUAL: Conexión JSON ↔ Tabla cr321_grupos

## 🎯 Cómo se Conectan

### 1️⃣ Tabla cr321_grupos en Dataverse

```
┌────────────────────────────────────────────────────────────────────┐
│ Tabla: cr321_grupos                                                │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│ cr321_grupoid (GUID - Primary Key)                                │
│ cr321_nombre (Text)                                                │
│ cr321_descripcion (Text)                                           │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

EJEMPLO DE REGISTROS REALES:

┌──────────────────────────────────────────────────────────────────┐
│ cr321_grupoid: a1b2c3d4-1234-5678-90ab-cdef12345678             │
│ cr321_nombre: Soporte Técnico                                    │
│ cr321_descripcion: Grupo de soporte técnico nivel 1             │
├──────────────────────────────────────────────────────────────────┤
│ cr321_grupoid: b2c3d4e5-2345-6789-01bc-def123456789             │
│ cr321_nombre: Mesa de Servicio                                   │
│ cr321_descripcion: Mesa de servicio general                      │
├──────────────────────────────────────────────────────────────────┤
│ cr321_grupoid: c3d4e5f6-3456-7890-12cd-ef1234567890             │
│ cr321_nombre: CAB - Comité de Cambios                            │
│ cr321_descripcion: Gestión de cambios RFC                        │
├──────────────────────────────────────────────────────────────────┤
│ cr321_grupoid: d4e5f6a7-4567-8901-23de-f12345678901             │
│ cr321_nombre: Ventas                                             │
│ cr321_descripcion: Equipo comercial y cotizaciones               │
└──────────────────────────────────────────────────────────────────┘
```

---

### 2️⃣ JSON en cr321_config (Tabla cr321_chatbots)

```json
{
  "menus": [
    {
      "numero": "1",
      "nombre": "Solicitud Ticket",
      "submenus": [
        {
          "numero": "1.1",
          "nombre": "Incidente Técnico",
          "handler": "A001",

          ┌─────────────────────────────────────────────────┐
          │ "grupo_id": "{a1b2c3d4-1234-5678-90ab-cdef...}" │ ◄─┐
          └─────────────────────────────────────────────────┘   │
                                                                │
          Este GUID debe coincidir exactamente ───────────────┘
          con un cr321_grupoid de la tabla cr321_grupos
        }
      ]
    }
  ]
}
```

---

### 3️⃣ Conexión en Acción

```
FLUJO COMPLETO:

1. Usuario selecciona: "1.1 - Incidente Técnico"
   │
   ▼
2. Sistema lee JSON de cr321_config
   │
   ▼
3. Encuentra: "grupo_id": "{a1b2c3d4-1234-5678-90ab-cdef12345678}"
   │
   ▼
4. Crea ticket en Dataverse con:
   │
   ├─► cr321_conversacionid (la conversación actual)
   │
   └─► cr321_grupoid (lookup) ──► Apunta a cr321_grupos
                                   donde cr321_grupoid = a1b2c3d4...

5. Resultado: Ticket asignado a "Soporte Técnico"
```

---

## 🔍 Ejemplo Real Paso a Paso

### PASO 1: Ver Grupos Disponibles

```bash
python listar_grupos_dataverse.py
```

**SALIDA:**
```
┌──────────────────────────────────────────────────────────┐
│ GRUPOS DISPONIBLES (Tabla: cr321_grupos)                │
├──────────────────────────────────────────────────────────┤
│ 1. Soporte Técnico                                       │
│    GUID: a1b2c3d4-1234-5678-90ab-cdef12345678           │  ◄── COPIAR ESTE
│    Grupo de soporte técnico nivel 1                      │
├──────────────────────────────────────────────────────────┤
│ 2. Mesa de Servicio                                      │
│    GUID: b2c3d4e5-2345-6789-01bc-def123456789           │  ◄── COPIAR ESTE
│    Mesa de servicio general                              │
└──────────────────────────────────────────────────────────┘
```

---

### PASO 2: Actualizar JSON con GUIDs Reales

**ANTES (con marcadores de posición):**
```json
{
  "numero": "1.1",
  "nombre": "Incidente Técnico",
  "handler": "A001",
  "grupo_id": "{12345678-1234-1234-1234-123456789ABC}"  ❌ GUID de ejemplo
}
```

**DESPUÉS (con GUID real de cr321_grupos):**
```json
{
  "numero": "1.1",
  "nombre": "Incidente Técnico",
  "handler": "A001",
  "grupo_id": "{a1b2c3d4-1234-5678-90ab-cdef12345678}"  ✅ GUID real
}
```

---

### PASO 3: Insertar en Dataverse

```
Tabla: cr321_chatbots

┌─────────────────────────────────────────────────────────┐
│ REGISTRO: Chatbot1                                      │
├─────────────────────────────────────────────────────────┤
│ cr321_chatbotid: [GUID generado automáticamente]        │
│ cr321_name: "Chatbot1"                                  │
│ cr321_active: true                                      │
│ cr321_config: {                                         │
│   "menus": [                                            │
│     {                                                   │
│       "submenus": [                                     │
│         {                                               │
│           "numero": "1.1",                              │
│           "grupo_id": "{a1b2c3d4-1234...}"  ◄────────┐  │
│         }                                           │  │
│       ]                                             │  │
│     }                                               │  │
│   ]                                                 │  │
│ }                                                   │  │
└─────────────────────────────────────────────────────┼──┘
                                                      │
                                                      │
              ┌───────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────┐
│ Tabla: cr321_grupos                                     │
├─────────────────────────────────────────────────────────┤
│ cr321_grupoid: a1b2c3d4-1234-5678-90ab-cdef12345678 ◄── MATCH!
│ cr321_nombre: Soporte Técnico                           │
└─────────────────────────────────────────────────────────┘
```

---

### PASO 4: Validar Conexión

```bash
python validar_grupos_menu.py
```

**SALIDA EXITOSA:**
```
============================================================
VALIDACIÓN DE GRUPOS DEL MENÚ
============================================================

→ Consultando grupos válidos en cr321_grupos...
  ✓ 15 grupos disponibles

→ Validando grupos del menú...

✅ GRUPOS VÁLIDOS (7):
┌──────────────────────────────────────────────────────────┐
│ 1.1    Incidente Técnico                                 │
│        → Grupo: Soporte Técnico                          │  ◄── CONEXIÓN OK
├──────────────────────────────────────────────────────────┤
│ 1.2    Solicitud de Servicio                             │
│        → Grupo: Mesa de Servicio                         │  ◄── CONEXIÓN OK
└──────────────────────────────────────────────────────────┘

RESUMEN
✅ Válidos:   7
❌ Inválidos: 0  ◄────────────────── ¡IMPORTANTE!
⚪ Sin grupo: 1
```

**SALIDA CON ERRORES:**
```
❌ GRUPOS INVÁLIDOS (2):
┌──────────────────────────────────────────────────────────┐
│ 1.1    Incidente Técnico                                 │
│        ⚠️ GUID no existe: {12345678-1234-1234...}        │  ◄── ERROR
└──────────────────────────────────────────────────────────┘

💡 SOLUCIÓN:
   1. Ejecuta: python listar_grupos_dataverse.py
   2. Copia los GUIDs correctos de cr321_grupos
   3. Actualiza el JSON en cr321_config
```

---

## 📋 Estructura Completa

```
┌─────────────────────────────────────────────────────────────────┐
│                     DATAVERSE                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────┐         ┌──────────────────────┐     │
│  │ cr321_chatbots       │         │ cr321_grupos         │     │
│  ├──────────────────────┤         ├──────────────────────┤     │
│  │ cr321_chatbotid (PK) │         │ cr321_grupoid (PK)   │     │
│  │ cr321_name           │         │ cr321_nombre         │     │
│  │ cr321_active         │         │ cr321_descripcion    │     │
│  │ cr321_config  ───────┼────┐    │                      │     │
│  │   {                  │    │    │                      │     │
│  │     "menus": [       │    │    │                      │     │
│  │       {              │    │    │                      │     │
│  │         "submenus": [│    │    │                      │     │
│  │           {          │    │    │                      │     │
│  │      "grupo_id": "{..}"  │    │                      │     │
│  │           }          │    │    │                      │     │
│  │         ]            │    │    │                      │     │
│  │       }              │    │    │                      │     │
│  │     ]                │    │    │                      │     │
│  │   }                  │    │    │                      │     │
│  └──────────────────────┘    │    └──────────────────────┘     │
│                              │                                 │
│     CONTIENE JSON            │       TABLA DE GRUPOS            │
│     con GUIDs ───────────────┴──────► VALIDACIÓN               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

           ▲                              ▲
           │                              │
           │                              │
           │                              │
    ┌──────┴──────┐              ┌───────┴────────┐
    │             │              │                │
    │  Sistema    │              │  Validación    │
    │  Lee JSON   │              │  En Runtime    │
    │             │              │                │
    └─────────────┘              └────────────────┘
```

---

## ✅ Checklist de Validación

```
□ Ejecutar: python listar_grupos_dataverse.py
  └─► Copiar GUIDs reales

□ Actualizar ejemplo_json_dataverse.json
  └─► Reemplazar todos los grupo_id con GUIDs reales

□ Insertar JSON en Dataverse
  └─► python insertar_json_dataverse.py

□ Validar conexión
  └─► python validar_grupos_menu.py
  └─► Debe mostrar: "✅ Todos los grupos válidos"

□ Iniciar sistema
  └─► python sistema_menu_json.py
  └─► Debe cargar sin advertencias
```

---

## 🎯 Resumen Visual

```
JSON en cr321_config           cr321_grupos (Tabla)
     │                              │
     │  "grupo_id": "{a1b2c3...}"   │  cr321_grupoid: a1b2c3...
     │              │               │              ▲
     │              └───────────────┼──────────────┘
     │                              │
     │                    COINCIDENCIA EXACTA
     │                              │
     ▼                              ▼
   VÁLIDO ✅                    GRUPO REAL ✅
```

**Regla de Oro:**
> Cada `grupo_id` en el JSON **DEBE** tener su correspondiente `cr321_grupoid` en la tabla `cr321_grupos`

---

**¿Necesitas más ejemplos de cómo configurar estas conexiones? 🚀**
