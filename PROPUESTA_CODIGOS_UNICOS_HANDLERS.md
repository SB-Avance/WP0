# 🔢 OPCIÓN MEJORADA: Códigos Únicos para Handlers

## 🎯 Tu Propuesta

**En lugar de nombres descriptivos, usar códigos únicos:**

```
cr321_handler1: "handler_incidente_tecnico"  ❌ Nombre largo
                     ↓
cr321_handler1: "HDL001"                     ✅ Código único
```

---

## 🏗️ Diseño con Códigos Únicos

### Opción A: Sistema con Tabla de Mapeo (RECOMENDADO)

```
┌─────────────────────────────────────────────────────────────────┐
│ Tabla: cr321_chatbots (Configuración de Menú)                  │
├─────────────────────────────────────────────────────────────────┤
│ cr321_elemento1:  "Incidente Técnico"                           │
│ cr321_handler1:   "HDL001"              ← Código único          │
│ cr321_grupo1:     {GUID-TI}                                     │
└─────────────────────────────────────────────────────────────────┘

                                ↓ mapea a ↓

┌─────────────────────────────────────────────────────────────────┐
│ Tabla: cr321_handlers (Catálogo de Handlers)                   │
├──────────┬──────────────────────────────────┬───────────────────┤
│ Código   │ Nombre Archivo                   │ Descripción       │
├──────────┼──────────────────────────────────┼───────────────────┤
│ HDL001   │ handler_incidente_tecnico.py     │ Incidentes TI     │
│ HDL002   │ handler_solicitud_servicio.py    │ Solicitudes SS    │
│ HDL003   │ handler_cambio_rfc.py            │ Cambios RFC       │
│ HDL004   │ handler_cotizacion.py            │ Cotizaciones      │
│ HDL005   │ handler_catalogo_pdf.py          │ Enviar catálogo   │
│ HDL006   │ handler_seguimiento_pedido.py    │ Track pedidos     │
│ HDL007   │ handler_asignar_directo.py       │ Asignación simple │
│ HDL008   │ handler_urgencia_prioridad.py    │ Urgencias         │
│ HDL999   │ handler_default.py               │ Handler genérico  │
└──────────┴──────────────────────────────────┴───────────────────┘
```

### Opción B: Sistema con JSON Config (Más Simple)

```
┌─────────────────────────────────────────────────────────────────┐
│ Tabla: cr321_chatbots                                           │
├─────────────────────────────────────────────────────────────────┤
│ cr321_elemento1:  "Incidente Técnico"                           │
│ cr321_handler1:   "HDL001"              ← Código único          │
│ cr321_grupo1:     {GUID-TI}                                     │
└─────────────────────────────────────────────────────────────────┘

                                ↓ mapea a ↓

┌─────────────────────────────────────────────────────────────────┐
│ Archivo: handlers/config_handlers.json                          │
├─────────────────────────────────────────────────────────────────┤
│ {                                                               │
│   "HDL001": {                                                   │
│     "archivo": "handler_incidente_tecnico.py",                  │
│     "clase": "HandlerIncidenteTecnico",                         │
│     "descripcion": "Incidentes técnicos con escalamiento",      │
│     "activo": true                                              │
│   },                                                            │
│   "HDL002": {                                                   │
│     "archivo": "handler_solicitud_servicio.py",                 │
│     "clase": "HandlerSolicitudServicio",                        │
│     "descripcion": "Solicitudes de servicio estándar",          │
│     "activo": true                                              │
│   },                                                            │
│   ...                                                           │
│ }                                                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 Ejemplos de Códigos Únicos

### Sistemática de Códigos:

```
HDL = Handler
001 = Número secuencial

Formato: HDL### (3 dígitos)

Ejemplos:
HDL001 = Incidente Técnico
HDL002 = Solicitud Servicio
HDL003 = Cambio RFC
HDL004 = Cotización
HDL005 = Catálogo PDF
...
HDL999 = Handler por defecto
```

### Alternativas de Abreviaturas:

**Opción 1: HDL (Handler)**
```
HDL001, HDL002, HDL003...
✓ Simple
✓ Claro
```

**Opción 2: HND (Handler)**
```
HND001, HND002, HND003...
✓ Más corto
```

**Opción 3: Por Categoría**
```
SOL001 = Solicitud - Incidente Técnico
SOL002 = Solicitud - Servicio
SOL003 = Solicitud - Cambio

VTA001 = Ventas - Cotización
VTA002 = Ventas - Catálogo
VTA003 = Ventas - Seguimiento

ATC001 = Atención - Asignación Directa
ATC002 = Atención - Urgencia

✓ Código indica la categoría
✓ Más descriptivo
```

**Opción 4: Código Mixto**
```
H-SOL-001 = Handler - Solicitud - 001
H-VTA-001 = Handler - Ventas - 001
H-ATC-001 = Handler - Atención - 001

✓ Muy descriptivo
⚠️ Más largo
```

---

## 🎨 Visualización Completa: Opción A (Con Tabla)

### 1. Tabla `cr321_chatbots` (Menú):

```
┌─────┬─────────────────────────┬───────────┬──────────────┬─────────┐
│ ID  │ Elemento (visible)      │ Handler   │ Grupo        │ Orden   │
├─────┼─────────────────────────┼───────────┼──────────────┼─────────┤
│ 001 │ MENÚ PRINCIPAL          │ -         │ -            │ 0       │
│     ├─────────────────────────┼───────────┼──────────────┼─────────┤
│     │ cr321_elemento1:        │ HDL001    │ {GUID-TI}    │ 1       │
│     │ "Incidente Técnico"     │           │              │         │
│     ├─────────────────────────┼───────────┼──────────────┼─────────┤
│     │ cr321_elemento2:        │ HDL002    │ {GUID-SD}    │ 2       │
│     │ "Solicitud Servicio"    │           │              │         │
│     ├─────────────────────────┼───────────┼──────────────┼─────────┤
│     │ cr321_elemento3:        │ HDL003    │ {GUID-CAB}   │ 3       │
│     │ "Cambio Programado"     │           │              │         │
└─────┴─────────────────────────┴───────────┴──────────────┴─────────┘

┌─────┬─────────────────────────┬───────────┬──────────────┬─────────┐
│ 002 │ Ventas                  │ -         │ -            │ 2       │
│     ├─────────────────────────┼───────────┼──────────────┼─────────┤
│     │ cr321_elemento1:        │ HDL004    │ {GUID-VEN}   │ 1       │
│     │ "Solicitar Cotización"  │           │              │         │
│     ├─────────────────────────┼───────────┼──────────────┼─────────┤
│     │ cr321_elemento2:        │ HDL005    │ -            │ 2       │
│     │ "Ver Catálogo PDF"      │           │              │         │
│     ├─────────────────────────┼───────────┼──────────────┼─────────┤
│     │ cr321_elemento3:        │ HDL006    │ {GUID-VEN}   │ 3       │
│     │ "Seguimiento Pedido"    │           │              │         │
└─────┴─────────────────────────┴───────────┴──────────────┴─────────┘
```

### 2. Tabla `cr321_handlers` (Catálogo):

```
┌───────────┬────────────────────────────────────┬──────────────────────────────┬────────┐
│ Código    │ Archivo Handler                    │ Descripción                  │ Activo │
├───────────┼────────────────────────────────────┼──────────────────────────────┼────────┤
│ HDL001    │ handler_incidente_tecnico.py       │ Incidentes TI con            │ ✓      │
│           │                                    │ escalamiento y severidad     │        │
├───────────┼────────────────────────────────────┼──────────────────────────────┼────────┤
│ HDL002    │ handler_solicitud_servicio.py      │ Solicitudes estándar         │ ✓      │
│           │                                    │ con 2 preguntas              │        │
├───────────┼────────────────────────────────────┼──────────────────────────────┼────────┤
│ HDL003    │ handler_cambio_rfc.py              │ Cambios con aprobación       │ ✓      │
│           │                                    │ y notificación CAB           │        │
├───────────┼────────────────────────────────────┼──────────────────────────────┼────────┤
│ HDL004    │ handler_cotizacion.py              │ Cotizaciones con cálculo     │ ✓      │
│           │                                    │ de precios y PDF             │        │
├───────────┼────────────────────────────────────┼──────────────────────────────┼────────┤
│ HDL005    │ handler_catalogo_pdf.py            │ Envía catálogo, 0 preguntas  │ ✓      │
├───────────┼────────────────────────────────────┼──────────────────────────────┼────────┤
│ HDL006    │ handler_seguimiento_pedido.py      │ Consulta ERP y muestra       │ ✓      │
│           │                                    │ estado de pedido             │        │
├───────────┼────────────────────────────────────┼──────────────────────────────┼────────┤
│ HDL007    │ handler_asignar_directo.py         │ Asigna sin preguntas         │ ✓      │
├───────────┼────────────────────────────────────┼──────────────────────────────┼────────┤
│ HDL008    │ handler_urgencia_prioridad.py      │ Escalamiento urgente con SMS │ ✓      │
├───────────┼────────────────────────────────────┼──────────────────────────────┼────────┤
│ HDL999    │ handler_default.py                 │ Handler genérico por defecto │ ✓      │
└───────────┴────────────────────────────────────┴──────────────────────────────┴────────┘
```

### 3. Código Python:

```python
class SistemaMenuModular:
    
    def __init__(self):
        self.catalogo_handlers = self.cargar_catalogo_handlers()
    
    def cargar_catalogo_handlers(self):
        """Carga catálogo desde tabla cr321_handlers"""
        response = requests.get(
            f"{DATAVERSE_URL}/cr321_handlers",
            headers=self.headers
        )
        
        catalogo = {}
        for handler in response.json()['value']:
            codigo = handler['cr321_codigo']      # "HDL001"
            archivo = handler['cr321_archivo']    # "handler_incidente_tecnico.py"
            activo = handler['cr321_activo']      # true/false
            
            if activo:
                catalogo[codigo] = archivo
        
        return catalogo
    
    def procesar_mensaje(self, from_user, texto):
        # 1. Usuario selecciona "1.1"
        
        # 2. Obtener configuración
        chatbot = self.obtener_chatbot_principal()
        codigo_handler = chatbot['cr321_handler1']  # "HDL001"
        
        # 3. Buscar en catálogo
        nombre_archivo = self.catalogo_handlers.get(codigo_handler, "handler_default.py")
        
        # 4. Cargar handler
        handler = self.cargar_handler_dinamico(nombre_archivo)
        
        # 5. Ejecutar
        handler.ejecutar()
```

---

## 🎨 Visualización: Opción B (Con JSON)

### 1. Tabla `cr321_chatbots` (igual que antes):

```
cr321_elemento1: "Incidente Técnico"
cr321_handler1: "HDL001"
cr321_grupo1: {GUID}
```

### 2. Archivo `handlers/config_handlers.json`:

```json
{
  "HDL001": {
    "archivo": "handler_incidente_tecnico.py",
    "clase": "HandlerIncidenteTecnico",
    "descripcion": "Incidentes técnicos con escalamiento automático",
    "activo": true,
    "version": "1.0.0",
    "categoria": "Solicitud Ticket",
    "preguntas_esperadas": 3,
    "requiere_grupo": true
  },
  "HDL002": {
    "archivo": "handler_solicitud_servicio.py",
    "clase": "HandlerSolicitudServicio",
    "descripcion": "Solicitudes de servicio estándar",
    "activo": true,
    "version": "1.0.0",
    "categoria": "Solicitud Ticket",
    "preguntas_esperadas": 2,
    "requiere_grupo": true
  },
  "HDL003": {
    "archivo": "handler_cambio_rfc.py",
    "clase": "HandlerCambioRFC",
    "descripcion": "Cambios con proceso RFC y aprobación CAB",
    "activo": true,
    "version": "2.1.0",
    "categoria": "Solicitud Ticket",
    "preguntas_esperadas": 4,
    "requiere_grupo": true
  },
  "HDL004": {
    "archivo": "handler_cotizacion.py",
    "clase": "HandlerCotizacion",
    "descripcion": "Cotizaciones con cálculo automático y PDF",
    "activo": true,
    "version": "1.5.0",
    "categoria": "Ventas",
    "preguntas_esperadas": 2,
    "requiere_grupo": true,
    "genera_pdf": true
  },
  "HDL005": {
    "archivo": "handler_catalogo_pdf.py",
    "clase": "HandlerCatalogoPDF",
    "descripcion": "Envía catálogo en PDF, sin preguntas",
    "activo": true,
    "version": "1.0.0",
    "categoria": "Ventas",
    "preguntas_esperadas": 0,
    "requiere_grupo": false,
    "genera_pdf": false,
    "envia_archivo": true
  },
  "HDL006": {
    "archivo": "handler_seguimiento_pedido.py",
    "clase": "HandlerSeguimientoPedido",
    "descripcion": "Consulta estado de pedido en ERP",
    "activo": true,
    "version": "1.2.0",
    "categoria": "Ventas",
    "preguntas_esperadas": 1,
    "requiere_grupo": false,
    "integra_con": "ERP"
  },
  "HDL007": {
    "archivo": "handler_asignar_directo.py",
    "clase": "HandlerAsignarDirecto",
    "descripcion": "Asigna directamente sin hacer preguntas",
    "activo": true,
    "version": "1.0.0",
    "categoria": "Solicitar Atención",
    "preguntas_esperadas": 0,
    "requiere_grupo": true
  },
  "HDL008": {
    "archivo": "handler_urgencia_prioridad.py",
    "clase": "HandlerUrgenciaPrioridad",
    "descripcion": "Manejo de urgencias con notificación SMS",
    "activo": true,
    "version": "1.3.0",
    "categoria": "Solicitar Atención",
    "preguntas_esperadas": 1,
    "requiere_grupo": true,
    "envia_sms": true,
    "notifica_gerencia": true
  },
  "HDL999": {
    "archivo": "handler_default.py",
    "clase": "HandlerDefault",
    "descripcion": "Handler genérico por defecto",
    "activo": true,
    "version": "1.0.0",
    "categoria": "Sistema",
    "preguntas_esperadas": 0,
    "requiere_grupo": true
  }
}
```

### 3. Código Python:

```python
import json
from pathlib import Path

class SistemaMenuModular:
    
    def __init__(self):
        self.config_handlers = self.cargar_config_json()
    
    def cargar_config_json(self):
        """Carga configuración desde JSON"""
        config_path = Path(__file__).parent / "handlers" / "config_handlers.json"
        
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def procesar_mensaje(self, from_user, texto):
        # 1. Usuario selecciona "1.1"
        
        # 2. Obtener configuración
        chatbot = self.obtener_chatbot_principal()
        codigo_handler = chatbot['cr321_handler1']  # "HDL001"
        
        # 3. Buscar en config JSON
        if codigo_handler not in self.config_handlers:
            codigo_handler = "HDL999"  # Fallback a default
        
        config = self.config_handlers[codigo_handler]
        
        # 4. Verificar si está activo
        if not config.get('activo', False):
            return "Handler no disponible temporalmente"
        
        # 5. Cargar handler
        nombre_archivo = config['archivo']
        handler = self.cargar_handler_dinamico(nombre_archivo)
        
        # 6. Ejecutar
        handler.ejecutar()
```

---

## ✅ Ventajas del Sistema con Códigos

```
1. DESACOPLAMIENTO TOTAL
   ✅ Código (HDL001) es independiente del nombre del elemento
   ✅ Código es independiente del nombre del archivo
   ✅ Puedes cambiar cualquiera sin afectar los demás

2. ESTABILIDAD
   ✅ Código HDL001 nunca cambia
   ✅ Referencias estables en la tabla
   ✅ No se rompen links

3. FÁCIL MANTENIMIENTO
   ✅ Cambiar nombre de archivo → Solo actualizar catálogo
   ✅ Cambiar elemento → Solo actualizar cr321_elemento1
   ✅ Reasignar handler → Solo cambiar HDL001 → HDL002

4. REUTILIZACIÓN
   ✅ Múltiples opciones pueden usar HDL001
   ✅ Fácil duplicar configuraciones

5. VERSIONAMIENTO
   ✅ Puedes tener HDL001 (v1) y HDL001B (v2) para testing
   ✅ Rollback fácil cambiando código

6. AUDITORÍA
   ✅ Historial claro de qué código usaba cada opción
   ✅ Trazabilidad perfecta

7. DOCUMENTACIÓN
   ✅ Código corto y fácil de recordar
   ✅ Fácil buscar "HDL001" en logs
```

---

## 🆚 Comparación: Con vs Sin Códigos

```
┌───────────────────────┬────────────────────────────┬──────────────────────┐
│ Característica        │ Sin Códigos                │ Con Códigos          │
├───────────────────────┼────────────────────────────┼──────────────────────┤
│ Campo handler         │ "handler_incidente_tec.."  │ "HDL001"             │
│ Largo del valor       │ 30-50 caracteres           │ 6 caracteres         │
│ Legibilidad en tabla  │ ⚠️ Texto largo             │ ✅ Código corto      │
│ Cambiar archivo       │ Actualizar campo en tabla  │ Actualizar catálogo  │
│ Cambiar elemento      │ ✅ Independiente           │ ✅ Independiente     │
│ Reutilizar handler    │ ✅ Copiar nombre           │ ✅ Copiar código     │
│ Buscar en logs        │ ⚠️ Nombre largo            │ ✅ "HDL001"          │
│ Documentar            │ ⚠️ Nombres descriptivos    │ ✅ Código + tabla    │
│ Testing A/B           │ ⚠️ Difícil                 │ ✅ HDL001A, HDL001B  │
│ Versionamiento        │ ⚠️ En nombre archivo       │ ✅ En catálogo       │
│ Complejidad sistem    │ ✅ Simple                  │ ⚠️ +1 tabla/JSON     │
│ Tiempo setup inicial  │ ✅ Rápido                  │ ⚠️ +1 hora config    │
└───────────────────────┴────────────────────────────┴──────────────────────┘
```

---

## 🎯 Comparación: Opción A (Tabla) vs Opción B (JSON)

```
┌───────────────────────┬────────────────────────────┬──────────────────────┐
│ Característica        │ OPCIÓN A: Tabla Dataverse  │ OPCIÓN B: JSON       │
├───────────────────────┼────────────────────────────┼──────────────────────┤
│ Catálogo handlers     │ Tabla cr321_handlers       │ config_handlers.json │
│ Actualizar catálogo   │ Power Apps / API           │ Editar archivo JSON  │
│ Sin deployment        │ ✅ Sí                      │ ⚠️ No (re-deploy)    │
│ Version control       │ ⚠️ En Dataverse            │ ✅ Git                │
│ Fácil para no-devs    │ ✅ Interfaz visual         │ ⚠️ Editar JSON       │
│ Backup automático     │ ✅ Dataverse backups       │ ⚠️ Git backups       │
│ Búsquedas/reportes    │ ✅ Power BI queries        │ ⚠️ Parsear JSON      │
│ Auditoría nativa      │ ✅ Dataverse audit log     │ ⚠️ Git history       │
│ Permisos granulares   │ ✅ Roles Dataverse         │ ⚠️ File permissions  │
│ Performance           │ ⚠️ API call                │ ✅ Lectura local     │
│ Complejidad           │ ⚠️ +1 tabla                │ ✅ Solo JSON         │
│ Mejor para            │ Empresas, múltiples users  │ Equipos dev, rápido  │
└───────────────────────┴────────────────────────────┴──────────────────────┘
```

---

## 💡 Recomendación

### Para Tu Caso: **OPCIÓN B (JSON)** 🏆

**Motivos:**
1. ✅ **Más simple** - Un archivo JSON vs crear tabla nueva
2. ✅ **Control de versiones** - Git trackea cambios en config_handlers.json
3. ✅ **Desarrollo rápido** - No necesitas API calls para leer catálogo
4. ✅ **Performance** - Lectura local vs llamada a Dataverse
5. ✅ **Flexibilidad** - Puedes agregar metadata sin cambiar schema

**Estructura de Códigos Recomendada:**

```
SOL001 = Solicitud - Incidente Técnico
SOL002 = Solicitud - Servicio Estándar
SOL003 = Solicitud - Cambio RFC

VTA001 = Ventas - Cotización
VTA002 = Ventas - Catálogo PDF
VTA003 = Ventas - Seguimiento

ATC001 = Atención - Asignación Directa
ATC002 = Atención - Urgencia

SYS999 = Sistema - Handler por defecto
```

✅ **Códigos descriptivos** (3 letras + 3 dígitos)
✅ **Fáciles de entender** (SOL = Solicitud, VTA = Ventas)
✅ **Espacio para crecer** (SOL001-SOL999)

---

## 📋 Estructura Final Propuesta

```
C:\VS\BIN\
├── sistema_menu_modular.py           ← Motor principal
├── handlers/
│   ├── config_handlers.json           ← Catálogo de handlers con códigos
│   ├── base_handler.py
│   ├── handler_incidente_tecnico.py
│   ├── handler_solicitud_servicio.py
│   ├── handler_cambio_rfc.py
│   ├── handler_cotizacion.py
│   ├── handler_catalogo_pdf.py
│   ├── handler_seguimiento_pedido.py
│   ├── handler_asignar_directo.py
│   ├── handler_urgencia_prioridad.py
│   └── handler_default.py

Dataverse:
├── cr321_chatbots
│   ├── cr321_elemento1: "Incidente Técnico"
│   ├── cr321_handler1: "SOL001"    ← Código único
│   └── cr321_grupo1: {GUID}
```

---

## 📝 Ejemplo de config_handlers.json Completo

```json
{
  "SOL001": {
    "codigo": "SOL001",
    "nombre": "Incidente Técnico",
    "archivo": "handler_incidente_tecnico.py",
    "clase": "HandlerIncidenteTecnico",
    "descripcion": "Manejo de incidentes con escalamiento",
    "activo": true,
    "categoria": "Solicitud Ticket",
    "preguntas": 3
  },
  "SOL002": {
    "codigo": "SOL002",
    "nombre": "Solicitud Servicio",
    "archivo": "handler_solicitud_servicio.py",
    "clase": "HandlerSolicitudServicio",
    "descripcion": "Solicitudes de servicio estándar",
    "activo": true,
    "categoria": "Solicitud Ticket",
    "preguntas": 2
  },
  "VTA001": {
    "codigo": "VTA001",
    "nombre": "Cotización",
    "archivo": "handler_cotizacion.py",
    "clase": "HandlerCotizacion",
    "descripcion": "Genera cotizaciones con PDF",
    "activo": true,
    "categoria": "Ventas",
    "preguntas": 2,
    "genera_pdf": true
  },
  "VTA002": {
    "codigo": "VTA002",
    "nombre": "Catálogo PDF",
    "archivo": "handler_catalogo_pdf.py",
    "clase": "HandlerCatalogoPDF",
    "descripcion": "Envía catálogo, sin preguntas",
    "activo": true,
    "categoria": "Ventas",
    "preguntas": 0,
    "envia_archivo": true
  },
  "SYS999": {
    "codigo": "SYS999",
    "nombre": "Default",
    "archivo": "handler_default.py",
    "clase": "HandlerDefault",
    "descripcion": "Handler por defecto",
    "activo": true,
    "categoria": "Sistema",
    "preguntas": 0
  }
}
```

---

## ✅ Resumen Ejecutivo

```
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│  SISTEMA CON CÓDIGOS ÚNICOS:                                   │
│                                                                │
│  Tabla cr321_chatbots:                                         │
│  ├── cr321_elemento1: "Incidente Técnico"   (texto visible)   │
│  ├── cr321_handler1:  "SOL001"               (código único)    │
│  └── cr321_grupo1:    {GUID}                 (grupo)           │
│                                                                │
│  Archivo config_handlers.json:                                 │
│  └── "SOL001" mapea a "handler_incidente_tecnico.py"          │
│                                                                │
│  VENTAJAS:                                                     │
│  ✅ Elemento y handler TOTALMENTE independientes              │
│  ✅ Cambias texto sin tocar código                            │
│  ✅ Cambias archivo handler sin tocar tabla                   │
│  ✅ Código corto (6 chars vs 30+ chars)                       │
│  ✅ Fácil auditoría y búsqueda en logs                        │
│  ✅ Testing A/B con códigos alternativos                      │
│                                                                │
│  RECOMENDACIÓN:                                                │
│  🏆 OPCIÓN B: JSON (más simple, Git friendly)                 │
│  📝 Códigos: SOL001, VTA001, ATC001, SYS999                   │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## ❓ Preguntas para Ti

**1. ¿Te gusta el sistema con códigos únicos?**
   - [ ] SÍ, usar códigos (SOL001, VTA001...)
   - [ ] NO, preferir nombres descriptivos

**2. ¿Qué opción para el catálogo?**
   - [ ] OPCIÓN A: Tabla en Dataverse (cr321_handlers)
   - [ ] OPCIÓN B: JSON (config_handlers.json) ⭐ RECOMENDADA

**3. ¿Qué formato de código prefieres?**
   - [ ] HDL001, HDL002... (genérico)
   - [ ] SOL001, VTA001, ATC001... (descriptivo) ⭐ RECOMENDADA
   - [ ] H-SOL-001, H-VTA-001 (muy descriptivo)
   - [ ] Otro: __________

**4. ¿Lista para implementar?**
   - [ ] SÍ, comenzar ahora
   - [ ] Necesito ver más detalles de: __________

---

**Esperando tu respuesta** 🚀
