"""
DEMOSTRACIÓN DE SISTEMAS COMPLEMENTARIOS
=========================================

Tickets | Estados | Mensajes WhatsApp
"""

import sys
sys.path.insert(0, 'backend')

print("""
╔══════════════════════════════════════════════════════════════╗
║      🎫 SISTEMA DE TICKETS, ESTADOS Y MENSAJES              ║
╔══════════════════════════════════════════════════════════════╗
""")

# ═══════════════════════════════════════════════════════════════
# SISTEMA 1: ESTADOS
# ═══════════════════════════════════════════════════════════════

print("\n" + "=" * 60)
print("        🎯 SISTEMA 1: ESTADOS (cr321_estados)")
print("=" * 60)

print("""
📋 PROPÓSITO:
   Gestionar el ciclo de vida de tickets y conversaciones

📊 ESTRUCTURA:
   Tabla: cr321_estados
   Campos:
     • cr321_estadoid (GUID) - Primary Key
     • cr321_nombre (STRING) - Nombre del estado
     • cr321_descripcion (STRING) - Descripción
     • cr321_color (STRING) - Color para UI
     • cr321_orden (INT) - Orden de visualización

🔄 ESTADOS INICIALES (creados por init_dataverse.py):
""")

estados = [
    {"id": 1, "nombre": "NUEVO", "color": "#2196F3", "desc": "Ticket recién creado"},
    {"id": 2, "nombre": "EN_PROCESO", "color": "#FF9800", "desc": "Siendo atendido"},
    {"id": 3, "nombre": "ESPERANDO", "color": "#9C27B0", "desc": "Esperando respuesta del cliente"},
    {"id": 4, "nombre": "RESUELTO", "color": "#4CAF50", "desc": "Problema resuelto"},
    {"id": 5, "nombre": "CERRADO", "color": "#607D8B", "desc": "Ticket cerrado"},
    {"id": 6, "nombre": "CANCELADO", "color": "#F44336", "desc": "Ticket cancelado"}
]

for estado in estados:
    print(f"   {estado['id']}. {estado['nombre']:<15} {estado['color']:<10} → {estado['desc']}")

print("""
🚀 API ENDPOINTS:
   GET    /api/estados              # Listar todos los estados
   GET    /api/estados/<id>         # Obtener estado específico
   POST   /api/estados              # Crear nuevo estado
   PUT    /api/estados/<id>         # Actualizar estado
   DELETE /api/estados/<id>         # Eliminar estado

💡 EJEMPLO DE USO:
   GET /api/estados
   Response:
   {
     "estados": [
       {
         "id": "guid-123",
         "nombre": "NUEVO",
         "descripcion": "Ticket recién creado",
         "color": "#2196F3",
         "orden": 1
       },
       ...
     ]
   }

🔗 RELACIONES:
   cr321_ticket.cr321_estadoid → cr321_estados (N:1)
   └─ Cada ticket tiene un estado actual
""")

# ═══════════════════════════════════════════════════════════════
# SISTEMA 2: TICKETS
# ═══════════════════════════════════════════════════════════════

print("\n" + "=" * 60)
print("        🎫 SISTEMA 2: TICKETS (cr321_ticket)")
print("=" * 60)

print("""
📋 PROPÓSITO:
   Sistema completo de gestión de tickets de soporte/solicitudes

📊 ESTRUCTURA:
   Tabla: cr321_ticket
   Campos principales:
     • cr321_ticketid (GUID) - Primary Key
     • cr321_titulo (STRING) - Título del ticket
     • cr321_descripcion (TEXT) - Descripción detallada
     • cr321_prioridad (CHOICE) - Baja/Media/Alta/Urgente
     • cr321_tipo (CHOICE) - Soporte/Cotización/Info/Atención
     • cr321_fechacreacion (DATETIME) - Fecha de creación
     • cr321_fechaactualizacion (DATETIME) - Última actualización
   
   Relaciones (Lookups):
     • cr321_contactoid → cr321_contacto
     • cr321_grupoid → cr321_grupos
     • cr321_estadoid → cr321_estados
     • cr321_usuarioasignadoid → cr321_usuarios

🎯 PRIORIDADES:
   462410000 → Baja      🟢 No urgente
   462410001 → Media     🟡 Normal
   462410002 → Alta      🟠 Importante
   462410003 → Urgente   🔴 Crítico

📦 TIPOS DE TICKET:
   462410000 → Soporte         🛠️  Problemas técnicos
   462410001 → Cotización      💰 Solicitud de precio
   462410002 → Información     📄 Consultas generales
   462410003 → Atención Agente 👤 Requiere agente humano

🚀 API ENDPOINTS:
   GET    /api/tickets                    # Listar tickets
   GET    /api/tickets/<id>               # Ticket específico
   GET    /api/tickets?estado=NUEVO       # Filtrar por estado
   GET    /api/tickets?grupo=1            # Filtrar por grupo
   GET    /api/tickets?prioridad=Alta     # Filtrar por prioridad
   POST   /api/tickets                    # Crear ticket
   PUT    /api/tickets/<id>               # Actualizar ticket
   DELETE /api/tickets/<id>               # Eliminar ticket
   PATCH  /api/tickets/<id>/asignar       # Asignar a usuario
   PATCH  /api/tickets/<id>/estado        # Cambiar estado

💡 EJEMPLO DE CREACIÓN:
   POST /api/tickets
   {
     "titulo": "Problemas con la aplicación",
     "descripcion": "La app se cierra al abrir mensajes",
     "contacto_id": "guid-del-contacto",
     "grupo_id": "guid-del-grupo",
     "prioridad": "Alta",
     "tipo": "Soporte"
   }

🔄 FLUJO DE VIDA DE UN TICKET:
   
   1. NUEVO           → Cliente envía mensaje
   2. EN_PROCESO      → Agente comienza a atender
   3. ESPERANDO       → Se solicita info al cliente
   4. EN_PROCESO      → Cliente responde
   5. RESUELTO        → Se soluciona el problema
   6. CERRADO         → Se cierra el ticket

🔗 RELACIONES COMPLETAS:
   
   Ticket conecta con:
   ┌─────────────────────────────────────────┐
   │                Ticket                   │
   └─────────┬──────┬──────┬────────┬────────┘
             │      │      │        │
             ▼      ▼      ▼        ▼
         Contacto Grupo Estado  Usuario
          (Quién)  (Qué) (Cómo) (Quién atiende)
""")

# ═══════════════════════════════════════════════════════════════
# SISTEMA 3: MENSAJES WHATSAPP
# ═══════════════════════════════════════════════════════════════

print("\n" + "=" * 60)
print("     💬 SISTEMA 3: MENSAJES WHATSAPP (cr321_adatawp0)")
print("=" * 60)

print("""
📋 PROPÓSITO:
   Almacenar TODOS los mensajes de WhatsApp (entrantes y salientes)

📊 ESTRUCTURA:
   Tabla: cr321_adatawp0
   Campos principales:
     • cr321_adatawp0id (GUID) - Primary Key
     • cr321_name (STRING) - Resumen del mensaje
     • cr321_fromphone (STRING) - Teléfono origen
     • cr321_tophone (STRING) - Teléfono destino
     • cr321_text (TEXT) - Contenido del mensaje
     • cr321_messagetype (CHOICE) - Texto/Imagen/Audio/Video/Doc
     • cr321_direction (CHOICE) - Entrante/Saliente
     • cr321_status (CHOICE) - Enviado/Entregado/Leído/Error
     • cr321_timestamp (DATETIME) - Fecha/hora del mensaje
     • cr321_wamid (STRING) - WhatsApp Message ID
     • cr321_mediaid (STRING) - ID de media (si aplica)
     • cr321_mediaurl (STRING) - URL de media (si aplica)
   
   Relaciones:
     • cr321_contactoid → cr321_contacto
     • cr321_ticketid → cr321_ticket

📨 TIPOS DE MENSAJE:
   462410000 → Texto      📝 Mensaje de texto
   462410001 → Imagen     🖼️  Foto enviada/recibida
   462410002 → Audio      🎵 Nota de voz
   462410003 → Video      🎬 Video compartido
   462410004 → Documento  📄 PDF, Word, etc.

↔️  DIRECCIÓN:
   462410000 → Entrante   📥 Cliente → Sistema
   462410001 → Saliente   📤 Sistema → Cliente

📊 ESTADO DE ENTREGA:
   462410000 → Enviado    ✉️  Enviado al servidor WhatsApp
   462410001 → Entregado  ✅ Recibido por el cliente
   462410002 → Leído      👁️  Cliente abrió el mensaje
   462410003 → Error      ❌ Fallo en el envío

🚀 API ENDPOINTS:
   GET    /api/messages                        # Listar mensajes
   GET    /api/messages/<id>                   # Mensaje específico
   GET    /api/messages/conversation/<phone>   # Por conversación
   GET    /api/messages?desde=2024-01-01       # Filtrar por fecha
   POST   /api/messages/send                   # Enviar mensaje
   POST   /webhook                             # Recibir de WhatsApp

💡 EJEMPLO DE MENSAJE ENTRANTE (Webhook):
   POST /webhook
   {
     "entry": [{
       "changes": [{
         "value": {
           "messages": [{
             "from": "5491112345678",
             "text": { "body": "Hola, necesito ayuda" },
             "timestamp": "1638360000"
           }]
         }
       }]
     }]
   }

💡 EJEMPLO DE ENVIAR MENSAJE:
   POST /api/messages/send
   {
     "phone": "5491112345678",
     "message": "Hola! ¿En qué podemos ayudarte?"
   }

🔄 FLUJO COMPLETO DE MENSAJERÍA:

   ┌──────────────┐
   │  WhatsApp    │
   │   Cliente    │
   └───────┬──────┘
           │ Envía mensaje
           ▼
   ┌──────────────┐
   │   Webhook    │ ← Recibe notificación
   └───────┬──────┘
           │
           ▼
   ┌──────────────────────┐
   │  cr321_adatawp0      │ ← Guarda mensaje
   │  (direction=entrante)│
   └───────┬──────────────┘
           │
           ▼
   ┌──────────────────┐
   │ ¿Ticket existe?  │
   └────┬──────────┬──┘
        │No        │Sí
        ▼          ▼
   Crear ticket  Asociar mensaje
        │          │
        └────┬─────┘
             ▼
   ┌──────────────────┐
   │  Notificar       │
   │  Usuarios        │
   └──────────────────┘
             │
             ▼
   ┌──────────────────┐
   │  Agente responde │
   └──────────┬───────┘
             ▼
   ┌──────────────────────┐
   │  cr321_adatawp0      │ ← Guarda respuesta
   │  (direction=saliente)│
   └───────┬──────────────┘
           │
           ▼
   ┌──────────────┐
   │ WhatsApp API │ ← Envía mensaje
   └───────┬──────┘
           ▼
   ┌──────────────┐
   │  Cliente     │ ← Recibe mensaje
   └──────────────┘
""")

# ═══════════════════════════════════════════════════════════════
# INTEGRACIÓN DE LOS 3 SISTEMAS
# ═══════════════════════════════════════════════════════════════

print("\n" + "=" * 60)
print("          🔗 INTEGRACIÓN DE LOS 3 SISTEMAS")
print("=" * 60)

print("""
Los 3 sistemas trabajan juntos para gestionar conversaciones:

📱 MENSAJE → 🎫 TICKET → 🎯 ESTADO

Ejemplo de flujo completo:

1. 💬 Cliente envía: "Mi app no funciona"
   └─ Se crea registro en cr321_adatawp0
   └─ direction = ENTRANTE
   └─ messagetype = TEXTO

2. 🎫 Sistema crea ticket automático
   └─ cr321_ticket con titulo "Mi app no funciona"
   └─ prioridad = MEDIA (default)
   └─ tipo = SOPORTE
   └─ Se asocia al mensaje (cr321_ticketid)

3. 🎯 Ticket se crea con estado NUEVO
   └─ cr321_estadoid → "NUEVO"
   └─ Order: 1

4. 📁 Se asigna a grupo según menú
   └─ Si cliente seleccionó "3" → SOPORTE
   └─ cr321_grupoid → grupo de SOPORTE

5. 👥 Usuarios del grupo reciben notificación
   └─ Consulta cr321_usuariogrupo
   └─ Notifica usuarios con permiso en grupo SOPORTE

6. 👤 Agente atiende ticket
   └─ Estado cambia a EN_PROCESO
   └─ Se asigna: cr321_usuarioasignadoid

7. 💬 Agente responde al cliente
   └─ Nuevo registro en cr321_adatawp0
   └─ direction = SALIENTE
   └─ Envío vía WhatsApp Graph API

8. ✅ Se resuelve el problema
   └─ Estado cambia a RESUELTO
   └─ Timestamp de actualización

9. 🔒 Se cierra el ticket
   └─ Estado final: CERRADO
   └─ Historial completo guardado
""")

# ═══════════════════════════════════════════════════════════════
# ESTADÍSTICAS
# ═══════════════════════════════════════════════════════════════

print("\n" + "=" * 60)
print("                  📊 ESTADÍSTICAS")
print("=" * 60)

print("""
SISTEMA DE ESTADOS:
  • Tabla: cr321_estados
  • Registros iniciales: 6 estados
  • Endpoints API: 4 (GET, POST, PUT, DELETE)
  • Relaciones: 1 (con tickets)

SISTEMA DE TICKETS:
  • Tabla: cr321_ticket
  • Campos: 10 estándar + 4 lookups
  • Prioridades: 4 niveles
  • Tipos: 4 categorías
  • Endpoints API: 8+ endpoints
  • Relaciones: 4 tablas (contactos, grupos, estados, usuarios)

SISTEMA DE MENSAJES:
  • Tabla: cr321_adatawp0
  • Campos: 13 campos
  • Tipos soportados: 5 (texto, imagen, audio, video, doc)
  • Estados de entrega: 4 estados
  • Endpoints API: 5+ endpoints
  • Webhook: Recibe de WhatsApp en tiempo real
  • Relaciones: 2 (contactos, tickets)

TOTAL COMBINADO:
  📋 3 tablas principales
  📊 27+ campos combinados
  🔗 7 relaciones entre tablas
  🚀 17+ endpoints API
  📈 Procesamiento en tiempo real
""")

# ═══════════════════════════════════════════════════════════════
# CÓMO PROBAR
# ═══════════════════════════════════════════════════════════════

print("\n" + "=" * 60)
print("              🧪 CÓMO PROBAR LOS SISTEMAS")
print("=" * 60)

print("""
PASO 1: Crear tablas en Dataverse
   • cr321_estados (4 campos)
   • cr321_ticket (10 campos + 4 lookups)
   • cr321_adatawp0 (13 campos + 2 lookups)
   → Ver: docs/GUIA_COMPLETA_CREAR_TABLAS_DATAVERSE.md

PASO 2: Inicializar datos
   python init_dataverse.py
   → Crea 6 estados automáticamente

PASO 3: Iniciar backend
   python backend/back.py
   → Servidor en http://localhost:5000

PASO 4: Probar APIs individualmente

   Estados:
   curl http://localhost:5000/api/estados

   Tickets:
   curl http://localhost:5000/api/tickets

   Mensajes:
   curl http://localhost:5000/api/messages

PASO 5: Ejecutar tests automatizados
   python tests/test_backend.py
   python tests/test_sistema.py

PASO 6: Configurar Webhook de WhatsApp
   1. Ir a Meta for Developers
   2. Configurar webhook: https://tu-dominio.com/webhook
   3. Token de verificación: valor de VERIFY_TOKEN en .env
   4. Suscribirse a eventos: messages
""")

print("\n" + "=" * 60)
print("✅ Documentación completa de los 3 sistemas")
print("=" * 60 + "\n")

print("💡 Archivos de referencia:")
print("   • backend/api/estados.py")
print("   • backend/api/tickets.py")
print("   • backend/api/messages.py")
print("   • backend/api/webhook.py")
print("   • docs/GUIA_COMPLETA_CREAR_TABLAS_DATAVERSE.md")
print("   • docs/GUIA_SISTEMA_CHATBOT.md\n")
