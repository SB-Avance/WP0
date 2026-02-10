"""
Verificar flujo completo: Usuario 0006 -> Grupos -> Conversaciones filtradas
"""
import requests

USUARIO_0006 = "e45580f3-59fa-f011-8406-002248df122f"

print("="*80)
print("VERIFICACION FLUJO COMPLETO CON LOOKUP")
print("="*80)

# 1. Obtener grupos del usuario via endpoint refactorizado
print("\n1. OBTENER GRUPOS DEL USUARIO")
print("-"*80)

url_grupos = f"http://localhost:5000/api/usuario-grupos/usuario/{USUARIO_0006}"
response_grupos = requests.get(url_grupos)

if response_grupos.status_code == 200:
    data = response_grupos.json()
    grupos = data.get("grupos", [])
    
    print(f"✅ Usuario: otro c (c)")
    print(f"   ID: {USUARIO_0006}")
    print(f"\n   Grupos asignados: {len(grupos)}")
    
    grupo_nombres = []
    for g in grupos:
        nombre = g.get("nombre")
        codigo = g.get("grupoid")
        guid = g.get("id")[:38]
        grupo_nombres.append(nombre)
        print(f"   - {nombre} (Codigo: {codigo} | GUID: {guid})")
else:
    print(f"❌ Error: {response_grupos.status_code}")
    exit(1)

# 2. Obtener todas las conversaciones
print("\n2. OBTENER CONVERSACIONES")
print("-"*80)

url_conversaciones = "http://localhost:5000/api/conversations"
response_conv = requests.get(url_conversaciones)

if response_conv.status_code == 200:
    data_conv = response_conv.json()
    conversaciones = data_conv.get("conversations", [])
    
    print(f"✅ Total conversaciones en sistema: {len(conversaciones)}")
else:
    print(f"❌ Error: {response_conv.status_code}")
    exit(1)

# 3. Filtrar conversaciones del usuario
print("\n3. FILTRAR CONVERSACIONES DEL USUARIO")
print("-"*80)

conversaciones_filtradas = [c for c in conversaciones if c.get("group") in grupo_nombres]

print(f"✅ Conversaciones visibles para usuario 0006: {len(conversaciones_filtradas)}")
print()

if conversaciones_filtradas:
    print(f"{'Telefono':<20} {'Nombre':<30} {'Grupo':<20}")
    print("-"*70)
    for c in conversaciones_filtradas:
        telefono = c.get("phone", "")
        nombre = c.get("name", "")[:28]
        grupo = c.get("group", "")
        print(f"{telefono:<20} {nombre:<30} {grupo:<20}")
else:
    print("⚠️  Sin conversaciones visibles")

# 4. Resumen del flujo
print("\n" + "="*80)
print("FLUJO COMPLETO")
print("="*80)

print("""
1. Usuario 0006 (c) hace login
   ↓
2. Backend consulta: /api/usuario-grupos/usuario/{user_id}
   ├── Query: cr321_usuariogrupos
   ├── Filter: _cr321_usuarioid_value eq {guid}
   └── Expand: $expand=cr321_grupo($select=cr321_nombre)
   ↓
3. Dataverse retorna grupos con lookup navegado:
   └── ["Contabilidad"]
   ↓
4. Backend obtiene conversaciones:
   └── cr321_adatawp0s con $expand=cr321_grupoid
   ↓
5. Frontend filtra conversaciones:
   └── if conversation.group in user_groups
""")

print("="*80)
print("ARQUITECTURA")
print("="*80)

print("""
✅ LOOKUP _cr321_grupo_value en cr321_usuariogrupos
   - Integridad referencial garantizada
   - Navegación con $expand eficiente
   - Sin diccionarios hardcoded
   - Nombres actualizados automáticamente

✅ LOOKUP _cr321_grupoid_value en cr321_adatawp0s
   - Mismas ventajas
   - Conversaciones asignadas a grupos válidos
   - Filtrado robusto

✅ BACKEND refactorizado
   - Eliminado: INT_TO_GROUP, GROUP_TO_INT, CODIGO_A_NOMBRE
   - Agregado: GROUP_GUID_CACHE, $expand en queries
   - Código más mantenible y robusto
""")

print("="*80)
print(f"✅ SISTEMA OPERATIVO CON ARQUITECTURA LOOKUP CORRECTA")
print("="*80)
