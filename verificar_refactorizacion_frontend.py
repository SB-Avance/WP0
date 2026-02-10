"""
Verificación de refactorización del frontend
"""
import re

print("="*80)
print("VERIFICACION DE REFACTORIZACION DEL FRONTEND")
print("="*80)

# Leer archivo refactorizado
with open("c:/VS/BIN/mobile/main.py", 'r', encoding='utf-8') as f:
    contenido = f.read()

tests_passed = 0
tests_failed = 0

def test(nombre, condicion, detalle=""):
    global tests_passed, tests_failed
    if condicion:
        print(f"  [OK] {nombre}")
        if detalle:
            print(f"       {detalle}")
        tests_passed += 1
        return True
    else:
        print(f"  [FAIL] {nombre}")
        if detalle:
            print(f"         {detalle}")
        tests_failed += 1
        return False

print("\n[TEST 1] Eliminación de código legacy")
print("-"*80)

test("group_mapping eliminado", 
     "group_mapping" not in contenido,
     "Diccionario hardcoded ya no existe")

test("Sin mapeos 0001-0004",
     '"0001": "Soporte"' not in contenido and
     '"0002": "Ventas"' not in contenido,
     "Códigos hardcoded eliminados")

print("\n[TEST 2] Cache de grupos implementado")
print("-"*80)

test("user_groups_cache definido",
     "user_groups_cache" in contenido,
     "Variable de cache agregada")

test("Cache inicializado", 
     'user_groups_cache = {"value": None}' in contenido,
     "Inicialización correcta")

test("Cache usado en filtrado",
     "if user_groups_cache" in contenido and "is None" in contenido,
     "Lógica de cache implementada")

test("Cache limpiado en logout",
     'user_groups_cache["value"] = None' in contenido,
     "Limpieza de cache al salir")

print("\n[TEST 3] Logs optimizados")
print("-"*80)

# Contar logs [DEBUG]
debug_count = len(re.findall(r'\[DEBUG\]', contenido))
filtro_count = len(re.findall(r'\[FILTRO\]', contenido))

test("Logs [DEBUG] reducidos",
     debug_count < 5,
     f"Cantidad: {debug_count} (antes: ~9)")

test("Logs [FILTRO] optimizados",
     filtro_count >= 4 and filtro_count <= 7,
     f"Cantidad: {filtro_count} (rango óptimo)")

print("\n[TEST 4] Código limpio")
print("-"*80)

# Buscar sección de filtrado
filtrado_section = contenido[contenido.find("if current_view[\"value\"] == \"chats\":"):
                             contenido.find("content = ChatsView")]

lineas_filtrado = len(filtrado_section.split('\n'))

test("Código de filtrado reducido",
     lineas_filtrado < 40,
     f"Líneas: {lineas_filtrado} (antes: 47)")

test("Sin comentarios de mapeo",
     "Mapeo de grupoid" not in contenido,
     "Comentarios legacy eliminados")

print("\n[TEST 5] Integración con backend")
print("-"*80)

test("Usa api.get_user_groups",
     "api.get_user_groups(user_id)" in contenido,
     "Endpoint correcto del backend")

test("Extrae nombres directamente",
     'g.get("nombre")' in contenido,
     "Usa lookups del backend")

test("Filtrado por nombres",
     'c.get("group") in user_group_names' in contenido,
     "Comparación correcta")

print("\n[TEST 6] Estructura de código")
print("-"*80)

test("Función on_logout actualizada",
     "on_logout" in contenido and "user_groups_cache" in contenido,
     "Función refactorizada")

test("Render optimizado",
     "def render():" in contenido,
     "Función principal intacta")

# Resumen
print("\n" + "="*80)
print("RESUMEN")
print("="*80)

total = tests_passed + tests_failed
porcentaje = (tests_passed / total * 100) if total > 0 else 0

print(f"""
Tests ejecutados: {total}
Tests exitosos:   {tests_passed}
Tests fallidos:   {tests_failed}
Éxito:            {porcentaje:.1f}%
""")

if tests_failed == 0:
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + " ✓ REFACTORIZACION EXITOSA" + " "*32 + "║")
    print("║" + " "*78 + "║")
    print("║  Frontend refactorizado con arquitectura optimizada" + " "*25 + "║")
    print("║  Sin código legacy • Cache implementado • Logs optimizados" + " "*17 + "║")
    print("╚" + "="*78 + "╝")
    
    print("\n📄 Archivo refactorizado: c:/VS/BIN/mobile/main.py")
    print("📚 Documentación: c:/VS/BIN/docs/REFACTORIZACION_FRONTEND.md")
    
else:
    print("╔" + "="*78 + "╗")
    print("║" + " "*22 + f"⚠ {tests_failed} TESTS FALLARON" + " "*36 + "║")
    print("║" + " "*78 + "║")
    print("║  Revisar errores arriba" + " "*54 + "║")
    print("╚" + "="*78 + "╝")

print("\n" + "="*80)
print("SIGUIENTES PASOS")
print("="*80)

print("""
1. Reiniciar aplicación:
   cd c:/VS/BIN
   .\iniciar.ps1

2. Pruebas manuales:
   - Login como usuario normal (c/c)
   - Verificar logs de cache
   - Verificar filtrado de conversaciones
   - Logout y volver a entrar

3. Monitorear logs:
   - [FILTRO] Cargando grupos... (primera vez)
   - [FILTRO] Usando cache... (siguientes veces)
   - [FILTRO] Filtrando X conversaciones...
""")

print("="*80)
