"""
Análisis detallado de lookups en archivos clave del backend
"""
import os
import re
from pathlib import Path

print("="*80)
print("ANALISIS DETALLADO DE LOOKUPS EN BACKEND")
print("="*80)

archivos_clave = {
    "backend/back.py": "Aplicación principal",
    "backend/api/usuario_grupos.py": "Relaciones usuario-grupo", 
    "backend/api/grupos.py": "Gestión de grupos",
    "backend/api/dashboard.py": "Dashboard y métricas",
    "backend/api/webhook_enhanced.py": "Webhook mejorado",
    "backend/api/chats_extended.py": "Chats extendidos"
}

for archivo, descripcion in archivos_clave.items():
    filepath = Path(f"c:/VS/BIN/{archivo}")
    
    if not filepath.exists():
        print(f"\n⚠️  {archivo} NO EXISTE")
        continue
    
    print(f"\n" + "="*80)
    print(f"📄 {archivo}")
    print(f"   {descripcion}")
    print("="*80)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        contenido = f.read()
        lineas = contenido.split('\n')
    
    # 1. Buscar tablas con lookups
    print("\n1. TABLAS Y LOOKUPS:")
    
    # Patrones de lookups
    lookup_pattern = re.compile(r'_(\w+)_value')
    lookups = set(lookup_pattern.findall(contenido))
    
    if lookups:
        for lookup in sorted(lookups):
            # Buscar líneas donde se usa
            for i, linea in enumerate(lineas, 1):
                if f"_{lookup}_value" in linea and not linea.strip().startswith("#"):
                    print(f"   ✅ _{lookup}_value (línea {i})")
                    print(f"      {linea.strip()[:70]}")
                    break
    else:
        print("   ⚠️  Sin lookups encontrados")
    
    # 2. Buscar $expand
    print("\n2. USO DE $EXPAND:")
    
    expand_lines = []
    for i, linea in enumerate(lineas, 1):
        if "$expand=" in linea and not linea.strip().startswith("#"):
            expand_lines.append((i, linea.strip()))
    
    if expand_lines:
        for num, linea in expand_lines:
            print(f"   ✅ Línea {num}:")
            print(f"      {linea[:70]}")
    else:
        print("   ⚠️  Sin $expand encontrado")
    
    # 3. Buscar @odata.bind
    print("\n3. USO DE @odata.bind:")
    
    odata_lines = []
    for i, linea in enumerate(lineas, 1):
        if "@odata.bind" in linea and not linea.strip().startswith("#"):
            odata_lines.append((i, linea.strip()))
    
    if odata_lines:
        for num, linea in odata_lines[:3]:  # Primeras 3
            print(f"   ✅ Línea {num}:")
            print(f"      {linea[:70]}")
        if len(odata_lines) > 3:
            print(f"   ... y {len(odata_lines) - 3} más")
    else:
        print("   ⚠️  Sin @odata.bind encontrado")
    
    # 4. Buscar queries a Dataverse
    print("\n4. QUERIES A DATAVERSE:")
    
    query_pattern = re.compile(r'/api/data/v9\.2/(cr321_\w+)')
    queries = query_pattern.findall(contenido)
    
    if queries:
        tablas_unique = sorted(set(queries))
        print(f"   Tablas consultadas: {len(tablas_unique)}")
        for tabla in tablas_unique:
            print(f"      - {tabla}")
    else:
        print("   ⚠️  Sin queries encontradas")
    
    # 5. Verificar GROUP_GUID_CACHE o similares
    print("\n5. CACHE DE GRUPOS:")
    
    if "GROUP_GUID_CACHE" in contenido:
        print("   ✅ Usa GROUP_GUID_CACHE")
        for i, linea in enumerate(lineas, 1):
            if "GROUP_GUID_CACHE" in linea and "=" in linea and "{" in linea:
                print(f"      Línea {i}: {linea.strip()[:60]}")
                break
    else:
        print("   ⚠️  No usa cache de grupos")

# Resumen final
print("\n" + "="*80)
print("RESUMEN GENERAL")
print("="*80)

print("""
✅ PATRON CORRECTO CON LOOKUPS:

1. Usar lookups para relaciones:
   - _cr321_grupoid_value para grupos
   - _cr321_usuarioid_value para usuarios
   - _cr321_contactoid_value para contactos
   
2. Navegación con $expand:
   url += "$expand=cr321_grupoid($select=cr321_nombre)"
   # Obtiene nombre del grupo en una sola query
   
3. Creación con @odata.bind:
   payload["cr321_grupoid@odata.bind"] = f"/cr321_grups({guid})"
   # Integridad referencial garantizada
   
4. Cache de GUIDs:
   GROUP_GUID_CACHE = {}
   # Evita queries repetidas

✅ VENTAJAS:
- Integridad referencial automática
- Una query en lugar de múltiples
- Sin diccionarios hardcoded
- Actualización automática de datos
- Código más mantenible

⚠️  ANTIPATRONES A EVITAR:
- Usar campos de texto en lugar de lookups
- Diccionarios de mapeo (INT_TO_GROUP, CODIGO_A_NOMBRE)
- Múltiples queries para obtener datos relacionados
- Guardar solo IDs sin integridad referencial
""")

print("="*80)
