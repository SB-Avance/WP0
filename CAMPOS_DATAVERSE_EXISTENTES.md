# ✅ USO DE CAMPOS EXISTENTES EN DATAVERSE

## 🎯 Campos que YA EXISTEN (no crear nuevos)

En la tabla **`cr321_chatbots`** ya tienes estos campos disponibles:

```sql
✅ cr321_config    (Texto)  - Para código del handler
✅ cr321_grupoid   (Lookup) - Para GUID del grupo asignado
✅ cr321_elemento1 (Texto)  - Nombre visible en menú
```

## 📋 Cómo Usarlos

### 1️⃣ Campo `cr321_config` - Código del Handler

**Propósito:** Almacenar el código único del handler (A001, B001, C001, etc.)

**Antes pensábamos crear:**
```
❌ cr321_handler1: "A001"
❌ cr321_handler2: "B001"
❌ cr321_handler3: "C001"
...
```

**Ahora usamos lo que YA existe:**
```
✅ cr321_config: "A001"
```

**Ejemplo completo:**
```sql
-- Opción del menú: 1.1 Incidente Técnico
cr321_elemento1: "Incidente Técnico"      -- Texto visible
cr321_config:    "A001"                   -- Código del handler
cr321_grupoid:   {GUID-SOPORTE-TI}        -- Grupo destino
```

---

### 2️⃣ Campo `cr321_grupoid` - Grupo Asignado

**Propósito:** Almacenar el GUID del grupo al que se asigna la conversación

**Valor:**
- GUID válido: `{12345678-1234-1234-1234-123456789ABC}`
- `null`: Sin grupo asignado

**Ejemplo:**
```sql
cr321_grupoid: {A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
```

---

## 🔄 Flujo Completo

```
┌────────────────────────────────────────────────────────────────┐
│ PASO A PASO: Cómo se usan los campos                          │
└────────────────────────────────────────────────────────────────┘

1. Usuario selecciona opción "1.1 Incidente Técnico"

2. Sistema consulta Dataverse:
   SELECT * FROM cr321_chatbots WHERE cr321_elemento1 = 'Incidente Técnico'

   Resultado:
   ├─ cr321_elemento1: "Incidente Técnico"
   ├─ cr321_config:    "A001"              ← Código handler
   └─ cr321_grupoid:   {GUID-SOPORTE}      ← Grupo destino

3. Sistema abre: handlers/config_handlers.json

   Busca código: "A001"

   Encuentra:
   {
     "A001": {
       "codigo": "A001",
       "archivo": "handler_A001.py",
       "clase": "HandlerA001",
       "grupo_override": null,
       "usa_grupo_de_dataverse": true
     }
   }

4. Sistema carga: handlers/handler_A001.py

5. Determina grupo destino:

   ┌─ config["grupo_override"] == null? ✅
   ├─ config["usa_grupo_de_dataverse"] == true? ✅
   └─ USAR: cr321_grupoid de Dataverse = {GUID-SOPORTE}

   O si fuera override:
   ┌─ config["grupo_override"] == {GUID-SUPERVISORES}? ✅
   ├─ config["usa_grupo_de_dataverse"] == false? ✅
   └─ USAR: {GUID-SUPERVISORES} (ignora cr321_grupoid)

6. Ejecuta handler:
   handler_A001.ejecutar(
     from_user="573001234567",
     grupo_id="{GUID-SOPORTE}"  ← De Dataverse o del JSON
   )
```

---

## 📊 Ejemplos Prácticos

### Ejemplo 1: Handler Normal (usa grupo de Dataverse)

**Dataverse:**
```sql
cr321_elemento1: "Incidente Técnico"
cr321_config:    "A001"
cr321_grupoid:   {GUID-SOPORTE-TI}
```

**JSON (config_handlers.json):**
```json
{
  "A001": {
    "archivo": "handler_A001.py",
    "grupo_override": null,
    "usa_grupo_de_dataverse": true
  }
}
```

**Resultado:**
```
✅ Carga: handler_A001.py
✅ Asigna a: {GUID-SOPORTE-TI} (de cr321_grupoid)
```

---

### Ejemplo 2: Handler con Override (ignora Dataverse)

**Dataverse:**
```sql
cr321_elemento1: "Atención Urgente"
cr321_config:    "H001"
cr321_grupoid:   {GUID-ATENCION-NORMAL}  ← Será ignorado
```

**JSON (config_handlers.json):**
```json
{
  "H001": {
    "archivo": "handler_H001.py",
    "grupo_override": "{GUID-SUPERVISORES}",
    "usa_grupo_de_dataverse": false
  }
}
```

**Resultado:**
```
✅ Carga: handler_H001.py
✅ Asigna a: {GUID-SUPERVISORES} (del JSON, ignora cr321_grupoid)
💡 Útil para urgencias que SIEMPRE van a Supervisores
```

---

### Ejemplo 3: Handler sin Grupo (solo responde)

**Dataverse:**
```sql
cr321_elemento1: "Ver Catálogo PDF"
cr321_config:    "E001"
cr321_grupoid:   null
```

**JSON (config_handlers.json):**
```json
{
  "E001": {
    "archivo": "handler_E001.py",
    "grupo_override": null,
    "usa_grupo_de_dataverse": false
  }
}
```

**Resultado:**
```
✅ Carga: handler_E001.py
❌ NO asigna a ningún grupo
💡 Solo envía PDF y termina
```

---

## 🎯 Ventajas de Usar Campos Existentes

```
✅ NO necesitas crear campos nuevos (cr321_handler1-5)
✅ NO necesitas modificar schema de Dataverse
✅ Aprovechas infraestructura existente
✅ cr321_config es flexible (puede almacenar cualquier código)
✅ cr321_grupoid ya es tipo Lookup (perfecto para grupos)
✅ Menos cambios = menos riesgo
✅ Implementación más rápida
```

---

## 🔑 Mapeo de Conceptos

| Concepto Anterior | Campo Nuevo (Dataverse) | ¿Existe? |
|-------------------|-------------------------|----------|
| Código handler    | `cr321_config`          | ✅ SÍ    |
| Grupo asignado    | `cr321_grupoid`         | ✅ SÍ    |
| Nombre visible    | `cr321_elemento1`       | ✅ SÍ    |

---

## 💡 Código de Ejemplo (Python)

### Consultar Dataverse y obtener campos:

```python
def obtener_handler_para_opcion(subopcion: str) -> dict:
    """
    Consulta Dataverse para obtener configuración de la opción.

    Returns:
        {
            'codigo_handler': 'A001',
            'grupo_id': '{GUID-SOPORTE}',
            'nombre': 'Incidente Técnico'
        }
    """

    # Consulta según subopción (1.1, 1.2, etc.)
    # Asumiendo que subopción 1.1 corresponde a cr321_orden = 11
    orden = int(subopcion.replace('.', ''))

    response = requests.get(
        f"{DATAVERSE_URL}/cr321_chatbots",
        headers=headers,
        params={
            "$filter": f"cr321_orden eq {orden}",
            "$select": "cr321_elemento1,cr321_config,cr321_grupoid"
        }
    )

    if response.status_code == 200:
        data = response.json()["value"][0]

        return {
            'codigo_handler': data.get('cr321_config'),        # ← "A001"
            'grupo_id': data.get('_cr321_grupoid_value'),      # ← GUID
            'nombre': data.get('cr321_elemento1')              # ← "Incidente Técnico"
        }

    return None


def determinar_grupo_final(codigo_handler: str, grupo_dataverse: str) -> str:
    """
    Determina qué grupo usar según configuración del handler.

    Args:
        codigo_handler: Código del handler (ej: "A001")
        grupo_dataverse: GUID del grupo en Dataverse (cr321_grupoid)

    Returns:
        GUID del grupo final a usar
    """

    # 1. Obtener config del handler desde JSON
    config = config_handlers[codigo_handler]

    # 2. Verificar si hay override
    if config.get('grupo_override'):
        # Tiene override → usar ese grupo (ignorar Dataverse)
        return config['grupo_override']

    # 3. Verificar si usa grupo de Dataverse
    if config.get('usa_grupo_de_dataverse', True):
        # Usa grupo de Dataverse
        return grupo_dataverse

    # 4. No usa grupo
    return None


# Ejemplo de uso:
config_opcion = obtener_handler_para_opcion("1.1")
# → {'codigo_handler': 'A001', 'grupo_id': '{GUID-SOPORTE}', 'nombre': 'Incidente Técnico'}

grupo_final = determinar_grupo_final(
    config_opcion['codigo_handler'],
    config_opcion['grupo_id']
)
# → '{GUID-SOPORTE}' (de Dataverse)
# O → '{GUID-SUPERVISORES}' (si hay override en JSON)
# O → None (si no usa grupo)
```

---

## 📝 Resumen

```
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│  CAMPOS DATAVERSE (YA EXISTEN):                                │
│  ├─ cr321_config    → Código handler (A001, B001, etc.)        │
│  ├─ cr321_grupoid   → GUID grupo asignado                      │
│  └─ cr321_elemento1 → Nombre visible en menú                   │
│                                                                │
│  ARCHIVO JSON (config_handlers.json):                          │
│  ├─ "codigo": "A001"                                           │
│  ├─ "archivo": "handler_A001.py"                               │
│  ├─ "clase": "HandlerA001"                                     │
│  ├─ "grupo_override": null o {GUID}                            │
│  └─ "usa_grupo_de_dataverse": true/false                       │
│                                                                │
│  LÓGICA:                                                       │
│  1. Leer cr321_config de Dataverse → "A001"                    │
│  2. Buscar "A001" en JSON → obtener archivo                    │
│  3. Cargar handler_A001.py                                     │
│  4. Determinar grupo:                                          │
│     ├─ Si grupo_override: usar ese                             │
│     ├─ Si usa_grupo_de_dataverse: usar cr321_grupoid           │
│     └─ Si ninguno: no asignar grupo                            │
│                                                                │
│  ✅ Simple, flexible, usa infraestructura existente            │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```
