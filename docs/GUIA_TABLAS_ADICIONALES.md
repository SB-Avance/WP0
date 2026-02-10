# 📋 Guía: Tablas del Sistema WhatsApp CRM

## 🎯 Objetivo
Documentación de las tablas en Dataverse para el sistema de chatbot WhatsApp.

---

## 🗂️ Tablas del Sistema

### Tabla: cr321_chatbot

**Información básica:**
```
Nombre para mostrar: Chatbot
Nombre plural: Chatbots  
Nombre: cr321_chatbot
Descripción: Gestión de chatbots de WhatsApp
```

**Campos a crear:**

| Campo | Tipo | Longitud | ¿Obligatorio? | Descripción |
|-------|------|----------|---------------|-------------|
| cr321_nombre | Texto | 100 | ✅ Sí | Nombre del Bot (campo principal) |
| cr321_tipo | Conjunto de opciones | - | ❌ No | Tipo de Bot |
| cr321_config | Texto multilínea | 100000 | ❌ No | Configuración JSON |
| cr321_activo | Sí/No | - | ❌ No | Activo |

**Opciones para cr321_tipo:**
```
Etiqueta: FlowBot         Valor: 462410000
Etiqueta: Simple          Valor: 462410001
Etiqueta: AI Assistant    Valor: 462410002
```

**Valores predeterminados:**
- cr321_tipo: 462410000 (FlowBot)
- cr321_activo: Sí (true)

---

### Tabla: cr321_flows

**Información básica:**
```
Nombre para mostrar: Flow
Nombre plural: Flows
Nombre: cr321_flow
Descripción: Definición de flujos para chatbots
```

**Campos a crear:**

| Campo | Tipo | Longitud/Relación | ¿Obligatorio? | Descripción |
|-------|------|-------------------|---------------|-------------|
| cr321_nombre | Texto | 100 | ✅ Sí | Nombre del Flujo |
| cr321_chatbotid | Búsqueda | → cr321_chatbot | ✅ Sí | Chatbot asociado |
| cr321_nodos | Texto multilínea | 100000 | ❌ No | Nodos en JSON |
| cr321_edges | Texto multilínea | 100000 | ❌ No | Conexiones en JSON |
| cr321_version | Número entero | - | ❌ No | Versión |

**Campo de búsqueda cr321_chatbotid:**
- Tipo: Búsqueda
- Tabla relacionada: cr321_chatbot
- Relación: Muchos a uno (N:1)

**Valores predeterminados:**
- cr321_version: 1

---

### Tabla: cr321_automatizaciones

**Información básica**:
```
Nombre para mostrar: Automatización
Nombre plural: Automatizaciones
Nombre: cr321_automatizaciones
Descripción: Reglas de automatización
```

**Campos a crear:**

| Campo | Tipo | Longitud | ¿Obligatorio? | Descripción |
|-------|------|----------|---------------|-------------|
| cr321_nombre | Texto | 100 | ✅ Sí | Nombre |
| cr321_trigger | Conjunto de opciones | - | ❌ No | Disparador |
| cr321_condiciones | Texto multilínea | 10000 | ❌ No | Condiciones JSON |
| cr321_acciones | Texto multilínea | 10000 | ❌ No | Acciones JSON |
| cr321_activo | Sí/No | - | ❌ No | Activa |

**Opciones para cr321_trigger:**
```
Etiqueta: Mensaje Recibido      Valor: 462410000
Etiqueta: Palabra Clave         Valor: 462410001
Etiqueta: Horario               Valor: 462410002
Etiqueta: Evento de Sistema     Valor: 462410003
```

**Valores predeterminados:**
- cr321_activo: Sí (true)

---

### Tabla: cr321_template

**Información básica:**
```
Nombre para mostrar: Template
Nombre plural: Templates
Nombre: cr321_template
Descripción: Plantillas de mensajes de WhatsApp
```

**Campos a crear:**

| Campo | Tipo | Longitud | ¿Obligatorio? | Descripción |
|-------|------|----------|---------------|-------------|
| cr321_nombre | Texto | 100 | ✅ Sí | Nombre |
| cr321_contenido | Texto multilínea | 5000 | ✅ Sí | Contenido |
| cr321_categoria | Conjunto de opciones | - | ❌ No | Categoría |
| cr321_idioma | Texto | 10 | ❌ No | Idioma |
| cr321_aprobado | Sí/No | - | ❌ No | Aprobada por Meta |

**Opciones para cr321_categoria:**
```
Etiqueta: Marketing    Valor: 462410000
Etiqueta: Servicio     Valor: 462410001
Etiqueta: Ventas       Valor: 462410002
Etiqueta: Soporte      Valor: 462410003
```

**Valores predeterminados:**
- cr321_idioma: es
- cr321_aprobado: No (false)

---

### Tabla: cr321_cuentadewhatsapp

**Información básica:**
```
Nombre para mostrar: Cuenta de WhatsApp
Nombre plural: Cuentas WhatsApp
Nombre: cr321_cuentadewhatsapp
Descripción: Conexiones de WhatsApp Business
```

**Campos a crear:**

| Campo | Tipo | Longitud | ¿Obligatorio? | Descripción |
|-------|------|----------|---------------|-------------|
| cr321_nombre | Texto | 100 | ✅ Sí | Nombre |
| cr321_phonenumberid | Texto | 50 | ✅ Sí | Phone Number ID |
| cr321_accesstoken | Texto | 500 | ✅ Sí | Access Token |
| cr321_verifytoken | Texto | 100 | ❌ No | Verify Token |
| cr321_activo | Sí/No | - | ❌ No | Activa |

**Valores predeterminados:**
- cr321_activo: Sí (true)

---

## 📝 Notas Importantes

### Campos de Texto Multilínea
- Tipo: **Texto multilínea**
- Longitud: 10000 o 100000 según necesidad
- Formato: Texto plano
- Uso: Configuraciones JSON, contenido extenso

### Campos Booleanos (Sí/No)
- **cr321_activo**: Predeterminado **Sí**
- **cr321_aprobado**: Predeterminado **No**

### Campos de Búsqueda (Lookup)
- Crean relaciones entre tablas
- Especificar tabla relacionada
- Tipo de relación: Muchos a uno (N:1) es el más común

---

## 🔗 Orden de Creación

**Orden recomendado** (de independientes a dependientes):

1. ✅ cr321_usuarios
2. ✅ cr321_grupos  
3. ✅ cr321_estados
4. ✅ cr321_contacto
5. ✅ cr321_cuentadewhatsapp
6. ✅ cr321_chatbot
7. ✅ cr321_automatizaciones
8. ✅ cr321_template
9. ✅ cr321_usuariogrupo (depende de usuarios y grupos)
10. ✅ cr321_flows (depende de chatbot)
11. ✅ cr321_ticket (depende de grupos, estados, contacto)
12. ✅ cr321_adatawp0

---

## 💡 Propósito de Cada Tabla

| Tabla | Propósito |
|-------|-----------|
| **cr321_adatawp0** | Mensajes WhatsApp (entrantes/salientes) |
| **cr321_usuarios** | Usuarios con roles (Admin/Usuario) |
| **cr321_grupos** | Categorías de atención |
| **cr321_estados** | Estados de tickets |
| **cr321_usuariogrupo** | Asignación usuarios-grupos |
| **cr321_contacto** | Datos de contactos |
| **cr321_ticket** | Tickets de soporte |
| **cr321_chatbot** | Configuración de bots |
| **cr321_flows** | Flujos visuales de conversación |
| **cr321_automatizaciones** | Reglas automáticas |
| **cr321_template** | Plantillas aprobadas |
| **cr321_cuentadewhatsapp** | Conexiones WhatsApp múltiples |

---

## 🎯 Verificación Final

**12 tablas del sistema:**

```
✅ cr321_adatawp0
✅ cr321_usuarios
✅ cr321_grupos
✅ cr321_estados
✅ cr321_ticket
✅ cr321_contacto
✅ cr321_usuariogrupo
✅ cr321_chatbot
✅ cr321_flows
✅ cr321_automatizaciones
✅ cr321_template
✅ cr321_cuentadewhatsapp
```

---

## ✅ Resumen

**Tiempo estimado:** 60-90 minutos

**Consejo Pro:** Crea primero tablas independientes, luego las dependientes.

---

**Última actualización:** Febrero 2026
