"""
Script de prueba para los nuevos endpoints de chats_extended.py
================================================================

Prueba los 5 endpoints nuevos que usan $expand de OData:
1. GET /api/chats/con-contacto
2. GET /api/chats/por-grupo/<grupo_id>
3. GET /api/chats/estadisticas-grupos
4. GET /api/chats/buscar
5. GET /api/chats/contacto/<contacto_id>/historial

Requisitos:
- Backend corriendo en localhost:5000
- Variables de entorno configuradas
- Datos en Dataverse con Lookups activos
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000"

def print_section(title):
    """Imprimir sección con formato"""
    print("\n" + "=" * 70)
    print(f"   {title}")
    print("=" * 70)

def test_health_check():
    """Test 0: Verificar que la API está disponible"""
    print_section("TEST 0: Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/api/chats/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API funcionando correctamente")
            print(f"📋 Endpoints disponibles: {len(data.get('endpoints', []))}")
            for endpoint in data.get('endpoints', []):
                print(f"   - {endpoint}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print("💡 ¿Está el backend corriendo? Ejecuta: iniciar_backend.ps1")
        return False

def test_chats_con_contacto():
    """Test 1: Obtener chats con información de contacto expandida"""
    print_section("TEST 1: Chats con Contacto (usando $expand)")
    
    try:
        params = {
            "top": 10
        }
        
        response = requests.get(
            f"{BASE_URL}/api/chats/con-contacto",
            params=params,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Éxito: {data.get('total', 0)} chats encontrados")
            
            if data.get('data') and len(data['data']) > 0:
                print("\n📊 Ejemplo de chat con contacto:")
                chat = data['data'][0]
                print(f"   Mensaje: {chat.get('mensaje', '¿?')[:50]}...")
                print(f"   Fecha: {chat.get('fecha_hora')}")
                print(f"   De: {chat.get('from_nombre')}")
                
                if chat.get('contacto'):
                    contacto = chat['contacto']
                    print(f"   📞 Contacto asociado:")
                    print(f"      - Nombre: {contacto.get('nombre')}")
                    print(f"      - Teléfono: {contacto.get('telefono')}")
                    print(f"      - Email: {contacto.get('correo')}")
                
                print(f"\n💡 Se trajo toda la info en 1 request (vs 2 requests sin $expand)")
            else:
                print("⚠️  No hay chats con contacto asociado")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Respuesta: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_estadisticas_grupos():
    """Test 3: Obtener estadísticas de mensajes por grupo"""
    print_section("TEST 2: Estadísticas por Grupo")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/chats/estadisticas-grupos",
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Éxito: {data.get('total_grupos', 0)} grupos con mensajes")
            
            if data.get('data') and len(data['data']) > 0:
                print("\n📊 Top 3 Grupos con más mensajes:")
                for i, grupo in enumerate(data['data'][:3], 1):
                    print(f"   {i}. {grupo.get('nombre')} ({grupo.get('tipo')})")
                    print(f"      Total mensajes: {grupo.get('total_mensajes')}")
                
                # Guardar grupo_id para siguiente test
                global primer_grupo_id
                primer_grupo_id = data['data'][0]['id']
                print(f"\n💾 Guardado ID del primer grupo para siguiente test: {primer_grupo_id}")
            else:
                print("⚠️  No hay estadísticas disponibles")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Respuesta: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_chats_por_grupo(grupo_id=None):
    """Test 2: Obtener chats de un grupo específico"""
    print_section("TEST 3: Chats por Grupo Específico")
    
    if not grupo_id:
        print("⚠️  No hay grupo_id disponible, saltando test")
        print("   (Ejecuta primero test_estadisticas_grupos)")
        return False
    
    try:
        params = {
            "top": 5,
            "expand_contacto": "true"
        }
        
        response = requests.get(
            f"{BASE_URL}/api/chats/por-grupo/{grupo_id}",
            params=params,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Éxito: {data.get('total', 0)} chats en este grupo")
            
            if data.get('data') and len(data['data']) > 0:
                print("\n📊 Primeros 2 chats del grupo:")
                for i, chat in enumerate(data['data'][:2], 1):
                    print(f"\n   Chat {i}:")
                    print(f"   - Mensaje: {chat.get('mensaje', '')[:40]}...")
                    print(f"   - Fecha: {chat.get('fecha_hora')}")
                    
                    if chat.get('grupo'):
                        grupo = chat['grupo']
                        print(f"   - Grupo: {grupo.get('nombre')} (Tipo {grupo.get('tipo')})")
                    
                    if chat.get('contacto'):
                        contacto = chat['contacto']
                        print(f"   - Contacto: {contacto.get('nombre')}")
                
                # Guardar contacto_id para siguiente test
                if data['data'][0].get('contacto'):
                    global primer_contacto_id
                    primer_contacto_id = data['data'][0]['contacto']['id']
                    print(f"\n💾 Guardado ID del primer contacto: {primer_contacto_id}")
            else:
                print("⚠️  No hay chats en este grupo")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Respuesta: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_buscar_chats():
    """Test 4: Búsqueda avanzada de chats"""
    print_section("TEST 4: Búsqueda Avanzada")
    
    try:
        params = {
            "texto": "hola",
            "top": 5
        }
        
        response = requests.get(
            f"{BASE_URL}/api/chats/buscar",
            params=params,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Éxito: {data.get('total', 0)} chats encontrados")
            print(f"   Filtros: {json.dumps(data.get('filtros_aplicados'), indent=2)}")
            
            if data.get('data') and len(data['data']) > 0:
                print("\n📊 Primer resultado:")
                chat = data['data'][0]
                print(f"   - Mensaje: {chat.get('mensaje', '')[:60]}...")
                print(f"   - Grupo: {chat.get('grupo_nombre')}")
                print(f"   - Contacto: {chat.get('contacto_nombre')}")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Respuesta: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_historial_contacto(contacto_id=None):
    """Test 5: Historial completo de un contacto"""
    print_section("TEST 5: Historial de Contacto")
    
    if not contacto_id:
        print("⚠️  No hay contacto_id disponible, saltando test")
        print("   (Ejecuta primero test_chats_por_grupo)")
        return False
    
    try:
        params = {
            "ordenar": "asc"
        }
        
        response = requests.get(
            f"{BASE_URL}/api/chats/contacto/{contacto_id}/historial",
            params=params,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Éxito: {data.get('total_mensajes', 0)} mensajes en historial")
            
            resumen = data.get('resumen', {})
            print(f"\n📊 Resumen del contacto:")
            print(f"   - Mensajes entrantes: {resumen.get('entrantes')}")
            print(f"   - Mensajes salientes: {resumen.get('salientes')}")
            print(f"   - Primera interacción: {resumen.get('primera_interaccion')}")
            print(f"   - Última interacción: {resumen.get('ultima_interaccion')}")
            
            if data.get('historial') and len(data['historial']) > 0:
                print(f"\n📜 Timeline (primeros 3 mensajes):")
                for i, msg in enumerate(data['historial'][:3], 1):
                    direccion = "📥 Entrante" if msg.get('direccion') == 1 else "📤 Saliente"
                    print(f"   {i}. {direccion}")
                    print(f"      {msg.get('mensaje', '')[:50]}...")
                    print(f"      Grupo: {msg.get('grupo', {}).get('nombre', 'N/A')}")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Respuesta: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def run_all_tests():
    """Ejecutar todos los tests en secuencia"""
    print("\n")
    print("🚀 " + "=" * 66 + " 🚀")
    print("   PRUEBA DE ENDPOINTS - CHATS EXTENDED API CON $EXPAND")
    print("🚀 " + "=" * 66 + " 🚀")
    print(f"   Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Backend: {BASE_URL}")
    
    # Variables globales para IDs
    global primer_grupo_id, primer_contacto_id
    primer_grupo_id = None
    primer_contacto_id = None
    
    # Test 0: Health check
    if not test_health_check():
        print("\n❌ Backend no disponible. Abortando tests.")
        print("💡 Ejecuta: .\\iniciar_backend.ps1")
        return
    
    # Test 1: Chats con contacto
    test_chats_con_contacto()
    
    # Test 2: Estadísticas (obtiene grupo_id)
    test_estadisticas_grupos()
    
    # Test 3: Chats por grupo (obtiene contacto_id)
    if primer_grupo_id:
        test_chats_por_grupo(primer_grupo_id)
    
    # Test 4: Búsqueda avanzada
    test_buscar_chats()
    
    # Test 5: Historial de contacto
    if primer_contacto_id:
        test_historial_contacto(primer_contacto_id)
    
    # Resumen final
    print("\n")
    print("=" * 70)
    print("   ✅ TESTS COMPLETADOS")
    print("=" * 70)
    print("\n💡 Próximos pasos:")
    print("   1. Implementar estos endpoints en el frontend")
    print("   2. Crear dashboard con estadísticas")
    print("   3. Optimizar consultas según necesidades")
    print("\n📚 Documentación: docs/SUGERENCIAS_PROXIMOS_PASOS.md")
    print()

if __name__ == "__main__":
    run_all_tests()
