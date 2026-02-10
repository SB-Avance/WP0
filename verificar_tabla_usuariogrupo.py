"""
Verificar el nombre correcto de la tabla Usuario-Grupo en Dataverse
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from goot import get_token, DATAVERSE_URL
import requests

def listar_tablas_usuario_grupo():
    """Probar diferentes nombres posibles para la tabla Usuario-Grupo"""
    token = get_token()
    if not token:
        print("❌ No se pudo autenticar")
        return
    
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    
    # Posibles nombres de la tabla
    nombres_posibles = [
        "cr321_usuariogrupos",
        "cr321_usuario_grupos",
        "cr321_usuario_gruposes",
        "cr321_usuariogrupo",
        "cr321_usuariosgrupos",
        "cr321_usuarios_grupos"
    ]
    
    print("\n🔍 Probando diferentes nombres de tabla...\n")
    
    tabla_correcta = None
    
    for nombre in nombres_posibles:
        print(f"   Probando: {nombre}...", end=" ")
        test_url = f"{DATAVERSE_URL}/api/data/v9.2/{nombre}?$top=1"
        
        try:
            response = requests.get(test_url, headers=headers)
            
            if response.status_code == 200:
                print(f"✅ ENCONTRADA")
                tabla_correcta = nombre
                
                # Obtener estructura
                data = response.json()
                records = data.get("value", [])
                
                if records:
                    print(f"      Registros: {len(records)}")
                    print(f"      Campos:")
                    for key in sorted(records[0].keys()):
                        if not key.startswith("@"):
                            print(f"         - {key}")
                else:
                    print(f"      ⚠️ Tabla vacía")
                
                # Intentar consultar con expand
                print(f"\n   🧪 Probando con $expand...")
                expand_url = f"{DATAVERSE_URL}/api/data/v9.2/{nombre}?$top=1"
                expand_url += "&$expand=cr321_usuarioid($select=cr321_nombre),cr321_grupoid($select=cr321_nombre)"
                
                expand_response = requests.get(expand_url, headers=headers)
                if expand_response.status_code == 200:
                    print(f"      ✅ $expand funciona")
                else:
                    print(f"      ⚠️ $expand error {expand_response.status_code}")
                    print(f"         {expand_response.text[:300]}")
                
                break
            elif response.status_code == 404:
                print(f"❌ No existe")
            else:
                print(f"⚠️ Error {response.status_code}")
        except Exception as e:
            print(f"⚠️ Excepción: {str(e)[:50]}")
    
    if not tabla_correcta:
        print("\n❌ Ningún nombre probado existe")
    else:
        print(f"\n✅ Nombre correcto: {tabla_correcta}")
    
    return tabla_correcta

if __name__ == "__main__":
    tabla = listar_tablas_usuario_grupo()
    
    if tabla:
        print(f"\n\n🔬 Obteniendo metadatos de {tabla}...")
        token = get_token()
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
        
        # Obtener definición de la entidad
        metadata_url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions(LogicalName='{tabla}')"
        metadata_url += "?$select=LogicalName,SchemaName&$expand=Attributes($select=LogicalName,AttributeType),ManyToOneRelationships($select=ReferencedEntity,ReferencingAttribute,SchemaName)"
        
        try:
            response = requests.get(metadata_url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                
                print(f"\n📊 Relaciones Many-to-One (Lookups):")
                relationships = data.get("ManyToOneRelationships", [])
                for rel in relationships:
                    schema = rel.get("SchemaName", "")
                    if "usuario" in schema.lower() or "grup" in schema.lower():
                        print(f"\n   Schema: {schema}")
                        print(f"   Tabla referenciada: {rel.get('ReferencedEntity')}")
                        print(f"   Campo lookup: {rel.get('ReferencingAttribute')}")
            else:
                print(f"❌ Error {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
