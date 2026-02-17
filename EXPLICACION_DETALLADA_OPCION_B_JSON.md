# 🔤 CÓDIGOS CON UNA LETRA + EXPLICACIÓN DETALLADA OPCIÓN B (JSON)

## 🎯 PARTE 1: Códigos Relacionados con Categoría del Menú

### Propuesta de Códigos (Letra según Categoría):

La letra indica la **categoría del menú** a la que pertenece:

```
S001 = Solicitud - Incidente Técnico
S002 = Solicitud - Servicio Estándar
S003 = Solicitud - Cambio RFC

V001 = Ventas - Cotización
V002 = Ventas - Catálogo PDF
V003 = Ventas - Seguimiento Pedido

A001 = Atención - Asignación Directa
A002 = Atención - Urgencia

X999 = Sistema - Default
```

### ✅ Ventajas:

```
1. INTUITIVO
   ✓ S = Solicitud (sabes de qué categoría es)
   ✓ V = Ventas
   ✓ A = Atención
   ✓ Fácil identificar handlers por categoría

2. ORGANIZADO
   ✓ Todos los handlers de Solicitud: S001-S999
   ✓ Todos los handlers de Ventas: V001-V999
   ✓ Agrupación lógica

3. BÚSQUEDA FÁCIL
   ✓ "Dame todos los handlers de Ventas" → Buscar V*
   ✓ Reportes por categoría simples

4. MÁS CORTO
   ✓ S001 (4 chars) vs SOL001 (6 chars)
```

### ⚠️ Desventajas:

```
1. DEPENDENCIA PARCIAL DEL MENÚ
   ⚠️ Si cambias el nombre de categoría "Solicitud" → "Tickets"
      Los códigos S001 quedan con letra que ya no coincide
   ⚠️ Letra sugiere la categoría actual

2. REORGANIZACIÓN COMPLEJA
   ⚠️ Si mueves "Incidente Técnico" de "Solicitud" a otra categoría
      Idealmente deberías cambiar S001 → otra letra
      Pero cambiar código rompe referencias (si no usas catálogo)

3. ESPACIO LIMITADO POR LETRA
   ⚠️ Solo 999 handlers por categoría (S001-S999)
   ⚠️ Si tienes más de 26 categorías, no hay letras
```

### 📊 Tabla Completa (PARTE 1):

```
┌──────────┬─────────────────────────────────────┬──────────────────────────────┐
│ Código   │ Nombre Menú                         │ Archivo Handler              │
├──────────┼─────────────────────────────────────┼──────────────────────────────┤
│ S001     │ Incidente Técnico                   │ handler_incidente_tecnico.py │
│ S002     │ Solicitud de Servicio               │ handler_solicitud_servicio.py│
│ S003     │ Cambio Programado (RFC)             │ handler_cambio_rfc.py        │
├──────────┼─────────────────────────────────────┼──────────────────────────────┤
│ V001     │ Solicitar Cotización                │ handler_cotizacion.py        │
│ V002     │ Ver Catálogo de Productos           │ handler_catalogo_pdf.py      │
│ V003     │ Seguimiento de Pedido               │ handler_seguimiento_pedido.py│
├──────────┼─────────────────────────────────────┼──────────────────────────────┤
│ A001     │ Asignación Directa                  │ handler_asignar_directo.py   │
│ A002     │ Atención Urgente                    │ handler_urgencia_prioridad.py│
├──────────┼─────────────────────────────────────┼──────────────────────────────┤
│ X999     │ Handler por Defecto                 │ handler_default.py           │
└──────────┴─────────────────────────────────────┴──────────────────────────────┘
```

---

## 🎯 PARTE 2: Códigos INDEPENDIENTES del Menú

### Propuesta de Códigos (Letras Secuenciales):

Los códigos son **completamente independientes** del nombre del menú:

```
A001 = Handler para captura de incidentes técnicos
B001 = Handler para solicitudes de servicio básicas
C001 = Handler para proceso RFC con aprobación
D001 = Handler para cotizaciones con cálculo automático
E001 = Handler para envío de catálogo PDF
F001 = Handler para consulta de pedidos en ERP
G001 = Handler para asignación directa sin preguntas
H001 = Handler para urgencias con notificación SMS
I001 = Handler para consulta de inventario
J001 = Handler para registro de quejas
...
Z001 = Handler número 26
AA01 = Handler número 27 (si necesitas más de 26)
AB01 = Handler número 28
...
ZZ01 = Handler número 702
```

### ✅ Ventajas:

```
1. INDEPENDENCIA TOTAL
   ✅ Cambias nombre de menú → Código NO cambia
   ✅ Mueves opción de categoría → Código NO cambia
   ✅ Renombras categoría → Código NO cambia
   ✅ CERO acoplamiento entre menú y handler

2. ESTABILIDAD MÁXIMA
   ✅ Código asignado una vez = permanente
   ✅ No hay razón para cambiar códigos
   ✅ Referencias nunca se rompen

3. FLEXIBILIDAD
   ✅ Un handler puede usarse en múltiples categorías
   ✅ Reorganizar menú = cambiar solo tabla, no códigos
   ✅ Mismo handler en varias opciones diferentes

4. ESCALABILIDAD
   ✅ A-Z (26) + AA-ZZ (676) = 702 handlers posibles
   ✅ Más que suficiente para cualquier proyecto
   ✅ Espacio de crecimiento enorme

5. REUTILIZACIÓN
   ✅ "Incidente Técnico" (categoría Solicitud) → A001
   ✅ "Reportar Problema" (categoría Soporte) → A001 (mismo handler)
   ✅ No duplicar handlers por estar en categorías diferentes

6. NEUTRO
   ✅ Código no sugiere nada (es solo secuencial)
   ✅ No genera confusión si la opción cambia de categoría
```

### ⚠️ Desventajas:

```
1. MENOS INTUITIVO
   ⚠️ A001 no indica qué hace (necesitas consultar catálogo)
   ⚠️ No puedes adivinar función por el código

2. DOCUMENTACIÓN CRÍTICA
   ⚠️ DEBES tener catálogo actualizado
   ⚠️ Sin descripción, no sabes qué hace A001

3. REORGANIZACIÓN MENOS VISUAL
   ⚠️ No puedes listar "todos los de Ventas" por código
   ⚠️ Necesitas metadata/tags para agrupar
```

### 📊 Tabla Completa (PARTE 2):

```
┌──────────┬─────────────────────────────────────┬──────────────────────────────┐
│ Código   │ Función del Handler                 │ Archivo Handler              │
│          │ (independiente del menú)            │                              │
├──────────┼─────────────────────────────────────┼──────────────────────────────┤
│ A001     │ Captura incidentes con              │ handler_captura_incidente.py │
│          │ escalamiento automático             │                              │
├──────────┼─────────────────────────────────────┼──────────────────────────────┤
│ B001     │ Solicitudes estándar 2 preguntas    │ handler_solicitud_basica.py  │
├──────────┼─────────────────────────────────────┼──────────────────────────────┤
│ C001     │ Proceso RFC con validación          │ handler_proceso_rfc.py       │
│          │ aprobador y CAB                     │                              │
├──────────┼─────────────────────────────────────┼──────────────────────────────┤
│ D001     │ Cotización con cálculo automático   │ handler_cotizacion_auto.py   │
│          │ de precios y generación PDF         │                              │
├──────────┼─────────────────────────────────────┼──────────────────────────────┤
│ E001     │ Envío de documento PDF sin          │ handler_enviar_pdf.py        │
│          │ preguntas (genérico)                │                              │
├──────────┼─────────────────────────────────────┼──────────────────────────────┤
│ F001     │ Consulta API externa para           │ handler_consulta_api.py      │
│          │ seguimiento (ERP, CRM, etc)         │                              │
├──────────┼─────────────────────────────────────┼──────────────────────────────┤
│ G001     │ Asignación directa a grupo sin      │ handler_asignar_simple.py    │
│          │ captura de datos                    │                              │
├──────────┼─────────────────────────────────────┼──────────────────────────────┤
│ H001     │ Urgencias con notificación multi-   │ handler_urgencia_multi.py    │
│          │ canal (SMS, email, Teams)           │                              │
├──────────┼─────────────────────────────────────┼──────────────────────────────┤
│ I001     │ Consulta inventario en tiempo real  │ handler_consulta_inventario.py│
├──────────┼─────────────────────────────────────┼──────────────────────────────┤
│ J001     │ Registro quejas con seguimiento     │ handler_registro_queja.py    │
├──────────┼─────────────────────────────────────┼──────────────────────────────┤
│ Z001     │ Último handler alfabético simple    │ handler_z001.py              │
├──────────┼─────────────────────────────────────┼──────────────────────────────┤
│ AA01     │ Handler 27 (doble letra)            │ handler_aa01.py              │
├──────────┼─────────────────────────────────────┼──────────────────────────────┤
│ ZZ99     │ Handler por defecto / fallback      │ handler_default.py           │
└──────────┴─────────────────────────────────────┴──────────────────────────────┘
```

### 🔄 Ejemplo de Reutilización:

Con códigos independientes, un handler puede usarse en múltiples lugares:

```
MENÚ:

1. Solicitud Ticket
   ├─ 1.1 Incidente Técnico      → A001
   ├─ 1.2 Solicitud Servicio      → B001
   └─ 1.3 Cambio RFC              → C001

2. Ventas
   ├─ 2.1 Cotización              → D001
   ├─ 2.2 Catálogo                → E001
   └─ 2.3 Seguimiento             → F001

3. Soporte Rápido
   ├─ 3.1 Reportar Error          → A001  ← MISMO QUE 1.1 (reutilizado)
   ├─ 3.2 Problema Urgente        → H001
   └─ 3.3 Consulta Rápida         → G001

4. Inventario
   ├─ 4.1 Consultar Existencias   → I001
   ├─ 4.2 Solicitar Reabasto      → B001  ← MISMO QUE 1.2 (reutilizado)
   └─ 4.3 Ver Catálogo            → E001  ← MISMO QUE 2.2 (reutilizado)
```

**Ventaja:** 
- Opción 1.1 y 3.1 usan el MISMO handler (A001)
- Si el nombre de 1.1 cambia de "Incidente Técnico" a "Reportar Falla"
- El código A001 NO cambia, sigue funcionando
- 3.1 no se afecta para nada

---

## 🆚 COMPARACIÓN: PARTE 1 vs PARTE 2

### 📊 Tabla Comparativa Completa:

```
┌─────────────────────────────┬───────────────────────────┬───────────────────────────┐
│ Característica              │ PARTE 1 (Por Categoría)   │ PARTE 2 (Independiente)   │
├─────────────────────────────┼───────────────────────────┼───────────────────────────┤
│ FORMATO                     │ S001, V001, A001          │ A001, B001, C001...Z001   │
│                             │ Letra = Categoría menú    │ Letra = Secuencial        │
├─────────────────────────────┼───────────────────────────┼───────────────────────────┤
│ LONGITUD                    │ 4 caracteres              │ 4 caracteres              │
│                             │ (igual)                   │ (igual)                   │
├─────────────────────────────┼───────────────────────────┼───────────────────────────┤
│ INDEPENDENCIA DEL MENÚ      │ ⚠️ PARCIAL                │ ✅ TOTAL                  │
│                             │ Letra sugiere categoría   │ Sin relación con menú     │
├─────────────────────────────┼───────────────────────────┼───────────────────────────┤
│ CAMBIAR NOMBRE ELEMENTO     │ ✅ OK (no afecta)         │ ✅ OK (no afecta)         │
│ "Incidente" → "Reporte"     │                           │                           │
├─────────────────────────────┼───────────────────────────┼───────────────────────────┤
│ CAMBIAR NOMBRE CATEGORÍA    │ ⚠️ Código queda obsoleto  │ ✅ OK (no afecta)         │
│ "Solicitud" → "Tickets"     │ S001 sugiere "Solicitud"  │ A001 no sugiere nada      │
├─────────────────────────────┼───────────────────────────┼───────────────────────────┤
│ MOVER OPCIÓN DE CATEGORÍA   │ ⚠️ Idealmente cambiar     │ ✅ OK (no afecta)         │
│ 1.1 → 3.1                   │ S001 → A001               │ A001 sigue siendo A001    │
├─────────────────────────────┼───────────────────────────┼───────────────────────────┤
│ REUTILIZAR HANDLER          │ ⚠️ Confuso                │ ✅ NATURAL                │
│ Mismo handler en 2          │ S001 en categoría V?      │ A001 donde sea            │
│ categorías diferentes       │ (sugiere otra categoría)  │ (neutro)                  │
├─────────────────────────────┼───────────────────────────┼───────────────────────────┤
│ INTUITIVIDAD                │ ✅ ALTA                   │ ⚠️ BAJA                   │
│ ¿Qué hace el código?        │ S = Solicitud (claro)     │ A = ??? (consultar)       │
├─────────────────────────────┼───────────────────────────┼───────────────────────────┤
│ ORGANIZACIÓN                │ ✅ Por categoría          │ ⚠️ Secuencial             │
│                             │ S* = Solicitudes          │ A-Z sin agrupación        │
├─────────────────────────────┼───────────────────────────┼───────────────────────────┤
│ BÚSQUEDA POR CATEGORÍA      │ ✅ FÁCIL                  │ ⚠️ Requiere metadata      │
│ "Todos los de Ventas"       │ Buscar V*                 │ Buscar tag "Ventas"       │
├─────────────────────────────┼───────────────────────────┼───────────────────────────┤
│ ESCALABILIDAD               │ ⚠️ 999 por categoría      │ ✅ 702 total (A-ZZ)       │
│                             │ 26 categorías máximo      │ Sin límite de categorías  │
├─────────────────────────────┼───────────────────────────┼───────────────────────────┤
│ ESTABILIDAD CÓDIGOS         │ ⚠️ MEDIA                  │ ✅ ALTA                   │
│                             │ Cambios estructurales     │ Nunca cambian             │
│                             │ pueden requerir cambios   │                           │
├─────────────────────────────┼───────────────────────────┼───────────────────────────┤
│ DOCUMENTACIÓN               │ ⚠️ Importante             │ ⚠️⚠️ CRÍTICA             │
│                             │ Letra da pista            │ Sin pista, catálogo vital │
├─────────────────────────────┼───────────────────────────┼───────────────────────────┤
│ IDEAL PARA                  │ ✓ Menús estables          │ ✓ Menús cambiantes        │
│                             │ ✓ Categorías claras       │ ✓ Handlers reutilizables  │
│                             │ ✓ Equipos pequeños        │ ✓ Sistemas grandes        │
│                             │ ✓ Prototipado rápido      │ ✓ Producción long-term    │
└─────────────────────────────┴───────────────────────────┴───────────────────────────┘
```

### 🎯 Ejemplos Lado a Lado:

#### Escenario 1: Cambio de Nombre de Elemento

```
ANTES:
cr321_elemento1: "Incidente Técnico"

PARTE 1: cr321_handler1: "S001"
PARTE 2: cr321_handler1: "A001"

DESPUÉS (cambias a "Reporte de Falla"):
cr321_elemento1: "Reporte de Falla"

PARTE 1: cr321_handler1: "S001"  ✅ Sigue funcionando
PARTE 2: cr321_handler1: "A001"  ✅ Sigue funcionando

RESULTADO: Ambas opciones funcionan igual ✅
```

#### Escenario 2: Cambio de Nombre de Categoría

```
ANTES:
Categoría: "1. Solicitud Ticket"
  └─ 1.1 Incidente Técnico

PARTE 1: cr321_handler1: "S001"  (S = Solicitud)
PARTE 2: cr321_handler1: "A001"  (A = secuencial)

DESPUÉS (cambias a "1. Gestión de Tickets"):
Categoría: "1. Gestión de Tickets"
  └─ 1.1 Incidente Técnico

PARTE 1: cr321_handler1: "S001"  ⚠️ Funciona, pero "S" ya no significa nada
         (confunde: S sugería Solicitud, ahora es Gestión)
         
PARTE 2: cr321_handler1: "A001"  ✅ Funciona, "A" nunca significó nada específico
         (no genera confusión)

RESULTADO: PARTE 2 mejor ✅
```

#### Escenario 3: Mover Opción a Otra Categoría

```
ANTES:
1. Solicitud Ticket
   └─ 1.1 Incidente Técnico → S001

3. Atención
   └─ 3.1 Asignación Directa → A001

DESPUÉS (mueves Incidente Técnico a Atención):
1. Solicitud Ticket
   └─ (vacío)

3. Atención
   ├─ 3.1 Asignación Directa → A001
   └─ 3.2 Incidente Técnico → S001  ⚠️ (S en categoría A?)

PARTE 1: Confuso - S001 sugiere Solicitud pero está en Atención
         Idealmente deberías cambiar S001 → A002
         
PARTE 2: No hay confusión - A001, B001 son neutrales
         No importa en qué categoría estén

RESULTADO: PARTE 2 mejor ✅
```

#### Escenario 4: Reutilizar Handler en Varias Categorías

```
ESCENARIO:
Quieres usar el MISMO handler de "captura básica de tickets"
en 3 lugares diferentes:

1. Solicitud Ticket
   └─ 1.2 Solicitud Servicio → ???

2. Ventas
   └─ 2.4 Reclamo → ???

3. Soporte
   └─ 3.3 Consulta → ???

PARTE 1:
1.2 → S002 (S = Solicitud) ✓ OK
2.4 → V004 (V = Ventas)    ⚠️ Confuso (handler no es de ventas)
3.3 → A003 (A = Atención)  ⚠️ Confuso (handler no es de atención)

Problemas:
- Letra sugiere categoría incorrecta
- Parece que son 3 handlers diferentes
- Confuso en mantenimiento

PARTE 2:
1.2 → B001
2.4 → B001  ← MISMO CÓDIGO
3.3 → B001  ← MISMO CÓDIGO

Ventajas:
- Código neutral, no sugiere nada
- Claro que es el mismo handler
- Fácil de mantener

RESULTADO: PARTE 2 mucho mejor ✅✅
```

### 🏆 Recomendación Final:

```
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│  SI TU MENÚ:                         USA:                      │
│                                                                │
│  ✓ Es estable (no cambia mucho)     PARTE 1 (Por Categoría)   │
│  ✓ Categorías claras y fijas         S001, V001, A001         │
│  ✓ Handlers únicos por categoría     ✅ Intuitivo             │
│  ✓ Equipo pequeño                                              │
│  ✓ Prototipo o MVP                                             │
│                                                                │
│  ─────────────────────────────────────────────────────────────│
│                                                                │
│  ✓ Cambia frecuentemente             PARTE 2 (Independiente)  │
│  ✓ Handlers reutilizables            A001, B001, C001         │
│  ✓ Reorganizaciones del menú         ✅ Flexible              │
│  ✓ Sistema grande / producción                                │
│  ✓ Múltiples devs / long-term                                 │
│                                                                │
└────────────────────────────────────────────────────────────────┘

🎯 PARA TU CASO (Sistema de menú con WhatsApp):

RECOMENDACIÓN: **PARTE 2 (Códigos Independientes)**

RAZONES:
✅ Menús de chatbot frecuentemente se reorganizan
✅ Opciones se mueven, renombran, combinan
✅ Quieres handlers reutilizables (eficiencia)
✅ Sistema en producción long-term
✅ El catálogo JSON compensa la falta de intuitividad

FORMATO RECOMENDADO:
A001, B001, C001, D001, E001...
(hasta Z001, luego AA01, AB01... si necesitas más)
```

---

## 📘 EXPLICACIÓN DETALLADA - OPCIÓN B (JSON) CON CÓDIGOS INDEPENDIENTES

### 🎯 Concepto General:

La **Opción B** usa un archivo JSON como "catálogo" que mapea códigos cortos (S001, V001) a archivos Python específicos.

```
┌────────────────────────────────────────────────────────────────┐
│ FLUJO COMPLETO                                                 │
└────────────────────────────────────────────────────────────────┘

1. Usuario escribe en WhatsApp: "1"
2. Sistema consulta Dataverse tabla cr321_chatbots
3. Encuentra: cr321_handler1 = "S001"
4. Sistema abre archivo: handlers/config_handlers.json
5. Busca código "S001" en el JSON
6. Lee nombre de archivo: "handler_incidente_tecnico.py"
7. Carga dinámicamente ese archivo Python
8. Ejecuta el handler
```

---

## 🏗️ ESTRUCTURA DE ARCHIVOS DETALLADA

### En tu Proyecto (C:\VS\BIN):

```
C:\VS\BIN\
│
├── sistema_menu_modular.py           ← Programa principal (motor)
│
├── handlers/                          ← Carpeta de handlers
│   │
│   ├── config_handlers.json          ← ARCHIVO JSON (catálogo de códigos)
│   │
│   ├── base_handler.py               ← Clase base (todos heredan de esta)
│   │
│   ├── handler_incidente_tecnico.py  ← Handler específico (S001)
│   ├── handler_solicitud_servicio.py ← Handler específico (S002)
│   ├── handler_cambio_rfc.py         ← Handler específico (S003)
│   ├── handler_cotizacion.py         ← Handler específico (V001)
│   ├── handler_catalogo_pdf.py       ← Handler específico (V002)
│   ├── handler_seguimiento_pedido.py ← Handler específico (V003)
│   ├── handler_asignar_directo.py    ← Handler específico (A001)
│   ├── handler_urgencia_prioridad.py ← Handler específico (A002)
│   └── handler_default.py            ← Handler por defecto (X999)
│
├── requirements.txt
└── README.md
```

---

## 📄 ARCHIVO 1: config_handlers.json (CATÁLOGO)

### Propósito:
Este archivo es el **"catálogo maeastro"** que dice:
- Qué código existe (S001, V001, etc.)
- Qué archivo Python ejecutar
- Metadata útil (descripción, si está activo, cuántas preguntas hace, etc.)

### Contenido Completo:

```json
{
  "S001": {
    "codigo": "S001",
    "nombre": "Incidente Técnico",
    "archivo": "handler_incidente_tecnico.py",
    "clase": "HandlerIncidenteTecnico",
    "descripcion": "Manejo de incidentes técnicos con escalamiento automático según severidad",
    "activo": true,
    "categoria": "Solicitud Ticket",
    "preguntas": 3,
    "requiere_grupo": true,
    "puede_escalar": true,
    "prioridad_default": "Media",
    "version": "1.2.0",
    "notas": "Escala automáticamente si afecta >50 usuarios o servicio caído"
  },
  
  "S002": {
    "codigo": "S002",
    "nombre": "Solicitud de Servicio",
    "archivo": "handler_solicitud_servicio.py",
    "clase": "HandlerSolicitudServicio",
    "descripcion": "Solicitudes estándar de servicio con 2 preguntas básicas",
    "activo": true,
    "categoria": "Solicitud Ticket",
    "preguntas": 2,
    "requiere_grupo": true,
    "puede_escalar": false,
    "prioridad_default": "Baja",
    "version": "1.0.0",
    "notas": "Handler básico sin validaciones complejas"
  },
  
  "S003": {
    "codigo": "S003",
    "nombre": "Cambio Programado (RFC)",
    "archivo": "handler_cambio_rfc.py",
    "clase": "HandlerCambioRFC",
    "descripcion": "Solicitudes de cambio con validación de aprobador y notificación a CAB",
    "activo": true,
    "categoria": "Solicitud Ticket",
    "preguntas": 4,
    "requiere_grupo": true,
    "requiere_aprobacion": true,
    "notifica_cab": true,
    "prioridad_default": "Media",
    "version": "2.0.1",
    "notas": "Valida que usuario tenga rol de aprobador antes de crear RFC"
  },
  
  "V001": {
    "codigo": "V001",
    "nombre": "Solicitar Cotización",
    "archivo": "handler_cotizacion.py",
    "clase": "HandlerCotizacion",
    "descripcion": "Genera cotizaciones con cálculo automático de precios y envío de PDF",
    "activo": true,
    "categoria": "Ventas",
    "preguntas": 2,
    "requiere_grupo": true,
    "genera_pdf": true,
    "envia_email": true,
    "integra_con": "ERP",
    "version": "1.5.0",
    "notas": "Consulta precios en ERP, aplica descuentos según cliente"
  },
  
  "V002": {
    "codigo": "V002",
    "nombre": "Ver Catálogo de Productos",
    "archivo": "handler_catalogo_pdf.py",
    "clase": "HandlerCatalogoPDF",
    "descripcion": "Envía catálogo en PDF, sin hacer preguntas",
    "activo": true,
    "categoria": "Ventas",
    "preguntas": 0,
    "requiere_grupo": false,
    "envia_archivo": true,
    "ruta_archivo": "/docs/catalogo_productos_2026.pdf",
    "version": "1.0.0",
    "notas": "Handler automático, solo envía PDF y termina"
  },
  
  "V003": {
    "codigo": "V003",
    "nombre": "Seguimiento de Pedido",
    "archivo": "handler_seguimiento_pedido.py",
    "clase": "HandlerSeguimientoPedido",
    "descripcion": "Consulta estado de pedido en sistema ERP",
    "activo": true,
    "categoria": "Ventas",
    "preguntas": 1,
    "requiere_grupo": false,
    "integra_con": "ERP",
    "consulta_api": "https://erp.empresa.com/api/pedidos",
    "version": "1.3.0",
    "notas": "Pide número de pedido y consulta ERP en tiempo real"
  },
  
  "A001": {
    "codigo": "A001",
    "nombre": "Asignación Directa",
    "archivo": "handler_asignar_directo.py",
    "clase": "HandlerAsignarDirecto",
    "descripcion": "Asigna conversación directamente a un grupo sin hacer preguntas",
    "activo": true,
    "categoria": "Solicitar Atención",
    "preguntas": 0,
    "requiere_grupo": true,
    "tipo_asignacion": "inmediata",
    "version": "1.0.0",
    "notas": "Solo asigna y notifica al grupo, sin capturar datos"
  },
  
  "A002": {
    "codigo": "A002",
    "nombre": "Atención Urgente",
    "archivo": "handler_urgencia_prioridad.py",
    "clase": "HandlerUrgenciaPrioridad",
    "descripcion": "Manejo de urgencias con notificación SMS a supervisores",
    "activo": true,
    "categoria": "Solicitar Atención",
    "preguntas": 1,
    "requiere_grupo": true,
    "prioridad_default": "Urgente",
    "envia_sms": true,
    "notifica_gerencia": true,
    "telefonos_notificar": ["+573001234567", "+573007654321"],
    "version": "1.4.0",
    "notas": "Envía SMS inmediatamente al asignar, para urgencias reales"
  },
  
  "X999": {
    "codigo": "X999",
    "nombre": "Handler por Defecto",
    "archivo": "handler_default.py",
    "clase": "HandlerDefault",
    "descripcion": "Handler genérico usado cuando no se encuentra el código especificado",
    "activo": true,
    "categoria": "Sistema",
    "preguntas": 0,
    "requiere_grupo": true,
    "es_fallback": true,
    "version": "1.0.0",
    "notas": "Se usa automáticamente si el código no existe o está inactivo"
  }
}
```

### 📝 Explicación de Campos en JSON:

```javascript
{
  "A001": {                           // ← Código único (4 caracteres)
    
    "codigo": "A001",                 // ← Código del handler
    "nombre": "Incidente Técnico",    // ← Nombre descriptivo (documentación)
    
    "archivo": "handler_A001.py",     // ← ARCHIVO PYTHON (nombre = código)
    "clase": "HandlerA001",           // ← CLASE DENTRO DEL ARCHIVO (= código)
    
    "activo": true,                   // ← Si false, no se usa (deshabilitado)
    
    "preguntas": 3,                   // ← Cuántas preguntas hace
    
    "grupo_asignado": null,           // ← Grupo específico o null
    "usa_grupo_de_menu": true,        // ← Si usa grupo del menú (cr321_grupo1)
    
    "descripcion": "...",             // ← Descripción larga (documentación)
    
    "version": "1.2.0",               // ← Control de versiones
    
    "tags": ["tickets", "..."],      // ← Tags para búsqueda/categorización
    
    "notas": "..."                    // ← Notas para desarrolladores
  }
}

// CONVENCIÓN DE NOMBRES:
// Código:   "A001"
// Archivo:  "handler_A001.py"
// Clase:    "HandlerA001"
// ✅ Consistencia perfecta
```

### 🔑 Campos Obligatorios vs Opcionales:

**OBLIGATORIOS** (el sistema los necesita):
- `codigo` - Código único del handler (ej: "A001")
- `archivo` - Nombre del archivo Python a cargar (ej: "handler_A001.py")
- `clase` - Nombre de la clase dentro del archivo (ej: "HandlerA001")
- `activo` - true/false (si está habilitado)

**RECOMENDADOS** (para manejo de grupos):
- `grupo_override` - GUID específico del grupo o null
  - Si es `null`: usa el grupo de Dataverse
  - Si tiene GUID: usa este grupo (override)
- `usa_grupo_de_dataverse` - true/false
  - Si `true`: usa **cr321_grupoid** del chatbot
  - Si `false`: NO asigna a grupo (o usa grupo_override si está definido)

**OPCIONALES** (para documentación/metadata):
- `nombre` - Nombre descriptivo
- `descripcion` - Descripción larga
- `preguntas` - Cantidad de preguntas (informativo)
- `version` - Control de versiones
- `tags` - Tags para búsqueda/categorización
- `notas` - Notas para desarrolladores
- Puedes agregar los campos que quieras

### 📊 Campos en Dataverse (ya existen):

```
Tabla: cr321_chatbots

✅ cr321_config    (Texto) - Código del handler (ej: "A001")
✅ cr321_grupoid   (Lookup) - GUID del grupo asignado
✅ cr321_elemento1 (Texto) - Nombre visible en menú

NO necesitas crear:
❌ cr321_handler1-5 (ya no necesarios)
```

### 📋 Lógica de Asignación de Grupo (usando campos existentes):

```
┌─────────────────────────────────────────────────────────────┐
│ CASO 1: Usar grupo de Dataverse (configuración estándar)   │
├─────────────────────────────────────────────────────────────┤
│ JSON Handler:                                               │
│ "grupo_override": null,                                     │
│ "usa_grupo_de_dataverse": true                             │
│                                                             │
│ Dataverse (tabla cr321_chatbots):                          │
│ cr321_config:   "A001"                                      │
│ cr321_grupoid:  "{GUID-SOPORTE-TI}"  ← Usa este grupo      │
│                                                             │
│ → Sistema usa cr321_grupoid del chatbot                     │
│ → Flexibilidad: cambias grupo en Dataverse, handler adapta │
│ → Configuración más común (90% de casos)                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ CASO 2: Grupo específico fijo (override)                   │
├─────────────────────────────────────────────────────────────┤
│ JSON Handler:                                               │
│ "grupo_override": "{GUID-SUPERVISORES}",                   │
│ "usa_grupo_de_dataverse": false                            │
│                                                             │
│ Dataverse (tabla cr321_chatbots):                          │
│ cr321_config:   "H001"                                      │
│ cr321_grupoid:  "{GUID-X}"  ← IGNORADO por handler         │
│                                                             │
│ → Sistema IGNORA cr321_grupoid                              │
│ → Siempre usa el GUID del JSON (grupo_override)            │
│ → Útil para: urgencias, escalamientos, casos especiales    │
│ → Ejemplo: Todas las urgencias van a Supervisores          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ CASO 3: Sin asignación (solo responde)                     │
├─────────────────────────────────────────────────────────────┤
│ JSON Handler:                                               │
│ "grupo_override": null,                                     │
│ "usa_grupo_de_dataverse": false                            │
│                                                             │
│ Dataverse (tabla cr321_chatbots):                          │
│ cr321_config:   "E001"                                      │
│ cr321_grupoid:  null  ← No se usa                           │
│                                                             │
│ → Sistema NO asigna a ningún grupo                          │
│ → Solo ejecuta el handler y responde                        │
│ → Útil para: consultas, envío de PDFs, respuestas auto     │
│ → Ejemplo: Enviar catálogo PDF (no necesita agente)        │
└─────────────────────────────────────────────────────────────┘

### 💡 Ejemplo Práctico Completo:

**Configuración en Dataverse:**
```sql
-- Opción 1.1: Incidente Técnico
cr321_elemento1: "Incidente Técnico"
cr321_config:    "A001"                    ← Código handler
cr321_grupoid:   "{GUID-SOPORTE-TI}"       ← Grupo normal

-- Opción 2.2: Ver Catálogo
cr321_elemento1: "Ver Catálogo de Productos"
cr321_config:    "E001"                    ← Código handler
cr321_grupoid:   null                      ← Sin grupo (no necesita)

-- Opción 3.1: Urgencia
cr321_elemento1: "Atención Urgente"
cr321_config:    "H001"                    ← Código handler
cr321_grupoid:   "{GUID-ATENCION}"         ← Grupo sugerido (pero será ignorado)
```

**Configuración en JSON (handlers/config_handlers.json):**
```json
{
  "A001": {
    "archivo": "handler_A001.py",
    "grupo_override": null,
    "usa_grupo_de_dataverse": true
    // → Usará {GUID-SOPORTE-TI} de cr321_grupoid
  },
  
  "E001": {
    "archivo": "handler_E001.py",
    "grupo_override": null,
    "usa_grupo_de_dataverse": false
    // → No asignará a ningún grupo
  },
  
  "H001": {
    "archivo": "handler_H001.py",
    "grupo_override": "{GUID-SUPERVISORES}",
    "usa_grupo_de_dataverse": false
    // → Ignorará {GUID-ATENCION} y usará {GUID-SUPERVISORES}
  }
}
```

---

## 📄 ARCHIVO 2: sistema_menu_modular.py (MOTOR)

### Propósito:
Este es el **programa principal** que:
1. Lee el JSON
2. Consulta Dataverse para saber qué código usar
3. Carga el handler correspondiente
4. Ejecuta el handler

### Código Completo con Explicación Paso a Paso:

```python
import json
import importlib
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, Optional
import requests
from datetime import datetime, timedelta

# Configuración Dataverse
DATAVERSE_URL = "https://tu-org.crm.dynamics.com/api/data/v9.2"
CLIENT_ID = "tu-client-id"
CLIENT_SECRET = "tu-client-secret"
TENANT_ID = "tu-tenant-id"


@dataclass
class ConfigHandler:
    """Representa la configuración de un handler desde el JSON"""
    codigo: str
    archivo: str
    clase: str
    activo: bool
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    preguntas: int = 0
    # Puedes agregar más campos según necesites


class SistemaMenuModular:
    """
    Sistema de menú modular con handlers configurables vía JSON.
    
    FLUJO PRINCIPAL:
    1. Cargar config_handlers.json al iniciar
    2. Usuario envía mensaje
    3. Consultar Dataverse para saber qué handler usar
    4. Buscar handler en config JSON
    5. Cargar dinámicamente el archivo Python
    6. Ejecutar el handler
    """
    
    def __init__(self):
        """Inicializa el sistema"""
        
        # 1. Cargar configuración de handlers desde JSON
        self.config_handlers = self._cargar_config_json()
        print(f"✓ Cargados {len(self.config_handlers)} handlers desde JSON")
        
        # 2. Obtener token de Dataverse
        self.token = self._obtener_token()
        print(f"✓ Token de Dataverse obtenido")
        
        # 3. Configurar headers para API
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
        
        # 4. Estado de usuarios (en memoria, podrías usar Redis)
        self.estados_usuarios = {}
    
    
    def _cargar_config_json(self) -> Dict[str, ConfigHandler]:
        """
        Carga el archivo config_handlers.json y lo convierte en objetos Python.
        
        PASO A PASO:
        1. Encontrar ruta del archivo JSON (handlers/config_handlers.json)
        2. Leer el archivo JSON
        3. Parsear JSON a diccionario Python
        4. Convertir cada entrada a objeto ConfigHandler
        5. Retornar diccionario {codigo: ConfigHandler}
        """
        
        # 1. Construir ruta al archivo JSON
        # Path(__file__) = ruta de este archivo .py
        # .parent = carpeta que contiene este archivo
        # / "handlers" / "config_handlers.json" = ruta completa
        ruta_json = Path(__file__).parent / "handlers" / "config_handlers.json"
        
        print(f"→ Buscando JSON en: {ruta_json}")
        
        # 2. Verificar que archivo existe
        if not ruta_json.exists():
            raise FileNotFoundError(
                f"No se encontró config_handlers.json en {ruta_json}. "
                "Por favor créalo primero."
            )
        
        # 3. Leer archivo JSON
        with open(ruta_json, 'r', encoding='utf-8') as f:
            data = json.load(f)  # Convierte JSON a diccionario Python
        
        # 4. Convertir cada entrada a objeto ConfigHandler
        config_handlers = {}
        
        for codigo, config in data.items():
            # Verificar campos obligatorios
            if not all(k in config for k in ['archivo', 'clase', 'activo']):
                print(f"⚠️ Handler {codigo} incompleto, saltando...")
                continue
            
            # Crear objeto ConfigHandler
            handler_config = ConfigHandler(
                codigo=config.get('codigo', codigo),
                archivo=config['archivo'],
                clase=config['clase'],
                activo=config['activo'],
                nombre=config.get('nombre'),
                descripcion=config.get('descripcion'),
                preguntas=config.get('preguntas', 0)
            )
            
            config_handlers[codigo] = handler_config
            print(f"  ✓ {codigo}: {handler_config.nombre}")
        
        # 5. Retornar diccionario
        return config_handlers
    
    
    def obtener_handler_para_opcion(self, subopcion: str, chatbot_data: dict) -> str:
        """
        Determina qué código de handler usar según la subopción seleccionada.
        
        EJEMPLO:
        subopcion = "1.1" 
        chatbot_data = {"cr321_handler1": "S001", "cr321_handler2": "S002", ...}
        
        RETORNA: "S001"
        """
        
        # Mapeo de subopción a campo en tabla
        mapeo = {
            "1.1": "cr321_handler1",
            "1.2": "cr321_handler2",
            "1.3": "cr321_handler3",
            "1.4": "cr321_handler4",
            "1.5": "cr321_handler5",
        }
        
        # Si subopción no tiene handler configurado, usar default
        campo_handler = mapeo.get(subopcion)
        if not campo_handler:
            return "X999"  # Handler por defecto
        
        # Obtener código del chatbot
        codigo = chatbot_data.get(campo_handler)
        
        # Si no hay código o está vacío, usar default
        if not codigo or codigo.strip() == "":
            return "X999"
        
        return codigo
    
    
    def cargar_handler_dinamico(self, codigo: str):
        """
        Carga dinámicamente un handler según su código.
        
        PASO A PASO:
        1. Buscar código en config_handlers
        2. Verificar que esté activo
        3. Obtener nombre de archivo y clase
        4. Importar el módulo Python dinámicamente
        5. Obtener la clase del módulo
        6. Instanciar la clase
        7. Retornar instancia
        
        EJEMPLO:
        codigo = "S001"
        
        → Busca en JSON: "archivo": "handler_incidente_tecnico.py"
        → Importa: handlers.handler_incidente_tecnico
        → Obtiene clase: HandlerIncidenteTecnico
        → Instancia y retorna
        """
        
        print(f"\n→ Cargando handler: {codigo}")
        
        # 1. Buscar en configuración
        if codigo not in self.config_handlers:
            print(f"⚠️ Código {codigo} no encontrado, usando default X999")
            codigo = "X999"
        
        config = self.config_handlers[codigo]
        
        # 2. Verificar que esté activo
        if not config.activo:
            print(f"⚠️ Handler {codigo} está desactivado, usando default X999")
            codigo = "X999"
            config = self.config_handlers["X999"]
        
        # 3. Obtener nombre de archivo y clase
        nombre_archivo = config.archivo.replace('.py', '')  # Quitar .py
        nombre_clase = config.clase
        
        print(f"  → Archivo: {nombre_archivo}")
        print(f"  → Clase: {nombre_clase}")
        
        try:
            # 4. Importar módulo dinámicamente
            # Ejemplo: importlib.import_module("handlers.handler_incidente_tecnico")
            modulo = importlib.import_module(f"handlers.{nombre_archivo}")
            
            # 5. Obtener la clase del módulo
            # Ejemplo: getattr(modulo, "HandlerIncidenteTecnico")
            clase_handler = getattr(modulo, nombre_clase)
            
            # 6. Instanciar la clase
            instancia = clase_handler(
                dataverse_url=DATAVERSE_URL,
                headers=self.headers
            )
            
            print(f"  ✓ Handler {codigo} cargado exitosamente")
            
            # 7. Retornar instancia
            return instancia
            
        except Exception as e:
            print(f"❌ Error al cargar handler {codigo}: {e}")
            print(f"  → Cargando handler por defecto X999")
            
            # Fallback al handler default
            modulo = importlib.import_module("handlers.handler_default")
            clase_handler = getattr(modulo, "HandlerDefault")
            return clase_handler(
                dataverse_url=DATAVERSE_URL,
                headers=self.headers
            )
    
    
    def procesar_mensaje(self, from_user: str, mensaje: str):
        """
        Procesa un mensaje de usuario.
        
        FLUJO COMPLETO:
        1. Usuario envía "1" → Mostrar submenú 1
        2. Usuario envía "1" de nuevo → Selecciona subopción 1.1
        3. Sistema consulta Dataverse: cr321_handler1 = "S001"
        4. Sistema busca "S001" en config_handlers.json
        5. JSON dice: archivo = "handler_incidente_tecnico.py"
        6. Sistema carga ese archivo
        7. Ejecuta el handler
        """
        
        print(f"\n{'='*60}")
        print(f"MENSAJE DE: {from_user}")
        print(f"CONTENIDO: {mensaje}")
        print(f"{'='*60}")
        
        # Aquí va la lógica del menú (similar a sistema_menu_con_tickets.py)
        # Por simplicidad, asumamos que usuario ya seleccionó subopción 1.1
        
        # EJEMPLO: Usuario seleccionó opción 1.1 (Incidente Técnico)
        subopcion = "1.1"
        
        # 1. Consultar Dataverse para obtener configuración del chatbot
        chatbot_data = self._obtener_chatbot_principal()
        
        # 2. Determinar qué handler usar
        codigo_handler = self.obtener_handler_para_opcion(subopcion, chatbot_data)
        print(f"→ Handler a usar: {codigo_handler}")
        
        # 3. Cargar handler dinámicamente
        handler = self.cargar_handler_dinamico(codigo_handler)
        
        # 4. Obtener configuración del handler desde JSON
        config = self.config_handlers[codigo_handler]
        print(f"→ Configuración:")
        print(f"  - Nombre: {config.nombre}")
        print(f"  - Preguntas: {config.preguntas}")
        print(f"  - Descripción: {config.descripcion}")
        
        # 5. Ejecutar handler
        print(f"\n→ Ejecutando handler...")
        resultado = handler.ejecutar(
            from_user=from_user,
            mensaje=mensaje,
            grupo_id=chatbot_data.get('cr321_grupo1')
        )
        
        print(f"✓ Handler ejecutado exitosamente")
        return resultado
    
    
    def _obtener_chatbot_principal(self) -> dict:
        """Obtiene configuración del chatbot desde Dataverse"""
        
        response = requests.get(
            f"{DATAVERSE_URL}/cr321_chatbots?$filter=cr321_orden eq 0",
            headers=self.headers
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['value']:
                return data['value'][0]
        
        raise Exception("No se pudo obtener configuración del chatbot")
    
    
    def _obtener_token(self) -> str:
        """Obtiene token OAuth de Microsoft"""
        
        token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
        
        data = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "scope": f"{DATAVERSE_URL}/.default",
            "grant_type": "client_credentials"
        }
        
        response = requests.post(token_url, data=data)
        
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            raise Exception(f"Error obteniendo token: {response.text}")


# ============================================================================
# EJECUCIÓN
# ============================================================================

if __name__ == "__main__":
    print("="*60)
    print("SISTEMA DE MENÚ MODULAR CON HANDLERS")
    print("="*60)
    
    # 1. Inicializar sistema
    sistema = SistemaMenuModular()
    
    # 2. Simular mensaje de usuario
    resultado = sistema.procesar_mensaje(
        from_user="573001234567@s.whatsapp.net",
        mensaje="Mi sistema no funciona"
    )
    
    print("\n" + "="*60)
    print("PROCESO COMPLETADO")
    print("="*60)
```

---

## 📄 ARCHIVO 3: handlers/base_handler.py (CLASE BASE)

### Propósito:
Todos los handlers heredan de esta clase base.

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import requests


class BaseHandler(ABC):
    """
    Clase base para todos los handlers.
    
    Todos los handlers deben heredar de esta clase e implementar:
    - get_preguntas(): Retorna lista de preguntas a hacer
    - ejecutar_accion_final(): Ejecuta la acción final tras capturar respuestas
    """
    
    def __init__(self, dataverse_url: str, headers: dict):
        """
        Inicializa el handler.
        
        Args:
            dataverse_url: URL de Dataverse (https://org.crm.dynamics.com/api/data/v9.2)
            headers: Headers con token de autenticación
        """
        self.dataverse_url = dataverse_url
        self.headers = headers
    
    
    @abstractmethod
    def get_preguntas(self) -> List[str]:
        """
        Retorna lista de preguntas que el handler necesita hacer al usuario.
        
        DEBE SER IMPLEMENTADO por cada handler específico.
        
        Returns:
            List[str]: Lista de preguntas
            
        Ejemplo:
            return [
                "¿Cuál es el sistema afectado?",
                "¿Cuántos usuarios están afectados?",
                "¿El servicio está completamente caído?"
            ]
        """
        pass
    
    
    @abstractmethod
    def ejecutar_accion_final(
        self,
        from_user: str,
        respuestas: Dict[str, str],
        grupo_id: Optional[str] = None
    ) -> str:
        """
        Ejecuta la acción final después de capturar todas las respuestas.
        
        DEBE SER IMPLEMENTADO por cada handler específico.
        
        Args:
            from_user: Teléfono del usuario
            respuestas: Diccionario con las respuestas {pregunta: respuesta}
            grupo_id: ID del grupo al que asignar (opcional)
        
        Returns:
            str: Mensaje final para enviar al usuario
            
        Ejemplo:
            return "✓ Ticket #12345 creado. Atención en 15 minutos."
        """
        pass
    
    
    def ejecutar(
        self,
        from_user: str,
        mensaje: str,
        grupo_id: Optional[str] = None
    ) -> str:
        """
        Método principal que orquesta el flujo del handler.
        
        Este método YA ESTÁ IMPLEMENTADO en la clase base.
        Los handlers específicos NO necesitan sobreescribirlo.
        
        FLUJO:
        1. Obtener lista de preguntas
        2. Hacer cada pregunta al usuario
        3. Capturar respuestas
        4. Ejecutar acción final
        5. Retornar mensaje final
        """
        
        print(f"\n{'─'*60}")
        print(f"HANDLER EJECUTANDO")
        print(f"{'─'*60}")
        
        # 1. Obtener preguntas
        preguntas = self.get_preguntas()
        print(f"→ Preguntas a hacer: {len(preguntas)}")
        
        # 2. Si no hay preguntas, ejecutar directamente
        if len(preguntas) == 0:
            print("→ No hay preguntas, ejecutando acción directamente")
            return self.ejecutar_accion_final(from_user, {}, grupo_id)
        
        # 3. Hacer preguntas y capturar respuestas
        # (Aquí iría la lógica completa de estado y captura)
        # Por ahora, simulamos respuestas
        respuestas = {}
        for i, pregunta in enumerate(preguntas, 1):
            print(f"  {i}. {pregunta}")
            respuesta = f"Respuesta simulada {i}"
            respuestas[pregunta] = respuesta
            print(f"     → Usuario: {respuesta}")
        
        # 4. Ejecutar acción final
        print(f"\n→ Ejecutando acción final...")
        mensaje_final = self.ejecutar_accion_final(from_user, respuestas, grupo_id)
        
        return mensaje_final
    
    
    def crear_ticket(
        self,
        titulo: str,
        descripcion: str,
        prioridad: str,
        grupo_id: str
    ) -> dict:
        """
        Método auxiliar para crear tickets en Dataverse.
        
        Disponible para todos los handlers que lo necesiten.
        """
        
        ticket_data = {
            "cr321_titulo": titulo,
            "cr321_descripcion": descripcion,
            "cr321_prioridad": prioridad,
            "cr321_grupo@odata.bind": f"/cr321_grups({grupo_id})",
            "cr321_estado": "Nuevo"
        }
        
        response = requests.post(
            f"{self.dataverse_url}/cr321_tickets",
            headers=self.headers,
            json=ticket_data
        )
        
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Error creando ticket: {response.text}")
```

---

## 📄 ARCHIVO 4: handlers/handler_incidente_tecnico.py (EJEMPLO)

### Propósito:
Handler específico para incidentes técnicos (código S001).

```python
from handlers.base_handler import BaseHandler
from typing import List, Dict, Optional


class HandlerIncidenteTecnico(BaseHandler):
    """
    Handler para incidentes técnicos con escalamiento automático.
    
    Código: S001
    Preguntas: 3
    - Sistema afectado
    - Cantidad de usuarios afectados
    - Si está caído completamente
    
    Lógica especial:
    - Si >50 usuarios afectados → Prioridad URGENTE
    - Si servicio caído → Severidad CRÍTICA + Notificar gerencia
    """
    
    def get_preguntas(self) -> List[str]:
        """Define las 3 preguntas para incidentes técnicos"""
        return [
            "¿Cuál es el sistema o aplicación afectada?",
            "¿Aproximadamente cuántos usuarios están afectados?",
            "¿El servicio está completamente caído? (Sí/No)"
        ]
    
    
    def ejecutar_accion_final(
        self,
        from_user: str,
        respuestas: Dict[str, str],
        grupo_id: Optional[str] = None
    ) -> str:
        """
        Crea el ticket con validaciones y escalamiento automático.
        
        LÓGICA:
        1. Analizar respuestas
        2. Determinar prioridad y severidad
        3. Crear ticket
        4. Si es urgente/crítico: Escalar y notificar
        5. Asignar a grupo
        6. Retornar mensaje
        """
        
        print(f"\n→ Analizando respuestas de incidente técnico...")
        
        # 1. Obtener respuestas
        sistema = respuestas.get("¿Cuál es el sistema o aplicación afectada?", "No especificado")
        usuarios_afectados = respuestas.get("¿Aproximadamente cuántos usuarios están afectados?", "0")
        servicio_caido = respuestas.get("¿El servicio está completamente caído? (Sí/No)", "No")
        
        # 2. Determinar prioridad
        try:
            num_usuarios = int(usuarios_afectados)
            if num_usuarios > 50:
                prioridad = "URGENTE"
                print(f"  ⚠️ >50 usuarios afectados → Prioridad: URGENTE")
            else:
                prioridad = "Media"
        except:
            prioridad = "Media"
        
        # 3. Determinar severidad
        severidad = "CRÍTICA" if servicio_caido.lower() in ['sí', 'si', 'yes'] else "Media"
        if severidad == "CRÍTICA":
            print(f"  🚨 Servicio caído → Severidad: CRÍTICA")
        
        # 4. Crear ticket
        descripcion = f"""
INCIDENTE TÉCNICO

Sistema afectado: {sistema}
Usuarios afectados: {usuarios_afectados}
Servicio caído: {servicio_caido}
Prioridad: {prioridad}
Severidad: {severidad}
        """.strip()
        
        ticket = self.crear_ticket(
            titulo=f"Incidente: {sistema}",
            descripcion=descripcion,
            prioridad=prioridad,
            grupo_id=grupo_id
        )
        
        ticket_id = ticket.get('cr321_ticketid', 'XXXXX')
        print(f"  ✓ Ticket #{ticket_id} creado")
        
        # 5. Escalamiento y notificaciones
        if severidad == "CRÍTICA" or prioridad == "URGENTE":
            self._notificar_gerencia(ticket_id, sistema, severidad)
            self._enviar_sms_equipo_guardia(ticket_id)
        
        # 6. Mensaje final
        mensaje = f"""
🚨 Incidente #{ticket_id} registrado

Sistema: {sistema}
Prioridad: {prioridad}
Severidad: {severidad}

Grupo asignado: Soporte Técnico
        """.strip()
        
        if severidad == "CRÍTICA":
            mensaje += "\n\n⚠️ Se notificó a gerencia de TI y equipo de guardia."
        
        return mensaje
    
    
    def _notificar_gerencia(self, ticket_id: str, sistema: str, severidad: str):
        """Notifica a gerencia de TI sobre incidente crítico"""
        print(f"  → Notificando a gerencia sobre ticket #{ticket_id}")
        # Aquí iría integración con email, Teams, etc.
    
    
    def _enviar_sms_equipo_guardia(self, ticket_id: str):
        """Envía SMS a equipo de guardia"""
        print(f"  → Enviando SMS a equipo de guardia sobre ticket #{ticket_id}")
        # Aquí iría integración con Twilio, etc.
```

---

## 📄 ARCHIVO 5: handlers/handler_catalogo_pdf.py (EJEMPLO SIMPLE)

### Propósito:
Handler que NO hace preguntas, solo envía un PDF.

```python
from handlers.base_handler import BaseHandler
from typing import List, Dict, Optional


### PARTE 1: Códigos por Categoría (S001, V001, A001)

```
┌────────────────────────────────────────────────────────────────┐
│ PARTE 1: Códigos Relacionados con Categoría                   │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  FORMATO: S001, V001, A001                                    │
│  ✓ S = Solicitud, V = Ventas, A = Atención                   │
│                                                                │
│  VENTAJAS:                                                     │
│  ✅ Intuitivo (letra indica categoría)                       │
│  ✅ Organizado por categoría                                 │
│  ✅ Fácil buscar por tipo (V*)                               │
│                                                                │
│  DESVENTAJAS:                                                  │
│  ⚠️ Si cambias nombre de categoría, código queda obsoleto    │
│  ⚠️ Si mueves opción de categoría, código confunde           │
│  ⚠️ Reutilizar handler en otras categorías = confuso         │
│                                                                │
│  IDEAL PARA:                                                   │
│  → Menús estables                                             │
│  → Categorías fijas                                           │
│  → Prototipado rápido                                         │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### PARTE 2: Códigos Independientes (A001, B001, C001) 🏆 RECOMENDADA

```
┌────────────────────────────────────────────────────────────────┐
│ PARTE 2: Códigos Independientes del Menú                      │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  FORMATO: A001, B001, C001...Z001, AA01...ZZ99               │
│  ✓ Letra secuencial (NO relacionada con menú)                │
│                                                                │
│  VENTAJAS:                                                     │
│  ✅ TOTAL independencia del menú                             │
│  ✅ Cambiar nombre/categoría: NO afecta códigos              │
│  ✅ Reutilizar handler: NATURAL                              │
│  ✅ Estabilidad máxima                                       │
│  ✅ Escalabilidad (702 handlers A-ZZ)                        │
│                                                                │
│  DESVENTAJAS:                                                  │
│  ⚠️ Menos intuitivo (necesitas catálogo)                     │
│  ⚠️ Documentación crítica                                    │
│                                                                │
│  IDEAL PARA:                                                   │
│  → Menús que cambian frecuentemente                           │
│  → Handlers reutilizables                                     │
│  → Sistemas en producción long-term                           │
│  → Tu caso (chatbot WhatsApp) 🎯                             │
│                                                                │
│  CATÁLOGO: config_handlers.json                               │
│  {                                                             │
│    "A001": {                                                   │
│      "codigo": "A001",                                        │
│      "nombre": "Captura de Incidentes con Escalamiento",     │
│      "archivo": "handler_captura_incidente.py",              │
│      "clase": "HandlerCapturaIncidente",                     │
│      "activo": true,                                         │
│      "preguntas": 3,                                         │
│      "tags": ["tickets", "incidentes", "escalamiento"]       │
│    }                                                          │
│  }                                                            │
│                                                                │
│  INDEPENDENCIA:                                                │
│  ┌──────────────────────┬────────────────────────────────┐   │
│  │ Menú: "Incidente"    │ Código: "A001"                 │   │
│  │ (puede cambiar)      │ (NUNCA cambia)                 │   │
│  ├──────────────────────┼────────────────────────────────┤   │
│  │ Handler: "Captura    │ Archivo: handler_captura_      │   │
│  │ Incidente" (función) │ incidente.py (independiente)   │   │
│  └──────────────────────┴────────────────────────────────┘   │
│                                                                │
│  MOTOR: sistema_menu_modular.py                               │
│  1. Carga JSON al iniciar                                     │
│  2. Usuario selecciona "1.1 Incidente Técnico"                │
│  3. Consulta Dataverse → obtiene "A001"                       │
│  4. Busca "A001" en JSON → obtiene archivo Python             │
│  5. Carga dinámicamente handler_captura_incidente.py          │
│  6. Ejecuta el handler A001                                   │
│                                                                │
│  🏆 RECOMENDACIÓN FINAL: PARTE 2 (Códigos Independientes)26. ¿En qué más podemos ayudarte?"
```

---

## 🎯 RESUMEN: Cómo Funciona la Opción B (JSON)

```
┌────────────────────────────────────────────────────────────────┐
│ FLUJO COMPLETO PASO A PASO                                     │
└────────────────────────────────────────────────────────────────┘

1. INICIO DEL SISTEMA
   sistema_menu_modular.py se ejecuta
   │
   ├─→ Carga config_handlers.json
   │   └─→ Parsea JSON a diccionario Python
   │       └─→ {
   │             "S001": ConfigHandler(...),
   │             "V001": ConfigHandler(...),
   │             ...
   │           }
   │
   └─→ Obtiene token de Dataverse
       └─→ Listo para procesar mensajes

2. USUARIO ENVÍA MENSAJE
   Usuario escribe "1" en WhatsApp
   │
   └─→ Sistema muestra menú principal
       Usuario escribe "1" de nuevo → Selecciona categoría "Solicitud Ticket"
       │
       └─→ Sistema muestra submenú
           Usuario escribe "1" → Selecciona "1.1 Incidente Técnico"

3. CONSULTA DATAVERSE
   sistema_menu_modular.py consulta tabla cr321_chatbots
   │
   └─→ SELECT * FROM cr321_chatbots WHERE cr321_orden = 1
       │
       └─→ Resultado:
           {
             "cr321_elemento1": "Incidente Técnico",
             "cr321_handler1": "S001",           ← ESTE VALOR
             "cr321_grupo1": "{GUID-TI-GRUPO}"
           }

4. BUSCA EN JSON
   Sistema busca código "S001" en config_handlers
   │
   └─→ config_handlers["S001"]
       │
       └─→ Resultado:
           {
             "archivo": "handler_incidente_tecnico.py",
             "clase": "HandlerIncidenteTecnico",
             "activo": true,
             ...
           }

5. CARGA HANDLER DINÁMICAMENTE
   sistema_menu_modular.py usa importlib
   │
   ├─→ importlib.import_module("handlers.handler_incidente_tecnico")
   │   └─→ Importa el archivo Python
   │
   └─→ getattr(modulo, "HandlerIncidenteTecnico")
       └─→ Obtiene la clase
           │
           └─→ HandlerIncidenteTecnico(dataverse_url, headers)
               └─→ Instancia la clase

6. EJECUTA HANDLER
   handler.ejecutar(from_user, mensaje, grupo_id)
   │
   ├─→ get_preguntas() → ["¿Sistema?", "¿Cuántos usuarios?", "¿Caído?"]
   │
   ├─→ Hace las 3 preguntas al usuario
   │   └─→ Captura respuestas: {"¿Sistema?": "Ventas", "¿Usuarios?": "80", ...}
   │
   └─→ ejecutar_accion_final(from_user, respuestas, grupo_id)
       │
       ├─→ Analiza respuestas: 80 usuarios > 50 → Prioridad URGENTE
       │
       ├─→ Crea ticket en Dataverse
       │   └─→ ticket_id = 12345
       │
       ├─→ Notifica gerencia (porque es urgente)
       │
       └─→ Retorna: "🚨 Ticket #12345 creado. Prioridad: URGENTE"

7. RESPUESTA AL USUARIO
   Sistema envía mensaje final a WhatsApp
   │
   └─→ Usuario recibe:
       "🚨 Ticket #12345 creado.
        Prioridad: URGENTE
        Se notificó a gerencia de TI."
```

---

## ✅ VENTAJAS de la Opción B (JSON)

```
1. SIMPLICIDAD
   ✓ Un solo archivo JSON vs crear tabla nueva en Dataverse
   ✓ Fácil de entender y modificar

2. CONTROL DE VERSIONES (GIT)
   ✓ Cada cambio en JSON queda en Git history
   ✓ Puedes hacer rollback fácilmente
   ✓ Code review de cambios en config

3. PERFORMANCE
   ✓ Lectura local (archivo) vs API call (Dataverse)
   ✓ Más rápido
   ✓ No consume cuota de API

4. FLEXIBILIDAD
   ✓ Agregar metadata sin cambiar schema de tabla
   ✓ Campos personalizados por handler
   ✓ Fácil experimentar

5. DESARROLLO
   ✓ Cambias JSON localmente y pruebas
   ✓ No necesitas acceso a Dataverse para config
   ✓ Desarrollo más ágil

6. DOCUMENTACIÓN AUTO-CONTENIDA
   ✓ JSON tiene descripción, versión, notas
   ✓ Todo en un lugar
```

---

## 📊 COMPARACIÓN: Con vs Sin JSON

```
┌──────────────────────────┬─────────────────────────────────────────┐
│ SIN JSON (Antes)         │ CON JSON (Opción B)                     │
├──────────────────────────┼─────────────────────────────────────────┤
│ cr321_handler1:          │ cr321_handler1: "S001"                  │
│ "handler_incidente_te.." │                                         │
│                          │ JSON mapea:                             │
│                          │ "S001" → "handler_incidente_tecnico.py" │
│                          │                                         │
│ Cambiar archivo:         │ Cambiar archivo:                        │
│ → Actualizar tabla       │ → Actualizar JSON (sin tocar tabla)     │
│                          │                                         │
│ Metadata:                │ Metadata:                               │
│ → No hay                 │ → descripcion, preguntas, version,      │
│                          │   categoria, notas, etc.                │
│                          │                                         │
│ Desactivar handler:      │ Desactivar handler:                     │
│ → ¿Cómo?                 │ → "activo": false en JSON               │
│                          │                                         │
│ Testing A/B:             │ Testing A/B:                            │
│ → Difícil                │ → "S001A" vs "S001B"                    │
│                          │                                         │
│ Documentación:           │ Documentación:                          │
│ → Separada               │ → Integrada en JSON                     │
└──────────────────────────┴─────────────────────────────────────────┘
```

---

## 🎯 RESUMEN EJECUTIVO

```
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│  OPCIÓN B: Sistema con Códigos de Una Letra + JSON            │
│                                                                │
│  CÓDIGOS:                                                      │
│  S001, S002, S003 (Solicitudes)                               │
│  V001, V002, V003 (Ventas)                                    │
│  A001, A002 (Atención)                                        │
│  X999 (Default)                                               │
│                                                                │
│  CATÁLOGO: config_handlers.json                               │
│  {                                                             │
│    "S001": {                                                   │
│      "archivo": "handler_incidente_tecnico.py",               │
│      "clase": "HandlerIncidenteTecnico",                      │
│      "activo": true,                                          │
│      "preguntas": 3,                                          │
│      ...metadata adicional...                                 │
│    }                                                           │
│  }                                                             │
│                                                                │
│  MOTOR: sistema_menu_modular.py                               │
│  1. Carga JSON al iniciar                                     │
│  2. Usuario selecciona opción                                 │
│  3. Consulta Dataverse → obtiene "S001"                       │
│  4. Busca "S001" en JSON → obtiene archivo Python             │
│  5. Carga dinámicamente el archivo                            │
│  6. Ejecuta el handler                                        │
│                                                                │
│  VENTAJAS:                                                     │
│  ✅ Códigos cortos (4 caracteres)                            │
│  ✅ Total independencia elemento/código/archivo              │
│  ✅ Config en Git (version control)                          │
│  ✅ Sin tabla adicional en Dataverse                         │
│  ✅ Performance (lectura local)                              │
│  ✅ Metadata rica (descripción, versión, notas)             │
│  ✅ Fácil activar/desactivar handlers                        │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## ❓ Próximos Pasos

**¿Te quedó claro cómo funciona la Opción B con JSON?**

**¿Lista para implementar?** 🚀
