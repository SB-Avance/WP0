"""
Test Dashboard API - Mejora #2
================================

Prueba los 5 endpoints del dashboard:
1. Health check
2. Métricas por grupos
3. Métricas generales
4. Volumetría
5. Tendencias

Ejecutar: python test_dashboard.py
"""

import requests
import json
from datetime import datetime, timedelta

# Configuración
BASE_URL = "http://localhost:5000"
DASHBOARD_URL = f"{BASE_URL}/api/dashboard"


def print_section(title):
    """Imprimir sección con formato."""
    print("\n" + "=" * 70)
    print(f"   {title}")
    print("=" * 70)


def print_json(data, max_items=3):
    """Imprimir JSON formateado."""
    if isinstance(data, list) and len(data) > max_items:
        print(f"\n📊 Mostrando {max_items} de {len(data)} elementos:")
        for item in data[:max_items]:
            print(json.dumps(item, indent=2, ensure_ascii=False))
        print(f"... y {len(data) - max_items} más")
    else:
        print(json.dumps(data, indent=2, ensure_ascii=False))


def test_1_health():
    """Test 1: Health check"""
    print_section("TEST 1: Health Check")
    
    try:
        response = requests.get(f"{DASHBOARD_URL}/health", timeout=10)
        
        print(f"🔄 GET {DASHBOARD_URL}/health")
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Service: {data.get('service')}")
            print(f"✅ Version: {data.get('version')}")
            print(f"✅ Endpoints: {len(data.get('endpoints', []))} disponibles")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False


def test_2_metricas_grupos():
    """Test 2: Métricas por grupos"""
    print_section("TEST 2: Métricas por Grupos")
    
    try:
        response = requests.get(f"{DASHBOARD_URL}/metricas-grupos", timeout=30)
        
        print(f"🔄 GET {DASHBOARD_URL}/metricas-grupos")
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                grupos = data.get('grupos', [])
                print(f"\n✅ Total grupos: {data.get('total_grupos')}")
                print(f"✅ Período: {data.get('periodo', {}).get('desde')} → {data.get('periodo', {}).get('hasta')}")
                
                print(f"\n📊 Top 3 grupos por mensajes:")
                for i, grupo in enumerate(grupos[:3], 1):
                    print(f"\n{i}. {grupo['grupo_nombre']} (ID: {grupo['grupo_id']})")
                    print(f"   📨 Total mensajes: {grupo['total_mensajes']}")
                    print(f"   📥 Entrantes: {grupo['mensajes_entrantes']}")
                    print(f"   📤 Salientes: {grupo['mensajes_salientes']}")
                    print(f"   👥 Contactos únicos (est): {grupo['contactos_unicos_estimado']}")
                    print(f"   📊 Tasa respuesta: {grupo['tasa_respuesta']}")
                
                return True
            else:
                print(f"❌ Error: {data.get('error')}")
                return False
        else:
            print(f"❌ HTTP Error: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False


def test_3_metricas_generales():
    """Test 3: Métricas generales"""
    print_section("TEST 3: Métricas Generales del Sistema")
    
    try:
        response = requests.get(f"{DASHBOARD_URL}/metricas-generales", timeout=30)
        
        print(f"🔄 GET {DASHBOARD_URL}/metricas-generales")
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                metricas = data.get('metricas', {})
                
                print(f"\n✅ MÉTRICAS GLOBALES:")
                print(f"   📨 Total mensajes: {metricas.get('total_mensajes')}")
                print(f"   📥 Entrantes: {metricas.get('mensajes_entrantes')}")
                print(f"   📤 Salientes: {metricas.get('mensajes_salientes')}")
                print(f"   👥 Total contactos: {metricas.get('total_contactos')}")
                print(f"   📁 Total grupos: {metricas.get('total_grupos')}")
                print(f"   📅 Mensajes hoy: {metricas.get('mensajes_hoy')}")
                print(f"   📊 Mensajes esta semana: {metricas.get('mensajes_esta_semana')}")
                print(f"   📈 Tasa respuesta: {metricas.get('tasa_respuesta_global')}")
                print(f"   💬 Mensajes por contacto: {metricas.get('mensajes_por_contacto')}")
                
                return True
            else:
                print(f"❌ Error: {data.get('error')}")
                return False
        else:
            print(f"❌ HTTP Error: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False


def test_4_volumetria():
    """Test 4: Volumetría"""
    print_section("TEST 4: Volumetría de Mensajes")
    
    try:
        # Últimos 7 días
        fecha_hasta = datetime.now().strftime('%Y-%m-%d')
        fecha_desde = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        url = f"{DASHBOARD_URL}/volumetria?desde={fecha_desde}&hasta={fecha_hasta}"
        response = requests.get(url, timeout=30)
        
        print(f"🔄 GET {url}")
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                volumetria = data.get('volumetria', [])
                resumen = data.get('resumen', {})
                
                print(f"\n✅ Período: {fecha_desde} → {fecha_hasta}")
                print(f"\n📊 RESUMEN:")
                print(f"   Total período: {resumen.get('total_periodo')}")
                print(f"   Promedio diario: {resumen.get('promedio_diario')}")
                
                if resumen.get('dia_max'):
                    print(f"   📈 Día máximo: {resumen['dia_max']['fecha']} ({resumen['dia_max']['total']} mensajes)")
                if resumen.get('dia_min'):
                    print(f"   📉 Día mínimo: {resumen['dia_min']['fecha']} ({resumen['dia_min']['total']} mensajes)")
                
                print(f"\n📅 Últimos 3 días:")
                for dia in volumetria[-3:]:
                    print(f"   {dia['periodo']}: {dia['total']} mensajes (↓{dia['entrantes']} ↑{dia['salientes']})")
                
                return True
            else:
                print(f"❌ Error: {data.get('error')}")
                return False
        else:
            print(f"❌ HTTP Error: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False


def test_5_tendencias():
    """Test 5: Tendencias"""
    print_section("TEST 5: Análisis de Tendencias")
    
    try:
        response = requests.get(f"{DASHBOARD_URL}/tendencias?dias=7", timeout=30)
        
        print(f"🔄 GET {DASHBOARD_URL}/tendencias?dias=7")
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                tendencias = data.get('tendencias', {})
                
                print(f"\n✅ TENDENCIAS (últimos 7 días):")
                print(f"   📈 Crecimiento: {tendencias.get('crecimiento_periodo')}")
                print(f"   🕐 Hora pico: {tendencias.get('hora_pico')}")
                print(f"   📅 Día semana pico: {tendencias.get('dia_semana_pico')}")
                print(f"   📊 Total período: {tendencias.get('total_periodo')}")
                print(f"   📉 Promedio diario: {tendencias.get('promedio_diario')}")
                
                mensajes_por_dia = tendencias.get('mensajes_por_dia', [])
                if mensajes_por_dia:
                    print(f"\n📅 Últimos 3 días:")
                    for dia in mensajes_por_dia[-3:]:
                        print(f"   {dia['fecha']}: {dia['total']} mensajes")
                
                return True
            else:
                print(f"❌ Error: {data.get('error')}")
                return False
        else:
            print(f"❌ HTTP Error: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False


def run_all_tests():
    """Ejecutar todos los tests"""
    print("\n" + "🚀 " + "=" * 66 + " 🚀")
    print("   PRUEBAS DE MEJORA #2: DASHBOARD API")
    print("🚀 " + "=" * 66 + " 🚀")
    print(f"   Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Backend: {BASE_URL}")
    
    resultados = []
    
    # Test 1: Health
    try:
        resultado = test_1_health()
        resultados.append(("Test 1: Health check", resultado))
    except Exception as e:
        print(f"\n❌ Error en Test 1: {e}")
        resultados.append(("Test 1: Health check", False))
    
    # Test 2: Métricas grupos
    try:
        resultado = test_2_metricas_grupos()
        resultados.append(("Test 2: Métricas grupos", resultado))
    except Exception as e:
        print(f"\n❌ Error en Test 2: {e}")
        resultados.append(("Test 2: Métricas grupos", False))
    
    # Test 3: Métricas generales
    try:
        resultado = test_3_metricas_generales()
        resultados.append(("Test 3: Métricas generales", resultado))
    except Exception as e:
        print(f"\n❌ Error en Test 3: {e}")
        resultados.append(("Test 3: Métricas generales", False))
    
    # Test 4: Volumetría
    try:
        resultado = test_4_volumetria()
        resultados.append(("Test 4: Volumetría", resultado))
    except Exception as e:
        print(f"\n❌ Error en Test 4: {e}")
        resultados.append(("Test 4: Volumetría", False))
    
    # Test 5: Tendencias
    try:
        resultado = test_5_tendencias()
        resultados.append(("Test 5: Tendencias", resultado))
    except Exception as e:
        print(f"\n❌ Error en Test 5: {e}")
        resultados.append(("Test 5: Tendencias", False))
    
    # Resumen
    print_section("📊 RESUMEN DE TESTS")
    
    total = len(resultados)
    pasados = sum(1 for _, r in resultados if r)
    fallidos = total - pasados
    
    for nombre, resultado in resultados:
        simbolo = "✅" if resultado else "❌"
        print(f"   {simbolo} {nombre}")
    
    print(f"\n{'='*70}")
    print(f"   Total: {total} | Pasados: {pasados} | Fallidos: {fallidos}")
    print(f"{'='*70}")
    
    if pasados == total:
        print("\n🎉 ¡TODOS LOS TESTS PASARON!")
        print("\n📝 Dashboard API está funcionando correctamente")
        print("\n📊 Endpoints disponibles:")
        print("   - GET /api/dashboard/health")
        print("   - GET /api/dashboard/metricas-grupos")
        print("   - GET /api/dashboard/metricas-generales")
        print("   - GET /api/dashboard/volumetria?desde=YYYY-MM-DD&hasta=YYYY-MM-DD")
        print("   - GET /api/dashboard/tendencias?dias=7")
    else:
        print(f"\n⚠️  {fallidos} test(s) fallaron. Revisar errores arriba.")
        if fallidos == total:
            print("\n💡 ¿Backend corriendo? Ejecuta: cd backend && python back.py")
    
    print()
    
    return pasados == total


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
