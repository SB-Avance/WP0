# MENÚ JERÁRQUICO - FLUJO VISUAL

## 🎯 Sistema Implementado

```
┌─────────────────────────────────────────────────────────────────┐
│                    MENÚ JERÁRQUICO WHATSAPP                     │
│                                                                 │
│  ✅ 3 Opciones Principales                                      │
│  ✅ Submenús por Opción                                         │
│  ✅ Grupos Diferentes por Subopción                             │
│  ✅ Navegación con 0 para Volver                                │
│  ✅ Cache Inteligente                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 ESTRUCTURA COMPLETA

```
                    ┌──────────────────┐
                    │   Usuario envía  │
                    │      "menu"      │
                    └────────┬─────────┘
                            │
                            ▼
            ┌───────────────────────────────┐
            │     MENÚ PRINCIPAL            │
            │                               │
            │  1. Solicitud Ticket          │
            │  2. Ventas                    │
            │  3. Solicitar Atención        │
            └───────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
   ┌────────┐   ┌────────┐   ┌────────────┐
   │ Usuario│   │ Usuario│   │  Usuario   │
   │ elige  │   │ elige  │   │  elige     │
   │   1    │   │   2    │   │    3       │
   └───┬────┘   └───┬────┘   └────┬───────┘
       │            │              │
       ▼            ▼              ▼
┌─────────────┐ ┌──────────┐ ┌────────────────┐
│  SUBMENÚ 1  │ │ SUBMENÚ 2│ │   SUBMENÚ 3    │
│             │ │          │ │                │
│ 1.1 Soporte │ │ 2.1 Coti │ │ 3.1 Agente     │
│ 1.2 Garantí │ │ 2.2 Catá │ │ 3.2 Agendar    │
│ 1.3 Consult │ │ 2.3 Segu │ │                │
│             │ │          │ │  0. Volver     │
│ 0. Volver   │ │ 0. Volve │ │                │
└─────────────┘ └──────────┘ └────────────────┘
       │            │              │
       ▼            ▼              ▼
  ┌─────────┐  ┌─────────┐  ┌──────────┐
  │ Usuario │  │ Usuario │  │ Usuario  │
  │ elige   │  │ elige   │  │ elige    │
  │ subop   │  │ subop   │  │ subop    │
  └────┬────┘  └────┬────┘  └─────┬────┘
       │            │              │
       ▼            ▼              ▼
┌──────────────────────────────────────┐
│   ASIGNACIÓN AUTOMÁTICA A GRUPO      │
│                                      │
│  1.1 → "Soporte Técnico"             │
│  1.2 → "Garantías"                   │
│  1.3 → "Consultas"                   │
│  2.1 → "Ventas - Cotización"         │
│  2.2 → "Ventas - Catálogo"           │
│  2.3 → "Ventas - Seguimiento"        │
│  3.1 → "Atención Inmediata"          │
│  3.2 → "Agendamiento"                │
└──────────────────────────────────────┘
```

---

## 💬 EJEMPLO DE CONVERSACIÓN COMPLETA

### Escenario 1: Solicitud de Soporte Técnico

```
┌─────────────────────────────────────────────────────────────┐
│ 👤 Usuario: "hola"                                          │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│ 🤖 Bot:                                                     │
│                                                             │
│ ¡Bienvenido! Seleccione una opción:                        │
│                                                             │
│ 1. Solicitud Ticket                                        │
│ 2. Ventas                                                  │
│ 3. Solicitar Atención                                      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 👤 Usuario: "1"                                             │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│ 🤖 Bot:                                                     │
│                                                             │
│ 📋 Solicitud Ticket                                        │
│                                                             │
│ Seleccione una opción:                                     │
│                                                             │
│ 1.1. Soporte Técnico                                       │
│ 1.2. Garantías                                             │
│ 1.3. Consultas Generales                                   │
│                                                             │
│ Escriba 0 para volver al menú principal                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 👤 Usuario: "1"                                             │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│ 🤖 Bot:                                                     │
│                                                             │
│ Ha seleccionado: Soporte Técnico                           │
│                                                             │
│ Un agente del área de Soporte Técnico se comunicará       │
│ con usted pronto.                                          │
│                                                             │
│ ✅ ASIGNADO: Grupo "Soporte Técnico"                       │
└─────────────────────────────────────────────────────────────┘
```

### Escenario 2: Solicitud de Cotización

```
┌─────────────────────────────────────────────────────────────┐
│ 👤 Usuario: "menu"                                          │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│ 🤖 Bot: [Muestra menú principal]                           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 👤 Usuario: "2"                                             │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│ 🤖 Bot:                                                     │
│                                                             │
│ 📋 Ventas                                                  │
│                                                             │
│ Seleccione una opción:                                     │
│                                                             │
│ 2.1. Cotización                                            │
│ 2.2. Catálogo                                              │
│ 2.3. Seguimiento                                           │
│                                                             │
│ Escriba 0 para volver al menú principal                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 👤 Usuario: "1"                                             │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│ 🤖 Bot:                                                     │
│                                                             │
│ Ha seleccionado: Cotización                                │
│                                                             │
│ Un agente del área de Ventas - Cotización se              │
│ comunicará con usted pronto.                               │
│                                                             │
│ ✅ ASIGNADO: Grupo "Ventas - Cotización"                   │
└─────────────────────────────────────────────────────────────┘
```

### Escenario 3: Volver al Menú Principal

```
┌─────────────────────────────────────────────────────────────┐
│ 👤 Usuario: "1" (en menú principal)                        │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│ 🤖 Bot: [Muestra submenú de Solicitud Ticket]             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 👤 Usuario: "0"                                             │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│ 🤖 Bot:                                                     │
│                                                             │
│ ¡Bienvenido! Seleccione una opción:                        │
│                                                             │
│ 1. Solicitud Ticket                                        │
│ 2. Ventas                                                  │
│ 3. Solicitar Atención                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🗄️ ESTRUCTURA EN DATAVERSE

### Tabla: cr321_chatbots

```
┌──────────────┬───────┬────────┬─────────────┬─────────────┬─────────────┬─────────────────────┬──────────────────┐
│ cr321_name   │ orden │ active │ elemento1   │ elemento2   │ elemento3   │ grupo1              │ grupo2           │
├──────────────┼───────┼────────┼─────────────┼─────────────┼─────────────┼─────────────────────┼──────────────────┤
│ Solicitud    │   1   │  ✅    │ Soporte     │ Garantías   │ Consultas   │ Soporte Técnico     │ Garantías        │
│ Ticket       │       │        │ Técnico     │             │ Generales   │                     │                  │
├──────────────┼───────┼────────┼─────────────┼─────────────┼─────────────┼─────────────────────┼──────────────────┤
│ Ventas       │   2   │  ✅    │ Cotización  │ Catálogo    │ Seguimiento │ Ventas - Cotización │ Ventas - Catálogo│
├──────────────┼───────┼────────┼─────────────┼─────────────┼─────────────┼─────────────────────┼──────────────────┤
│ Solicitar    │   3   │  ✅    │ Agente      │ Agendar     │             │ Atención Inmediata  │ Agendamiento     │
│ Atención     │       │        │ Disponible  │ Cita        │             │                     │                  │
└──────────────┴───────┴────────┴─────────────┴─────────────┴─────────────┴─────────────────────┴──────────────────┘
```

### Tabla: cr321_grups (Tipo A = 462410000)

```
┌─────────────────────────┬─────────┬──────────────────────────────┐
│ cr321_nombre            │ cr321_t │ cr321_descripcion            │
│                         │ ipo     │                              │
├─────────────────────────┼─────────┼──────────────────────────────┤
│ Soporte Técnico         │ 462410  │ Soporte técnico y ayuda      │
├─────────────────────────┼─────────┼──────────────────────────────┤
│ Garantías               │ 462410  │ Gestión de garantías         │
├─────────────────────────┼─────────┼──────────────────────────────┤
│ Consultas               │ 462410  │ Consultas generales          │
├─────────────────────────┼─────────┼──────────────────────────────┤
│ Ventas - Cotización     │ 462410  │ Solicitudes de cotización    │
├─────────────────────────┼─────────┼──────────────────────────────┤
│ Ventas - Catálogo       │ 462410  │ Consultas de catálogo        │
├─────────────────────────┼─────────┼──────────────────────────────┤
│ Ventas - Seguimiento    │ 462410  │ Seguimiento de ventas        │
├─────────────────────────┼─────────┼──────────────────────────────┤
│ Atención Inmediata      │ 462410  │ Atención rápida              │
├─────────────────────────┼─────────┼──────────────────────────────┤
│ Agendamiento            │ 462410  │ Agendar citas                │
└─────────────────────────┴─────────┴──────────────────────────────┘
```

---

## 🔧 ARCHIVOS DEL SISTEMA

```
c:\VS\BIN\
│
├── 📄 sistema_menu_jerarquico.py        ← Sistema principal
├── 📄 configurar_menu_jerarquico.py     ← Configuración automática
├── 📄 probar_menu_jerarquico.py         ← Pruebas completas
├── 📄 GUIA_MENU_JERARQUICO.md           ← Guía detallada
└── 📄 FLUJO_VISUAL_MENU.md              ← Este archivo
```

---

## ⚡ INICIO RÁPIDO

### 1. Configurar Dataverse
```powershell
python configurar_menu_jerarquico.py
```

### 2. Probar Sistema
```powershell
python probar_menu_jerarquico.py
```

### 3. Ver Demo
```powershell
python sistema_menu_jerarquico.py
```

### 4. Integrar con Flask
```python
from sistema_menu_jerarquico import crear_sistema_menu_jerarquico

sistema = crear_sistema_menu_jerarquico(DATAVERSE_URL, get_token)
respuesta = sistema.procesar_mensaje(mensaje, telefono)

if respuesta['grupo']:
    asignar_a_grupo(telefono, respuesta['grupo'])
```

---

## 🎯 CASOS DE USO

### ✅ Usuario Nueva Cotización
```
"menu" → "2" → "1" → Grupo "Ventas - Cotización"
```

### ✅ Usuario Problema Técnico
```
"hola" → "1" → "1" → Grupo "Soporte Técnico"
```

### ✅ Usuario Quiere Agente
```
"menu" → "3" → "1" → Grupo "Atención Inmediata"
```

### ✅ Usuario Se Equivoca
```
"menu" → "1" → "0" → "2" → "3" → Grupo "Ventas - Seguimiento"
```

---

## 📊 VENTAJAS DEL SISTEMA

| Característica | Beneficio |
|---------------|-----------|
| **Jerarquía** | Organización clara y profesional |
| **Grupos Diferentes** | Cada área recibe sus chats específicos |
| **Navegación con 0** | Usuario puede corregir errores |
| **Cache** | Respuesta rápida (no consulta Dataverse cada vez) |
| **Estado por Usuario** | Múltiples usuarios simultáneos sin conflictos |
| **Logs Detallados** | Fácil debugging y monitoreo |
| **Fallback Hardcoded** | Funciona aunque Dataverse falle |
| **Escalable** | Fácil agregar más opciones |

---

## 🚀 ¡LISTO PARA USAR!

El sistema está **completamente funcional** con:
- ✅ 3 opciones principales (1, 2, 3)
- ✅ Submenús configurables
- ✅ 8 grupos diferentes
- ✅ Navegación intuitiva
- ✅ Asignación automática
- ✅ Cache inteligente
- ✅ Logs detallados

**¡Empieza a probarlo ahora!** 🎉
