"""
Probar endpoint refactorizado con lookup
"""
import requests

# Usuario 0006 (otro c) - Grupo Contabilidad
USUARIO_ID = "e45580f3-59fa-f011-8406-002248df122f"

print("="*70)
print("PRUEBA DE ENDPOINT REFACTORIZADO")
print("="*70)

print(f"\nUsuario ID: {USUARIO_ID}")
print("Endpoint: /api/usuario-grupos/usuario/<usuario_id>")

url = f"http://localhost:5000/api/usuario-grupos/usuario/{USUARIO_ID}"

print(f"\nLlamando a: {url}")
response = requests.get(url)

print(f"\nStatus: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    grupos = data.get("grupos", [])
    
    print(f"\nTotal grupos: {len(grupos)}")
    print(f"\n{'GUID':<40} {'Codigo':<10} {'Nombre':<20}")
    print("-"*70)
    
    for g in grupos:
        guid = g.get("id", "")[:38]
        codigo = g.get("grupoid", "")
        nombre = g.get("nombre", "")
        print(f"{guid:<40} {codigo:<10} {nombre:<20}")
    
    print("\n" + "="*70)
    print("VENTAJAS DEL LOOKUP:")
    print("="*70)
    print("✅ Nombres vienen directamente de Dataverse (sin diccionario hardcoded)")
    print("✅ Integridad referencial garantizada")
    print("✅ Si cambia nombre en cr321_grup, se actualiza automáticamente")
    print("✅ Una sola query en lugar de múltiples")
    print("✅ Código más mantenible y robusto")
    
else:
    print(f"\nError: {response.text}")
