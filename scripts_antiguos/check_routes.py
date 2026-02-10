"""Script para listar todas las rutas registradas en Flask"""
import sys
sys.path.append('C:/VS/BIN/backend')

from back import app

print("\n=== RUTAS REGISTRADAS EN FLASK ===\n")

for rule in app.url_map.iter_rules():
    methods = ','.join(sorted(rule.methods - {'OPTIONS', 'HEAD'}))
    print(f"{methods:20} {rule.rule}")

print(f"\nTotal rutas: {len(list(app.url_map.iter_rules()))}")

# Buscar específicamente dashboard
dashboard_routes = [r for r in app.url_map.iter_rules() if 'dashboard' in str(r.rule)]
print(f"\n=== RUTAS DASHBOARD ===")
if dashboard_routes:
    for r in dashboard_routes:
        print(f"  {r.rule}")
else:
    print("  ❌ No se encontraron rutas de dashboard")
