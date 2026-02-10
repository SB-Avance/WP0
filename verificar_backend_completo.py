"""
Verificar todas las tablas del backend y su arquitectura
"""
import os
import re
from pathlib import Path

print("="*80)
print("VERIFICACION COMPLETA DEL BACKEND")
print("="*80)

# Directorio backend
backend_dir = Path("c:/VS/BIN/backend")

# Patrones a buscar
tablas_pattern = re.compile(r'cr321_\w+(?:es|s)')  # Nombres de tablas
expand_pattern = re.compile(r'\$expand=')
odata_bind_pattern = re.compile(r'@odata\.bind')
diccionario_pattern = re.compile(r'(INT_TO_|_TO_INT|CODIGO_A_|_A_CODIGO|GROUP_TO|TO_GROUP)\w+\s*=\s*\{')

archivos_python = list(backend_dir.rglob("*.py"))

print(f"\n✅ Total archivos Python: {len(archivos_python)}")

# Análisis por archivo
print("\n" + "="*80)
print("ANALISIS POR ARCHIVO")
print("="*80)

resultados = []

for archivo in sorted(archivos_python):
    if "__pycache__" in str(archivo):
        continue
        
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Buscar tablas
        tablas = set(tablas_pattern.findall(contenido))
        
        # Buscar $expand
        usa_expand = len(expand_pattern.findall(contenido))
        
        # Buscar @odata.bind
        usa_odata_bind = len(odata_bind_pattern.findall(contenido))
        
        # Buscar diccionarios hardcoded
        diccionarios = diccionario_pattern.findall(contenido)
        
        if tablas or usa_expand or usa_odata_bind or diccionarios:
            rel_path = archivo.relative_to(backend_dir)
            
            resultado = {
                "archivo": str(rel_path),
                "tablas": sorted(list(tablas)),
                "expand_count": usa_expand,
                "odata_bind_count": usa_odata_bind,
                "diccionarios": diccionarios,
                "lineas": len(contenido.split('\n'))
            }
            
            resultados.append(resultado)
            
            print(f"\n📄 {rel_path}")
            print(f"   Líneas: {resultado['lineas']}")
            
            if tablas:
                print(f"   Tablas: {', '.join(sorted(tablas))}")
            
            if usa_expand:
                print(f"   ✅ Usa $expand: {usa_expand} veces")
            
            if usa_odata_bind:
                print(f"   ✅ Usa @odata.bind: {usa_odata_bind} veces")
            
            if diccionarios:
                print(f"   ⚠️  Diccionarios hardcoded: {', '.join(diccionarios)}")
    
    except Exception as e:
        print(f"Error leyendo {archivo}: {e}")

# Resumen de tablas
print("\n" + "="*80)
print("RESUMEN DE TABLAS USADAS")
print("="*80)

todas_tablas = set()
for r in resultados:
    todas_tablas.update(r["tablas"])

print(f"\n✅ Total tablas únicas: {len(todas_tablas)}")
for tabla in sorted(todas_tablas):
    archivos_usan = [r["archivo"] for r in resultados if tabla in r["tablas"]]
    print(f"\n   {tabla}:")
    for arch in archivos_usan:
        print(f"      - {arch}")

# Resumen de lookups
print("\n" + "="*80)
print("RESUMEN DE USO DE LOOKUPS")
print("="*80)

total_expand = sum(r["expand_count"] for r in resultados)
total_odata = sum(r["odata_bind_count"] for r in resultados)

print(f"\n✅ Total usos de $expand: {total_expand}")
print(f"✅ Total usos de @odata.bind: {total_odata}")

if total_expand > 0:
    print("\n✅ El backend USA navegación de lookups con $expand")
else:
    print("\n⚠️  El backend NO usa navegación de lookups con $expand")

if total_odata > 0:
    print("✅ El backend USA OData binding para crear relaciones")
else:
    print("⚠️  El backend NO usa OData binding para crear relaciones")

# Resumen de diccionarios
print("\n" + "="*80)
print("DICCIONARIOS HARDCODED (LEGACY)")
print("="*80)

archivos_con_diccionarios = [r for r in resultados if r["diccionarios"]]

if archivos_con_diccionarios:
    print(f"\n⚠️  {len(archivos_con_diccionarios)} archivos con diccionarios hardcoded:")
    for r in archivos_con_diccionarios:
        print(f"\n   {r['archivo']}:")
        for d in r["diccionarios"]:
            print(f"      - {d}...")
    
    print("\n⚠️  RECOMENDACION:")
    print("   Refactorizar para usar lookups con $expand en lugar de diccionarios")
else:
    print("\n✅ Sin diccionarios hardcoded - Arquitectura limpia")

# Verificar archivos específicos
print("\n" + "="*80)
print("VERIFICACION DE ARCHIVOS CLAVE")
print("="*80)

archivos_clave = {
    "back.py": "Aplicación principal Flask",
    "api/usuario_grupos.py": "Relaciones usuario-grupo",
    "api/grupos.py": "Gestión de grupos",
    "api/messages.py": "Mensajes WhatsApp",
    "api/conversations.py": "Conversaciones"
}

for nombre, descripcion in archivos_clave.items():
    encontrado = [r for r in resultados if nombre in r["archivo"]]
    if encontrado:
        r = encontrado[0]
        print(f"\n✅ {nombre} - {descripcion}")
        print(f"   $expand: {r['expand_count']} | @odata.bind: {r['odata_bind_count']}")
        
        if r["diccionarios"]:
            print(f"   ⚠️  Diccionarios: {', '.join(r['diccionarios'])}")
        else:
            print(f"   ✅ Sin diccionarios hardcoded")
    else:
        print(f"\n⚠️  {nombre} NO encontrado")

print("\n" + "="*80)
print("CONCLUSIONES")
print("="*80)

if total_expand > 0 and total_odata > 0 and not archivos_con_diccionarios:
    print("\n✅ ARQUITECTURA CORRECTA:")
    print("   - Usa lookups con navegación $expand")
    print("   - Usa OData binding para integridad referencial")
    print("   - Sin diccionarios hardcoded")
    print("   - Backend siguiendo mejores prácticas de Dataverse")
elif archivos_con_diccionarios:
    print("\n⚠️  ARQUITECTURA MIXTA:")
    print("   - Algunos archivos usan lookups correctamente")
    print("   - Algunos archivos tienen diccionarios hardcoded")
    print("   - ACCION: Refactorizar archivos con diccionarios")
else:
    print("\n⚠️  ARQUITECTURA LEGACY:")
    print("   - No usa lookups correctamente")
    print("   - ACCION: Migrar a arquitectura lookup completa")

print("\n" + "="*80)
