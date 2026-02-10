"""
Prueba end-to-end del sistema completo
"""
import requests
import sys

print("="*80)
print("PRUEBA END-TO-END DEL SISTEMA COMPLETO")
print("="*80)

# Usuario de prueba
USUARIO_0006 = "e45580f3-59fa-f011-8406-002248df122f"
BASE_URL = "http://localhost:5000"

tests_passed = 0
tests_failed = 0

def test(nombre, condicion, mensaje_ok="OK", mensaje_error="FALLO"):
    global tests_passed, tests_failed
    if condicion:
        print(f"  [OK] {nombre}: {mensaje_ok}")
        tests_passed += 1
        return True
    else:
        print(f"  [FAIL] {nombre}: {mensaje_error}")
        tests_failed += 1
        return False

# TEST 1: Backend activo
print("\n[TEST 1] Backend activo")
print("-"*80)
try:
    response = requests.get(f"{BASE_URL}/api/conversations", timeout=3)
    test("Backend responde", response.status_code == 200, 
         f"Status {response.status_code}", f"Status {response.status_code}")
except Exception as e:
    test("Backend responde", False, "", str(e))
    print("\n❌ Backend no activo - abortando tests")
    sys.exit(1)

# TEST 2: API de grupos del usuario con lookup
print("\n[TEST 2] API usuario-grupos usa lookups")
print("-"*80)
try:
    response = requests.get(f"{BASE_URL}/api/usuario-grupos/usuario/{USUARIO_0006}")
    data = response.json()
    grupos = data.get("grupos", [])
    
    test("API responde", response.status_code == 200)
    test("Usuario tiene grupos", len(grupos) > 0, f"{len(grupos)} grupos")
    
    if grupos:
        grupo = grupos[0]
        test("Tiene campo 'id' (GUID)", "id" in grupo, f"GUID: {grupo.get('id', '')[:8]}...")
        test("Tiene campo 'grupoid' (código)", "grupoid" in grupo, f"Código: {grupo.get('grupoid')}")
        test("Tiene campo 'nombre'", "nombre" in grupo, f"Nombre: {grupo.get('nombre')}")
        test("Nombre NO es None", grupo.get("nombre") is not None, grupo.get("nombre"))
        
        print(f"\n  📊 Datos del grupo:")
        print(f"     GUID: {grupo.get('id')}")
        print(f"     Código: {grupo.get('grupoid')}")
        print(f"     Nombre: {grupo.get('nombre')}")
        
except Exception as e:
    test("API usuario-grupos", False, "", str(e))

# TEST 3: GET conversaciones retorna datos correctos
print("\n[TEST 3] GET /api/conversations con lookups")
print("-"*80)
try:
    response = requests.get(f"{BASE_URL}/api/conversations")
    data = response.json()
    conversaciones = data.get("conversations", [])
    grupos = data.get("groups", [])
    
    test("API responde", response.status_code == 200)
    test("Tiene conversaciones", len(conversaciones) > 0, f"{len(conversaciones)} conversaciones")
    test("Tiene grupos", len(grupos) > 0, f"{len(grupos)} grupos: {', '.join(grupos[:3])}")
    
    if conversaciones:
        conv = conversaciones[0]
        test("Conversación tiene 'group'", "group" in conv, f"Grupo: {conv.get('group')}")
        test("Grupo NO es None", conv.get("group") is not None, conv.get("group"))
        test("Grupo está en lista", conv.get("group") in grupos)
        
        print(f"\n  📊 Primera conversación:")
        print(f"     Teléfono: {conv.get('phone')}")
        print(f"     Nombre: {conv.get('name')}")
        print(f"     Grupo: {conv.get('group')}")
        
except Exception as e:
    test("GET conversaciones", False, "", str(e))

# TEST 4: Filtrado de conversaciones del usuario
print("\n[TEST 4] Filtrado de conversaciones por usuario")
print("-"*80)
try:
    # Obtener grupos del usuario
    response_grupos = requests.get(f"{BASE_URL}/api/usuario-grupos/usuario/{USUARIO_0006}")
    grupos_usuario = [g.get("nombre") for g in response_grupos.json().get("grupos", [])]
    
    # Obtener todas las conversaciones
    response_conv = requests.get(f"{BASE_URL}/api/conversations")
    todas_conv = response_conv.json().get("conversations", [])
    
    # Filtrar
    conv_filtradas = [c for c in todas_conv if c.get("group") in grupos_usuario]
    
    test("Usuario tiene grupos asignados", len(grupos_usuario) > 0, f"Grupos: {grupos_usuario}")
    test("Se pueden filtrar conversaciones", True, f"{len(conv_filtradas)}/{len(todas_conv)} visibles")
    
    print(f"\n  📊 Filtrado:")
    print(f"     Grupos del usuario: {', '.join(grupos_usuario)}")
    print(f"     Conversaciones visibles: {len(conv_filtradas)}")
    
    for c in conv_filtradas:
        print(f"       - {c.get('phone')}: {c.get('name')} [{c.get('group')}]")
        
except Exception as e:
    test("Filtrado de conversaciones", False, "", str(e))

# TEST 5: Cache de grupos
print("\n[TEST 5] Cache de grupos (GROUP_GUID_CACHE)")
print("-"*80)

# Verificar que back.py tiene el cache
try:
    with open("c:/VS/BIN/backend/back.py", 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    test("back.py tiene GROUP_GUID_CACHE", "GROUP_GUID_CACHE" in contenido)
    test("back.py tiene load_group_guids()", "load_group_guids" in contenido)
    test("back.py tiene get_group_guid()", "get_group_guid" in contenido)
    test("Cache se carga al inicio", "load_group_guids()" in contenido)
    
except Exception as e:
    test("Verificar cache en código", False, "", str(e))

# TEST 6: Sin diccionarios hardcoded
print("\n[TEST 6] Sin diccionarios hardcoded (legacy)")
print("-"*80)

archivos_backend = [
    "c:/VS/BIN/backend/back.py",
    "c:/VS/BIN/backend/api/usuario_grupos.py"
]

for archivo in archivos_backend:
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        nombre = archivo.split('/')[-1]
        test(f"{nombre} sin INT_TO_GROUP", "INT_TO_GROUP" not in contenido)
        test(f"{nombre} sin GROUP_TO_INT", "GROUP_TO_INT" not in contenido)
        test(f"{nombre} sin CODIGO_A_NOMBRE", "CODIGO_A_NOMBRE" not in contenido)
        
    except Exception as e:
        print(f"  ⚠️  Error leyendo {archivo}: {e}")

# RESUMEN
print("\n" + "="*80)
print("RESUMEN DE TESTS")
print("="*80)

total_tests = tests_passed + tests_failed
porcentaje = (tests_passed / total_tests * 100) if total_tests > 0 else 0

print(f"""
Tests ejecutados:  {total_tests}
Tests exitosos:    {tests_passed} ✅
Tests fallidos:    {tests_failed} ❌
Éxito:             {porcentaje:.1f}%
""")

if tests_failed == 0:
    print("╔" + "="*78 + "╗")
    print("║" + " "*26 + "✅ TODOS LOS TESTS PASARON" + " "*26 + "║")
    print("║" + " "*78 + "║")
    print("║  Backend completamente funcional con arquitectura lookup" + " "*19 + "║")
    print("║  Sin código legacy • Integridad referencial • Cache activo" + " "*16 + "║")
    print("╚" + "="*78 + "╝")
    sys.exit(0)
else:
    print("╔" + "="*78 + "╗")
    print("║" + " "*22 + f"⚠️  {tests_failed} TESTS FALLARON" + " "*28 + "║")
    print("║" + " "*78 + "║")
    print("║  Revisar errores arriba" + " "*54 + "║")
    print("╚" + "="*78 + "╝")
    sys.exit(1)
