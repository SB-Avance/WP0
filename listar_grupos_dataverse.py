"""
Script para Listar Grupos de Dataverse
======================================

Lista todos los grupos disponibles en la tabla cr321_grupos
para obtener los GUIDs reales y actualizar el JSON.
"""

import requests
import os
import json


# ============================================================================
# CONFIGURACIÓN
# ============================================================================

DATAVERSE_URL = os.getenv("DATAVERSE_URL", "https://tu-org.crm.dynamics.com/api/data/v9.2")
CLIENT_ID = os.getenv("CLIENT_ID", "tu-client-id")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "tu-client-secret")
TENANT_ID = os.getenv("TENANT_ID", "tu-tenant-id")


# ============================================================================
# FUNCIONES
# ============================================================================

def obtener_token() -> str:
    """Obtiene token OAuth de Microsoft"""
    
    token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": f"{DATAVERSE_URL}/.default",
        "grant_type": "client_credentials"
    }
    
    response = requests.post(token_url, data=data)
    
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"Error obteniendo token: {response.text}")


def listar_grupos(headers: dict):
    """Lista todos los grupos disponibles desde cr321_grupos"""
    
    response = requests.get(
        f"{DATAVERSE_URL}/cr321_grupos",
        headers=headers,
        params={
            "$select": "cr321_grupoid,cr321_nombre,cr321_descripcion",
            "$orderby": "cr321_nombre asc"
        }
    )
    
    if response.status_code == 200:
        return response.json()["value"]
    else:
        raise Exception(f"Error obteniendo grupos: {response.text}")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Función principal"""
    
    print("="*60)
    print("GRUPOS DISPONIBLES EN DATAVERSE")
    print("="*60)
    print()
    
    try:
        # 1. Obtener token
        print("→ Obteniendo token...")
        token = obtener_token()
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        print("  ✓ Token obtenido")
        
        # 2. Listar grupos
        print("\n→ Consultando grupos...")
        grupos = listar_grupos(headers)
        
        if not grupos:
            print("  ⚠️ No se encontraron grupos")
            return
        
        print(f"  ✓ {len(grupos)} grupos encontrados\n")
        
        # 3. Mostrar grupos
        print("┌" + "─"*58 + "┐")
        print("│ GRUPOS DISPONIBLES (Tabla: cr321_grupos)                │")
        print("├" + "─"*58 + "┤")
        
        for i, grupo in enumerate(grupos, 1):
            nombre = grupo.get('cr321_nombre', 'Sin nombre')
            guid = grupo.get('cr321_grupoid', 'N/A')
            descripcion = grupo.get('cr321_descripcion', '')
            
            print(f"│ {i}. {nombre:<52} │")
            print(f"│    GUID: {guid:<44} │")
            
            if descripcion:
                # Truncar descripción si es muy larga
                desc_corta = descripcion[:50] + "..." if len(descripcion) > 50 else descripcion
                print(f"│    {desc_corta:<52} │")
            
            if i < len(grupos):
                print("├" + "─"*58 + "┤")
        
        print("└" + "─"*58 + "┘")
        
        # 4. Generar snippet JSON
        print("\n" + "="*60)
        print("SNIPPET PARA ACTUALIZAR JSON")
        print("="*60)
        print("\nCopia y pega estos GUIDs en tu JSON:\n")
        
        for grupo in grupos[:5]:  # Primeros 5 grupos
            nombre = grupo.get('cr321_nombre', 'Sin nombre').replace(' ', '_').upper()
            guid = grupo.get('cr321_grupoid', 'N/A')
            print(f'"{nombre}": "{{{guid}}}",')
        
        print("\nEjemplo de uso en ejemplo_json_dataverse.json:")
        print("─"*60)
        print("""
{
  "numero": "1.1",
  "nombre": "Incidente Técnico",
  "handler": "A001",
  "grupo_id": "{GUID-AQUÍ}",  ← Reemplazar con GUID real
  ...
}
        """)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
