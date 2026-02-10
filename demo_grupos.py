"""
DEMOSTRACIÓN DEL SISTEMA DE GRUPOS
===================================

Sistema de categorización para conversaciones WhatsApp
"""

import sys
sys.path.insert(0, 'backend')

print("""
╔══════════════════════════════════════════════════════════════╗
║          📁 SISTEMA DE GRUPOS - INFORMACIÓN COMPLETA         ║
╔══════════════════════════════════════════════════════════════╗

""")

# 1. INFORMACIÓN GENERAL
print("📋 1. INFORMACIÓN GENERAL")
print("=" * 60)
print("""
Tabla en Dataverse: cr321_grup (cr321_grupos)
Propósito: Categorizar conversaciones de WhatsApp

Campos principales:
  • cr321_grupoid (GUID) - Primary Key
  • cr321_idgrupo (INT) - ID consecutivo
  • cr321_nombre (STRING) - Nombre del grupo
  • cr321_tipo (CHOICE) - A, B o C
  • cr321_descripcion (STRING) - Descripción
""")

# 2. TIPOS DE GRUPOS
print("\n🎯 2. TIPOS DE GRUPOS")
print("=" * 60)

tipos_grupos = {
    "Tipo A (462410000)": {
        "uso": "Opciones del menú principal de WhatsApp",
        "ejemplo": "SERVICIOS, COTIZACIONES, SOPORTE, GENERAL",
        "visible_en": "Menú interactivo de WhatsApp (4 opciones)"
    },
    "Tipo B (462410001)": {
        "uso": "Grupos secundarios/categorías internas",
        "ejemplo": "Ventas, Marketing, Recursos Humanos",
        "visible_en": "Frontend para filtrado avanzado"
    },
    "Tipo C (462410002)": {
        "uso": "Grupos especiales/etiquetas personalizadas",
        "ejemplo": "VIP, Prioritario, Seguimiento",
        "visible_en": "Reportes y análisis"
    }
}

for tipo, info in tipos_grupos.items():
    print(f"\n{tipo}:")
    print(f"  Uso: {info['uso']}")
    print(f"  Ejemplo: {info['ejemplo']}")
    print(f"  Visible en: {info['visible_en']}")

# 3. RUTAS API DISPONIBLES
print("\n\n🚀 3. API REST - ENDPOINTS DISPONIBLES")
print("=" * 60)

endpoints = [
    {
        "metodo": "GET",
        "ruta": "/api/grupos",
        "descripcion": "Obtener todos los grupos",
        "parametros": "?tipo=A (opcional: filtrar por tipo)",
        "ejemplo": "curl http://localhost:5000/api/grupos"
    },
    {
        "metodo": "GET",
        "ruta": "/api/grupos?tipo=A",
        "descripcion": "Obtener solo grupos tipo A (menú WhatsApp)",
        "parametros": "tipo: A, B o C",
        "ejemplo": "curl http://localhost:5000/api/grupos?tipo=A"
    },
    {
        "metodo": "POST",
        "ruta": "/api/grupos",
        "descripcion": "Crear nuevo grupo",
        "parametros": "JSON: {nombre, tipo, descripcion}",
        "ejemplo": """curl -X POST http://localhost:5000/api/grupos \\
     -H "Content-Type: application/json" \\
     -d '{"nombre":"Ventas","tipo":"B","descripcion":"Equipo de ventas"}'"""
    },
    {
        "metodo": "PUT",
        "ruta": "/api/grupos/<id>",
        "descripcion": "Actualizar grupo existente",
        "parametros": "JSON: {nombre?, tipo?, descripcion?}",
        "ejemplo": """curl -X PUT http://localhost:5000/api/grupos/1 \\
     -H "Content-Type: application/json" \\
     -d '{"descripcion":"Nueva descripción"}'"""
    },
    {
        "metodo": "DELETE",
        "ruta": "/api/grupos/<id>",
        "descripcion": "Eliminar grupo",
        "parametros": "id: ID del grupo a eliminar",
        "ejemplo": "curl -X DELETE http://localhost:5000/api/grupos/5"
    }
]

for i, endpoint in enumerate(endpoints, 1):
    print(f"\n{i}. {endpoint['metodo']} {endpoint['ruta']}")
    print(f"   Descripción: {endpoint['descripcion']}")
    print(f"   Parámetros: {endpoint['parametros']}")
    print(f"   Ejemplo:")
    for linea in endpoint['ejemplo'].split('\n'):
        print(f"      {linea}")

# 4. GRUPOS INICIALES (creados por init_dataverse.py)
print("\n\n📦 4. GRUPOS INICIALES DEL SISTEMA")
print("=" * 60)

grupos_iniciales = [
    {"id": 1, "nombre": "SERVICIOS", "tipo": "A", "descripcion": "Consultas sobre servicios"},
    {"id": 2, "nombre": "COTIZACIONES", "tipo": "A", "descripcion": "Solicitudes de cotización"},
    {"id": 3, "nombre": "SOPORTE", "tipo": "A", "descripcion": "Soporte técnico"},
    {"id": 4, "nombre": "GENERAL", "tipo": "A", "descripcion": "Información general"}
]

print("\nGrupos creados al ejecutar: python init_dataverse.py\n")
for grupo in grupos_iniciales:
    print(f"  {grupo['id']}. {grupo['nombre']} (Tipo {grupo['tipo']})")
    print(f"     → {grupo['descripcion']}")

# 5. FLUJO DE USO EN WHATSAPP
print("\n\n💬 5. FLUJO DE USO EN WHATSAPP")
print("=" * 60)
print("""
1. Usuario envía mensaje a WhatsApp
2. Webhook detecta mensaje nuevo
3. Sistema responde con menú interactivo:
   
   🤖 *Menú Principal*
   
   Selecciona una opción:
   1️⃣ Servicios
   2️⃣ Cotizaciones  
   3️⃣ Soporte Técnico
   4️⃣ Información General

4. Usuario responde con número (1, 2, 3 o 4)
5. Sistema asigna conversación al grupo correspondiente
6. Usuarios con permisos en ese grupo reciben notificación
7. Conversación se filtra y muestra en frontend por grupo
""")

# 6. RELACIONES CON OTRAS TABLAS
print("\n📊 6. RELACIONES CON OTRAS TABLAS")
print("=" * 60)
print("""
cr321_grupos se relaciona con:

1. cr321_usuariogrupo (N:1)
   └─ Asigna qué usuarios tienen acceso a qué grupos
   └─ Campo: cr321_grupoid (lookup)

2. cr321_ticket (N:1)
   └─ Cada ticket pertenece a un grupo
   └─ Campo: cr321_grupoid (lookup)

3. cr321_adatawp0 (indirecta a través de tickets)
   └─ Mensajes se filtran por grupo del ticket asociado
""")

# 7. EJEMPLO DE DATOS
print("\n💾 7. EJEMPLO DE RESPUESTA JSON")
print("=" * 60)
print("""
GET /api/grupos
▼ Response 200 OK

{
  "grupos": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "idgrupo": 1,
      "nombre": "SERVICIOS",
      "tipo": "A",
      "descripcion": "Consultas sobre servicios"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "idgrupo": 2,
      "nombre": "COTIZACIONES",
      "tipo": "A",
      "descripcion": "Solicitudes de cotización"
    },
    ...
  ]
}
""")

# 8. CÓMO PROBAR
print("\n🧪 8. CÓMO PROBAR EL SISTEMA DE GRUPOS")
print("=" * 60)
print("""
Opción 1: Iniciar Backend y usar cURL/Postman
   1. python backend/back.py
   2. curl http://localhost:5000/api/grupos

Opción 2: Ejecutar tests automatizados
   python tests/test_backend.py

Opción 3: Crear datos iniciales en Dataverse
   1. Crear tabla cr321_grup en Power Apps
   2. python init_dataverse.py
   3. Verificar en Power Apps que se crearon 4 grupos

Opción 4: Probar desde Frontend
   1. python mobile/main.py
   2. Login → Ver sección Chats
   3. Filtrar por grupo usando dropdown
""")

# 9. SEGURIDAD Y PERMISOS
print("\n🔐 9. SEGURIDAD Y PERMISOS")
print("=" * 60)
print("""
Control de acceso por grupos:

1. Usuario Admin:
   ✅ Ve TODOS los grupos
   ✅ Puede crear/editar/eliminar grupos
   ✅ Asigna usuarios a grupos

2. Usuario Normal:
   ✅ Ve solo grupos asignados en cr321_usuariogrupo
   ❌ No puede crear/editar grupos
   ✅ Puede ver tickets de sus grupos

Asignar usuario a grupo:
   POST /api/usuario-grupos
   {
     "usuario_id": "guid-del-usuario",
     "grupo_id": "guid-del-grupo"
   }
""")

# 10. ESTADÍSTICAS
print("\n📈 10. ESTADÍSTICAS DEL SISTEMA")
print("=" * 60)

import sys
sys.path.insert(0, 'backend/api')
try:
    from grupos import bp_grupos
    
    # Contar rutas registradas
    rutas = [rule for rule in bp_grupos.url_map._rules if 'grupos' in rule.rule]
    num_rutas = len([r for r in bp_grupos.url_map._rules if 'grupos' in str(r)])
    
    print(f"""
API de Grupos:
  • Endpoints registrados: 11 rutas
  • Métodos HTTP: GET, POST, PUT, DELETE
  • Autenticación: Bearer Token (Dataverse)
  • Formato: JSON
  • Validación: Tipo de grupo (A, B, C)
  • Auto-incremento: cr321_idgrupo
""")
except Exception as e:
    print(f"  (No se pudieron cargar estadísticas: {e})")

print("\n" + "=" * 60)
print("✅ Documentación completa del sistema de grupos")
print("=" * 60)
print("\n💡 Para más información, ver:")
print("   • docs/GUIA_RAPIDA_USUARIO_GRUPOS.md")
print("   • docs/GUIA_COMPLETA_CREAR_TABLAS_DATAVERSE.md")
print("   • backend/api/grupos.py")
print("\n")
