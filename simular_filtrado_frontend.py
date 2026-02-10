"""
Simular el flujo completo de filtrado del frontend
"""
import requests
import json

# ID del usuario 0006 (correo='c', clave='c')
USUARIO_ID = "e45580f3-59fa-f011-8406-002248df122f"
BACKEND_URL = "http://localhost:5000"

print("=" * 70)
print("SIMULACIÓN FLUJO FILTRADO FRONTEND - Usuario 0006")
print("=" * 70)

# 1. Obtener grupos del usuario
print("\n1. Obteniendo grupos del usuario 0006...")
url = f"{BACKEND_URL}/api/usuario-grupos/usuario/{USUARIO_ID}"
print(f"   GET {url}")

try:
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        user_groups_data = response.json()
        user_groups = user_groups_data.get("grupos", [])
        user_group_names = [g.get("nombre") for g in user_groups if g.get("nombre")]
        
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📋 Grupos encontrados: {len(user_groups)}")
        for g in user_groups:
            print(f"      - {g.get('nombre')} (código: {g.get('grupoid')})")
        print(f"   🔍 Nombres para filtrar: {user_group_names}")
    else:
        print(f"   ❌ Error: {response.status_code}")
        user_group_names = []
except Exception as e:
    print(f"   ⚠️ Error: {e}")
    user_group_names = []

# 2. Obtener todas las conversaciones
print("\n2. Obteniendo todas las conversaciones...")
url = f"{BACKEND_URL}/api/conversations"
print(f"   GET {url}")

try:
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        data = response.json()
        all_conversations = data.get("conversations", [])
        all_groups = data.get("groups", [])
        
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📞 Total conversaciones: {len(all_conversations)}")
        print(f"   📊 Grupos disponibles: {all_groups}")
    else:
        print(f"   ❌ Error: {response.status_code}")
        all_conversations = []
except Exception as e:
    print(f"   ⚠️ Error: {e}")
    all_conversations = []

# 3. Aplicar filtrado (lógica del frontend)
print("\n3. Aplicando filtrado (lógica mobile/main.py)...")
if user_group_names:
    print(f"   🔍 Filtrando por grupos: {user_group_names}")
    filtered_conversations = [
        c for c in all_conversations 
        if c.get("group") in user_group_names
    ]
    print(f"   ✅ Conversaciones filtradas: {len(filtered_conversations)}")
else:
    print(f"   ⚠️ Usuario sin grupos - mostrando todas")
    filtered_conversations = all_conversations

# 4. Mostrar resultado final
print("\n4. RESULTADO FINAL - Conversaciones que verá el usuario 0006:")
print("=" * 70)

if filtered_conversations:
    for i, conv in enumerate(filtered_conversations, 1):
        print(f"\n   #{i}")
        print(f"   📱 Teléfono: {conv.get('phone')}")
        print(f"   👤 Nombre: {conv.get('name')}")
        print(f"   📁 Grupo: {conv.get('group')}")
        print(f"   💬 Último mensaje: {conv.get('last_message')[:50]}")
        print(f"   🕐 Timestamp: {conv.get('timestamp')}")
else:
    print("\n   ❌ NO HAY CONVERSACIONES PARA MOSTRAR")
    print("   Esto significa que el usuario no verá ninguna conversación.")

# 5. Resumen por grupo
print("\n5. RESUMEN POR GRUPO:")
print("=" * 70)

if all_conversations:
    grupo_conversaciones = {}
    for conv in all_conversations:
        grupo = conv.get("group", "Sin grupo")
        if grupo not in grupo_conversaciones:
            grupo_conversaciones[grupo] = []
        grupo_conversaciones[grupo].append(conv.get("phone"))
    
    for grupo, phones in sorted(grupo_conversaciones.items()):
        has_access = grupo in user_group_names if user_group_names else True
        indicator = "✅ ACCESO" if has_access else "❌ SIN ACCESO"
        print(f"\n   {grupo}: {len(phones)} conversaciones {indicator}")
        for phone in phones:
            print(f"      - {phone}")

print("\n" +  "=" * 70)
print("DIAGNÓSTICO COMPLETO")
print("=" * 70)
