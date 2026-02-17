# 🔄 FLEXIBILIDAD DEL MENÚ - Aumentar o Disminuir Opciones

## ✅ El Sistema ES Completamente Flexible

La arquitectura con JSON en `cr321_config` permite:
- ✅ **Agregar** opciones sin límite
- ✅ **Eliminar** opciones sin afectar otras
- ✅ **Desactivar** opciones temporalmente
- ✅ **Reorganizar** opciones fácilmente
- ✅ **Sin cambios en Dataverse** (no migrations)

---

## 📊 Comparación con Sistema Rígido

### ❌ Sistema Rígido (Campos Fijos)
```sql
-- Dataverse con campos fijos:
cr321_elemento1, cr321_handler1, cr321_grupo1  -- Opción 1.1
cr321_elemento2, cr321_handler2, cr321_grupo2  -- Opción 1.2
cr321_elemento3, cr321_handler3, cr321_grupo3  -- Opción 1.3
cr321_elemento4, cr321_handler4, cr321_grupo4  -- Opción 1.4
cr321_elemento5, cr321_handler5, cr321_grupo5  -- Opción 1.5

⚠️ Problema: Solo 5 opciones máximo
⚠️ Si necesitas 6ta opción → Crear cr321_elemento6 (migration)
⚠️ Si quieres 20 opciones → No caben en campos fijos
```

### ✅ Sistema JSON (Dinámico)
```json
{
  "menus": [
    {
      "numero": "1",
      "nombre": "Solicitud Ticket",
      "submenus": [
        { "numero": "1.1", "nombre": "Opción 1" },
        { "numero": "1.2", "nombre": "Opción 2" },
        { "numero": "1.3", "nombre": "Opción 3" }
        // ✅ Puedes agregar 100 opciones si quieres
      ]
    }
  ]
}

✅ Sin límites: Agrega cuantas opciones necesites
✅ Sin migrations: Solo editas el JSON
✅ Inmediato: Cambios se aplican al guardar
```

---

## 🎯 Casos de Uso Reales

### Caso 1: Agregar Nueva Opción al Menú

**Antes (3 opciones):**
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
          "grupo_id": "{GUID-SOPORTE}"
        },
        {
          "numero": "1.2",
          "nombre": "Solicitud de Servicio",
          "handler": "B001",
          "grupo_id": "{GUID-MESA}"
        },
        {
          "numero": "1.3",
          "nombre": "Cambio RFC",
          "handler": "C001",
          "grupo_id": "{GUID-CAB}"
        }
      ]
    }
  ]
}
```

**Después (4 opciones - agregamos nueva):**
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
          "grupo_id": "{GUID-SOPORTE}"
        },
        {
          "numero": "1.2",
          "nombre": "Solicitud de Servicio",
          "handler": "B001",
          "grupo_id": "{GUID-MESA}"
        },
        {
          "numero": "1.3",
          "nombre": "Cambio RFC",
          "handler": "C001",
          "grupo_id": "{GUID-CAB}"
        },
        {
          "numero": "1.4",
          "nombre": "Consulta de Estado",  ← NUEVA OPCIÓN
          "handler": "I001",
          "grupo_id": "{GUID-CONSULTAS}",
          "activo": true,
          "tags": ["consulta", "estado"]
        }
      ]
    }
  ]
}
```

**Pasos para aplicar:**
1. Editar JSON en Dataverse (campo `cr321_config`)
2. Guardar
3. ✅ Listo - Sistema carga automáticamente 4 opciones

---

### Caso 2: Eliminar Opción del Menú

**Opción A: Borrar Completamente**
```json
// ANTES: 4 opciones
"submenus": [
  { "numero": "1.1", "nombre": "Incidente" },
  { "numero": "1.2", "nombre": "Solicitud" },
  { "numero": "1.3", "nombre": "Cambio RFC" },    ← Eliminar esta
  { "numero": "1.4", "nombre": "Consulta" }
]

// DESPUÉS: 3 opciones
"submenus": [
  { "numero": "1.1", "nombre": "Incidente" },
  { "numero": "1.2", "nombre": "Solicitud" },
  { "numero": "1.3", "nombre": "Consulta" }  ← Renumerada
]
```

**Opción B: Desactivar Temporalmente (Mejor)**
```json
"submenus": [
  { "numero": "1.1", "nombre": "Incidente", "activo": true },
  { "numero": "1.2", "nombre": "Solicitud", "activo": true },
  { 
    "numero": "1.3", 
    "nombre": "Cambio RFC", 
    "activo": false  ← Solo desactivar
  },
  { "numero": "1.4", "nombre": "Consulta", "activo": true }
]
```

**Ventajas de desactivar vs eliminar:**
- ✅ Puedes reactivarla después
- ✅ Conservas la configuración (handler, grupo, etc.)
- ✅ Historial de qué opciones existieron

---

### Caso 3: Menú Crece de 8 a 25 Opciones

**Escenario:** Tu empresa crece y necesitas más opciones

```json
// INICIO: 8 opciones (3 menús)
{
  "menus": [
    { "numero": "1", "submenus": [ 3 opciones ] },
    { "numero": "2", "submenus": [ 3 opciones ] },
    { "numero": "3", "submenus": [ 2 opciones ] }
  ]
}

// 6 MESES DESPUÉS: 25 opciones (5 menús)
{
  "menus": [
    { "numero": "1", "submenus": [ 5 opciones ] },  ← Creció
    { "numero": "2", "submenus": [ 4 opciones ] },  ← Creció
    { "numero": "3", "submenus": [ 3 opciones ] },  ← Creció
    { "numero": "4", "submenus": [ 6 opciones ] },  ← NUEVO MENÚ
    { "numero": "5", "submenus": [ 7 opciones ] }   ← NUEVO MENÚ
  ]
}

✅ Sin cambios en Dataverse
✅ Sin código nuevo
✅ Solo editar JSON
```

---

### Caso 4: Reorganizar Opciones

**Mover opción de un menú a otro:**

```json
// ANTES:
"menus": [
  {
    "numero": "1",
    "nombre": "Solicitud Ticket",
    "submenus": [
      { "numero": "1.1", "nombre": "Incidente", "handler": "A001" },
      { "numero": "1.2", "nombre": "Cotización", "handler": "D001" }
    ]
  }
]

// DESPUÉS (Cotización movida a Ventas):
"menus": [
  {
    "numero": "1",
    "nombre": "Solicitud Ticket",
    "submenus": [
      { "numero": "1.1", "nombre": "Incidente", "handler": "A001" }
    ]
  },
  {
    "numero": "2",
    "nombre": "Ventas",
    "submenus": [
      { "numero": "2.1", "nombre": "Cotización", "handler": "D001" }
    ]
  }
]

✅ Mismo handler "D001" funciona en cualquier menú
✅ Sin dependencias rígidas
```

---

## 🛠️ Script para Actualizar Menú Dinámicamente

```python
"""
Script para agregar/eliminar opciones del menú sin editar JSON manualmente
"""

import requests
import json

def obtener_config_actual(chatbot_name: str) -> dict:
    """Obtiene el JSON actual del chatbot"""
    response = requests.get(
        f"{DATAVERSE_URL}/cr321_chatbots",
        headers=headers,
        params={
            "$filter": f"cr321_name eq '{chatbot_name}'",
            "$select": "cr321_chatbotid,cr321_config"
        }
    )
    
    data = response.json()["value"][0]
    return {
        'guid': data['cr321_chatbotid'],
        'config': json.loads(data['cr321_config'])
    }


def agregar_submenu(config: dict, numero_menu: str, nueva_opcion: dict):
    """Agrega una nueva opción a un menú existente"""
    
    for menu in config['menus']:
        if menu['numero'] == numero_menu:
            menu['submenus'].append(nueva_opcion)
            print(f"✓ Nueva opción agregada al menú {numero_menu}")
            return config
    
    raise Exception(f"Menú {numero_menu} no encontrado")


def eliminar_submenu(config: dict, numero_submenu: str):
    """Elimina una opción específica"""
    
    for menu in config['menus']:
        menu['submenus'] = [
            sub for sub in menu['submenus'] 
            if sub['numero'] != numero_submenu
        ]
    
    print(f"✓ Opción {numero_submenu} eliminada")
    return config


def desactivar_submenu(config: dict, numero_submenu: str):
    """Desactiva una opción sin eliminarla"""
    
    for menu in config['menus']:
        for submenu in menu['submenus']:
            if submenu['numero'] == numero_submenu:
                submenu['activo'] = False
                print(f"✓ Opción {numero_submenu} desactivada")
                return config
    
    raise Exception(f"Submenú {numero_submenu} no encontrado")


def actualizar_config(guid: str, config: dict):
    """Guarda la configuración actualizada en Dataverse"""
    
    config_json = json.dumps(config, ensure_ascii=False, indent=2)
    
    response = requests.patch(
        f"{DATAVERSE_URL}/cr321_chatbots({guid})",
        headers=headers,
        json={"cr321_config": config_json}
    )
    
    if response.status_code == 204:
        print("✓ Configuración actualizada en Dataverse")
    else:
        raise Exception(f"Error actualizando: {response.text}")


# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

# 1. AGREGAR NUEVA OPCIÓN
chatbot = obtener_config_actual("Chatbot1")

nueva_opcion = {
    "numero": "1.4",
    "nombre": "Consulta de Estado",
    "descripcion": "Consultar estado de ticket",
    "handler": "I001",
    "grupo_id": "{GUID-CONSULTAS}",
    "activo": True,
    "tags": ["consulta", "estado"]
}

config_actualizado = agregar_submenu(chatbot['config'], "1", nueva_opcion)
actualizar_config(chatbot['guid'], config_actualizado)


# 2. DESACTIVAR OPCIÓN (sin eliminar)
chatbot = obtener_config_actual("Chatbot1")
config_actualizado = desactivar_submenu(chatbot['config'], "1.3")
actualizar_config(chatbot['guid'], config_actualizado)


# 3. ELIMINAR OPCIÓN PERMANENTEMENTE
chatbot = obtener_config_actual("Chatbot1")
config_actualizado = eliminar_submenu(chatbot['config'], "1.3")
actualizar_config(chatbot['guid'], config_actualizado)
```

---

## 📊 Límites y Capacidad

### Límites Técnicos

```
Campo cr321_config:
├─ Tipo: Text (Long Text)
├─ Tamaño máximo: ~100,000 caracteres
└─ Capacidad estimada:
    ├─ ~500-1000 opciones de menú (realista)
    ├─ ~50-100 menús principales
    └─ Más que suficiente para cualquier chatbot

Límites prácticos (experiencia de usuario):
├─ Recomendado: 3-5 menús principales
├─ Máximo recomendado: 5-10 opciones por menú
└─ Total recomendado: 15-50 opciones totales
```

### ¿Cuánto JSON cabe?

**Ejemplo real:**
```json
// 1 opción simple = ~200 caracteres
{
  "numero": "1.1",
  "nombre": "Incidente Técnico",
  "descripcion": "Reportar problemas técnicos",
  "handler": "A001",
  "grupo_id": "{GUID}",
  "activo": true,
  "tags": ["soporte"]
}

// 100,000 caracteres ÷ 200 = ~500 opciones posibles
// En la práctica: 200-300 opciones con metadata completa
```

---

## ✅ Ventajas de la Flexibilidad

### 1. Evolución Gradual
```
Mes 1: 8 opciones   → Lanzamiento MVP
Mes 3: 12 opciones  → Agregar Ventas
Mes 6: 20 opciones  → Agregar Consultas
Mes 12: 35 opciones → Empresa creció

✅ Todo sin cambios en código o base de datos
```

### 2. Testing de Nuevas Opciones
```json
// Agregar opción en testing
{
  "numero": "1.5",
  "nombre": "Nueva Función BETA",
  "handler": "Z001",
  "activo": true,
  "tags": ["beta", "experimental"]
}

// Si no funciona bien → Desactivar
"activo": false

// Si funciona → Dejar activo
"activo": true

// No hay riesgo, no afecta otras opciones
```

### 3. Menús Especializados por Cliente
```
Chatbot1 (Cliente A): 8 opciones
Chatbot2 (Cliente B): 15 opciones  ← Más opciones
Chatbot3 (Testing):   3 opciones   ← Solo lo básico

✅ Cada chatbot tiene su propio JSON
✅ Flexibilidad total por cliente
```

---

## 🎯 Mejores Prácticas

### ✅ Recomendaciones

1. **Desactivar mejor que eliminar**
   ```json
   "activo": false  // Mejor que borrar el objeto
   ```

2. **Usar números secuenciales con huecos**
   ```json
   "1.1", "1.2", "1.5", "1.7"  // Dejar espacio para futuro
   ```

3. **Tags para organizar opciones**
   ```json
   "tags": ["urgente", "tecnico", "beta"]  // Facilita búsquedas
   ```

4. **Versionar el JSON**
   ```json
   "version": "2.1.0"  // Control de versiones
   ```

5. **Comentarios en descripción**
   ```json
   "descripcion": "Opción agregada 2026-02-11 - Temporal para campaña"
   ```

### ⚠️ Evitar

1. ❌ Borrar opciones sin backup
2. ❌ Agregar 50 opciones de golpe (confuso para usuario)
3. ❌ Cambiar números de opciones existentes
4. ❌ Olvidar actualizar handlers cuando agregas opciones

---

## 🚀 Resumen

```
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│  ✅ EL MENÚ ES COMPLETAMENTE FLEXIBLE                          │
│                                                                │
│  Puedes:                                                       │
│  ├─ ✅ Agregar opciones sin límite                             │
│  ├─ ✅ Eliminar opciones fácilmente                            │
│  ├─ ✅ Desactivar temporalmente                                │
│  ├─ ✅ Reorganizar estructura                                  │
│  ├─ ✅ Crear menús nuevos                                      │
│  └─ ✅ Todo sin cambios en Dataverse                           │
│                                                                │
│  Límites:                                                      │
│  ├─ Técnico: ~500-1000 opciones posibles                      │
│  └─ Práctico: 15-50 opciones recomendadas (UX)                │
│                                                                │
│  Proceso:                                                      │
│  1. Editar JSON en cr321_config                                │
│  2. Guardar en Dataverse                                       │
│  3. ✅ Sistema carga automáticamente                           │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## 💡 Ejemplo Completo: De 8 a 20 Opciones en 6 Meses

### Mes 0 (Lanzamiento):
```
1. Solicitud Ticket (3 opciones)
2. Ventas (2 opciones)
3. Atención (2 opciones)
Total: 7 opciones
```

### Mes 3 (Crecimiento):
```
1. Solicitud Ticket (5 opciones)  ← +2 opciones
2. Ventas (4 opciones)            ← +2 opciones
3. Atención (3 opciones)          ← +1 opción
Total: 12 opciones
```

### Mes 6 (Expansión):
```
1. Solicitud Ticket (5 opciones)
2. Ventas (4 opciones)
3. Atención (3 opciones)
4. Consultas (4 opciones)         ← NUEVO MENÚ
5. Recursos Humanos (4 opciones)  ← NUEVO MENÚ
Total: 20 opciones
```

**Todo con el mismo sistema, sin cambios en código.** 🎉
