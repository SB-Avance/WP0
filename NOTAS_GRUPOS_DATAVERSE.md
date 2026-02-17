# ⚙️ Conexión con Tabla cr321_grupos

## 📌 Concepto

El campo **`grupo_id`** en el JSON debe contener **GUIDs reales** de la tabla **`cr321_grupos`** de Dataverse. Esto garantiza:

- ✅ Integridad referencial
- ✅ Grupos válidos y activos
- ✅ Correcta asignación de tickets

---

## 🔗 Arquitectura de Conexión

```
┌──────────────────────────────────────────────────────────┐
│ cr321_chatbots (Tabla de Chatbots)                      │
├──────────────────────────────────────────────────────────┤
│ cr321_name: "Chatbot1"                                   │
│ cr321_config: {                                          │
│   "menus": [                                             │
│     {                                                    │
│       "submenus": [                                      │
│         {                                                │
│           "numero": "1.1",                               │
│           "nombre": "Incidente Técnico",                 │
│           "grupo_id": "{GUID}" ──────┐                   │
│         }                             │                   │
│       ]                               │                   │
│     }                                 │                   │
│   ]                                   │                   │
│ }                                     │                   │
└───────────────────────────────────────┼──────────────────┘
                                        │
                                        │ REFERENCIA
                                        │
                                        ▼
┌──────────────────────────────────────────────────────────┐
│ cr321_grupos (Tabla de Grupos)                          │
├──────────────────────────────────────────────────────────┤
│ cr321_grupoid: {GUID} ◄─────────────────┘                │
│ cr321_nombre: "Soporte Técnico"                          │
│ cr321_descripcion: "Grupo de soporte nivel 1"            │
└──────────────────────────────────────────────────────────┘
```

---

## 🔍 ¿Por Qué dentro del JSON y No como Lookup?

### Opción 1: Lookup de Dataverse (NO usado)
```
❌ Campo separado: cr321_grupoid (lookup a cr321_grupos)
❌ Un solo grupo por chatbot
❌ No flexible para múltiples menús
❌ Requiere cambios en schema para nuevo submenu
```

### Opción 2: GUID en JSON (✅ Usado - Arquitectura actual)
```
✅ Cada submenu tiene su propio grupo_id
✅ 100% flexible sin cambios en Dataverse
✅ Validación en runtime
✅ Sistema verifica integridad al cargar
```

**Razonamiento:**
- Un lookup de Dataverse solo funciona en **campos dedicados**, no dentro de texto JSON
- El JSON nos da **flexibilidad máxima**: cada submenu puede tener grupo diferente
- La **validación** se hace al cargar el sistema: verifica que cada GUID exista en `cr321_grupos`

---

## 🛠️ Workflow de Validación

### 1. Al Inicializar Sistema

```python
# sistema_menu_json.py
def _validar_grupos_menu(self):
    """
    Valida que todos los grupo_id del menú existan en cr321_grupos
    """
    
    # 1. Obtener grupos válidos de Dataverse
    response = requests.get(f"{DATAVERSE_URL}/cr321_grupos")
    grupos_validos = {g['cr321_grupoid']: g['cr321_nombre'] 
                      for g in response.json()["value"]}
    
    # 2. Validar cada grupo_id del menú
    for menu in self.config_menu.menus:
        for submenu in menu.get('submenus', []):
            grupo_id = submenu.get('grupo_id')
            
            if grupo_id and grupo_id not in grupos_validos:
                print(f"⚠️ GUID inválido: {grupo_id}")
```

**Salida esperada:**
```
→ Validando grupos del menú...
  ✓ Todos los grupos válidos (8 verificados)
```

**Si hay errores:**
```
→ Validando grupos del menú...
  ⚠️ 2 grupo(s) inválido(s) encontrado(s):
     - 1.1: Incidente Técnico → {12345678-XXXX-XXXX-XXXX-123456789ABC}
     - 1.2: Solicitud Básica → {ABCDEFGH-XXXX-XXXX-XXXX-123456789DEF}
  💡 Ejecuta: python listar_grupos_dataverse.py para ver grupos válidos
```

---

## 📋 Scripts Disponibles

### 1. Listar Grupos Válidos

```bash
python listar_grupos_dataverse.py
```

**Salida:**
```
┌──────────────────────────────────────────────────────────┐
│ GRUPOS DISPONIBLES (Tabla: cr321_grupos)                │
├──────────────────────────────────────────────────────────┤
│ 1. Soporte Técnico                                       │
│    GUID: 12345678-1234-1234-1234-123456789ABC           │
│    Grupo de soporte técnico nivel 1                      │
├──────────────────────────────────────────────────────────┤
│ 2. Mesa de Servicio                                      │
│    GUID: ABCDEFGH-1234-1234-1234-123456789DEF           │
│    Mesa de servicio general                              │
└──────────────────────────────────────────────────────────┘
```

**Uso:**
- Copiar GUIDs reales para actualizar JSON
- Verificar nombres de grupos
- Ver todos los grupos disponibles

---

### 2. Validar Configuración Actual

```bash
python validar_grupos_menu.py
```

**Qué valida:**
- ✅ Cada `grupo_id` existe en `cr321_grupos`
- ✅ GUIDs tienen formato correcto
- ✅ No hay referencias huérfanas

**Salida:**
```
============================================================
VALIDACIÓN DE GRUPOS DEL MENÚ
============================================================

→ Consultando grupos válidos en cr321_grupos...
  ✓ 15 grupos disponibles

→ Validando grupos del menú...

✅ GRUPOS VÁLIDOS (8):
┌──────────────────────────────────────────────────────────┐
│ 1.1    Incidente Técnico                                 │
│        → Grupo: Soporte Técnico                          │
├──────────────────────────────────────────────────────────┤
│ 1.2    Solicitud de Servicio                             │
│        → Grupo: Mesa de Servicio                         │
└──────────────────────────────────────────────────────────┘

⚪ SIN GRUPO ASIGNADO (1):
┌──────────────────────────────────────────────────────────┐
│ 3.1    Información General                               │
│        → No requiere grupo                               │
└──────────────────────────────────────────────────────────┘

RESUMEN
✅ Válidos:   8
❌ Inválidos: 0
⚪ Sin grupo: 1
📊 Total:     9

✅ Todos los grupos son válidos
```

---

## 🔧 Cómo Actualizar Grupos en el JSON

### Paso 1: Listar grupos disponibles

```bash
python listar_grupos_dataverse.py
```

Copiar el GUID del grupo deseado.

### Paso 2: Editar JSON en Dataverse

**Opción A: Desde Power Apps**
1. Ir a Power Apps → Dataverse → cr321_chatbots
2. Editar registro "Chatbot1"
3. Campo `cr321_config` → Buscar submenu
4. Actualizar `grupo_id`:

```json
{
  "numero": "1.1",
  "nombre": "Incidente Técnico",
  "grupo_id": "{12345678-1234-1234-1234-123456789ABC}"  ← GUID real
}
```

5. Guardar

**Opción B: Desde Python**

```python
import requests
import json

# 1. Obtener config actual
response = requests.get(
    f"{DATAVERSE_URL}/cr321_chatbots",
    headers=headers,
    params={
        "$filter": "cr321_name eq 'Chatbot1'",
        "$select": "cr321_chatbotid,cr321_config"
    }
)

data = response.json()["value"][0]
chatbot_id = data['cr321_chatbotid']
config = json.loads(data['cr321_config'])

# 2. Actualizar grupo_id
for menu in config['menus']:
    for submenu in menu['submenus']:
        if submenu['numero'] == '1.1':
            submenu['grupo_id'] = '{12345678-1234-1234-1234-123456789ABC}'

# 3. Guardar
requests.patch(
    f"{DATAVERSE_URL}/cr321_chatbots({chatbot_id})",
    headers=headers,
    json={"cr321_config": json.dumps(config, ensure_ascii=False, indent=2)}
)
```

### Paso 3: Validar cambios

```bash
python validar_grupos_menu.py
```

Verificar que no hay errores.

### Paso 4: Reiniciar sistema

```bash
python sistema_menu_json.py
```

El sistema carga la configuración actualizada.

---

## ⚠️ Errores Comunes

### Error: "Grupo inválido detectado"

**Causa:** El GUID en el JSON no existe en `cr321_grupos`

**Solución:**
```bash
# Ver grupos válidos
python listar_grupos_dataverse.py

# Validar qué está mal
python validar_grupos_menu.py

# Actualizar JSON con GUID correcto
```

---

### Error: "GUID con formato incorrecto"

**Formato correcto:**
```json
"grupo_id": "{12345678-1234-1234-1234-123456789ABC}"
```

**Formatos incorrectos:**
```json
❌ "grupo_id": "12345678-1234-1234-1234-123456789ABC"  // Sin llaves
❌ "grupo_id": "12345678"                               // Incompleto
❌ "grupo_id": null                                     // Null (usar "null" si no tiene)
❌ "grupo_id": ""                                       // Vacío
```

**Formato especial para "sin grupo":**
```json
"grupo_id": "null"  // O simplemente omitir el campo
```

---

## 📊 Ventajas de Esta Arquitectura

### ✅ Flexibilidad Total
- Cada submenu puede tener grupo diferente
- Agregar/quitar grupos sin cambiar schema
- Configurar grupos por chatbot independientemente

### ✅ Validación en Runtime
- Sistema verifica integridad al iniciar
- Reporta problemas claramente
- No permite grupos inexistentes

### ✅ Escalabilidad
- 500+ submenus con grupos diferentes
- Sin límite de combinaciones
- Menús jerárquicos con grupos variados

### ✅ Mantenimiento Simple
- Un solo archivo JSON por chatbot
- Scripts de validación automáticos
- Troubleshooting fácil

---

## 🎯 Resumen

1. **`grupo_id` en JSON** → Contiene GUID de `cr321_grupos`
2. **Validación automática** → Sistema verifica al iniciar
3. **Scripts disponibles:**
   - `listar_grupos_dataverse.py` → Ver grupos válidos
   - `validar_grupos_menu.py` → Verificar configuración
4. **Arquitectura flexible** → Cada submenu tiene su grupo
5. **Sin cambios en Dataverse** → Todo en JSON

---

**¿Dudas sobre cómo conectar grupos con el menú? 🚀**
