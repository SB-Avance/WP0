"""
Corregir asignación de grupo del usuario 0006
Cambiar código '0005' (no existe) a '0004' (Contabilidad)
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from goot import get_token, DATAVERSE_URL
import requests

token = get_token()
headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

usuario_id = "e45580f3-59fa-f011-8406-002248df122f"

print("\n=== CORRIGIENDO GRUPO USUARIO 0006 ===\n")

# Paso 1: Buscar el registro actual
print("1. Buscando registro actual...")
url_buscar = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuariogrupos"
url_buscar += f"?$filter=_cr321_usuarioid_value eq {usuario_id}"
url_buscar += "&$select=cr321_usuariogrupoid,cr321_usuariogrupo1"

response = requests.get(url_buscar, headers=headers)

if response.status_code != 200:
    print(f"❌ Error al buscar: {response.status_code}")
    exit(1)

data = response.json()
registros = data.get("value", [])

if not registros:
    print("❌ No se encontró registro para usuario 0006")
    exit(1)

registro = registros[0]
registro_id = registro.get("cr321_usuariogrupoid")
codigo_actual = registro.get("cr321_usuariogrupo1")

print(f"✅ Registro encontrado:")
print(f"   ID: {registro_id}")
print(f"   Código actual: '{codigo_actual}'")

# Paso 2: Actualizar a código válido
nuevo_codigo = "0004"  # Contabilidad
print(f"\n2. Actualizando a código '{nuevo_codigo}' (Contabilidad)...")

url_actualizar = f"{DATAVERSE_URL}/api/data/v9.2/cr321_usuariogrupos({registro_id})"
headers_update = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "If-Match": "*"
}

payload = {
    "cr321_usuariogrupo1": nuevo_codigo
}

response_update = requests.patch(url_actualizar, json=payload, headers=headers_update)

if response_update.status_code == 204:
    print("✅ Actualización exitosa")
    
    # Verificar cambio
    print("\n3. Verificando cambio...")
    response_verify = requests.get(url_buscar, headers=headers)
    if response_verify.status_code == 200:
        registro_nuevo = response_verify.json().get("value", [])[0]
        codigo_nuevo = registro_nuevo.get("cr321_usuariogrupo1")
        print(f"✅ Código actualizado: '{codigo_nuevo}'")
        print(f"\n✅ Usuario 0006 ahora pertenece al grupo Contabilidad")
elif response_update.status_code == 412:
    print("⚠️  Error 412: El registro fue modificado por otro proceso")
    print("   Intenta de nuevo")
else:
    print(f"❌ Error al actualizar: {response_update.status_code}")
    print(f"   {response_update.text[:300]}")
