# Agregar Campo de Relación: Contacto → Chats

## 📋 Objetivo
Agregar el campo `cr321_contactoId` (Lookup) a la tabla `cr321_adatawp0` para relacionar mensajes de WhatsApp con contactos mediante una relación directa en Dataverse.

## 🎯 Cambio Implementado

### Campo Nuevo: `cr321_contactoId`
- **Tabla**: `cr321_adatawp0` (Chats WhatsApp)
- **Tipo**: Búsqueda (Lookup)
- **Tabla relacionada**: `cr321_contacto`
- **Obligatorio**: No
- **Descripción**: Contacto relacionado por teléfono

### Relación
- **Nombre**: `cr321_adatawp0_contacto`
- **Tipo**: Muchos a Uno (N:1)
- **Descripción**: Múltiples mensajes pueden pertenecer a un contacto

---

## 📝 Pasos para Crear el Campo en Dataverse

### 1. Acceder a la Tabla
1. Ir a: https://make.powerapps.com
2. Navegar a: **Tablas** → Buscar `cr321_adatawp0`
3. Abrir la tabla y seleccionar **Columnas**

### 2. Agregar Campo de Búsqueda
1. Clic en **+ Nueva columna**
2. Completar:
   - **Nombre para mostrar**: `Contacto`
   - **Nombre**: `cr321_contactoId` (se generará automáticamente)
   - **Tipo de datos**: **Búsqueda**
   - **Tabla relacionada**: `cr321_contacto`
   - **Obligatorio**: No
   - **Descripción**: `Contacto relacionado por teléfono`

3. Clic en **Guardar**

### 3. Publicar Cambios
1. Clic en **Publicar** en la parte superior
2. Esperar confirmación

---

## 💻 Uso en el Código

### Crear/Actualizar Mensaje con Contacto

```python
import requests

# Buscar contacto por teléfono
telefono = "+573001234567"
contacto_url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_contactos?$filter=cr321_telefono eq '{telefono}'"
contacto_response = requests.get(contacto_url, headers=headers)
contactos = contacto_response.json().get("value", [])

if contactos:
    contacto_id = contactos[0]["cr321_contactoid"]
    
    # Crear mensaje con relación al contacto
    payload = {
        "cr321_name": f"Mensaje de {telefono}",
        "cr321_from": telefono,
        "cr321_body": "Hola, necesito ayuda",
        "cr321_timestamp": "2026-02-08T10:00:00Z",
        "cr321_type": 462410000,  # Texto
        "cr321_direction": 462410000,  # Entrante
        "cr321_contactoId@odata.bind": f"/cr321_contactos({contacto_id})"
    }
    
    url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s"
    response = requests.post(url, json=payload, headers=headers)
```

### Obtener Mensajes con Datos del Contacto (Expand)

```python
# Obtener mensajes expandiendo información del contacto
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s"
params = {
    "$expand": "cr321_contactoId($select=cr321_nombre,cr321_telefono,cr321_email,cr321_empresa)",
    "$orderby": "cr321_timestamp desc",
    "$top": 50
}

response = requests.get(url, params=params, headers=headers)
mensajes = response.json().get("value", [])

for mensaje in mensajes:
    contacto = mensaje.get("cr321_contactoId", {})
    print(f"Mensaje de: {contacto.get('cr321_nombre', 'Sin contacto')}")
    print(f"Teléfono: {mensaje['cr321_from']}")
    print(f"Empresa: {contacto.get('cr321_empresa', 'N/A')}")
```

### Filtrar Mensajes de un Contacto Específico

```python
# Opción 1: Filtrar por GUID del contacto (más eficiente)
contacto_id = "12345678-1234-1234-1234-123456789abc"
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s"
params = {
    "$filter": f"_cr321_contactoid_value eq {contacto_id}",
    "$orderby": "cr321_timestamp desc"
}

# Opción 2: Filtrar por teléfono (alternativa)
telefono = "+573001234567"
url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s"
params = {
    "$filter": f"cr321_from eq '{telefono}'",
    "$orderby": "cr321_timestamp desc"
}

response = requests.get(url, params=params, headers=headers)
```

---

## 🔄 Migración de Datos Existentes

### Script para Asociar Mensajes con Contactos

```python
"""
Script para asociar mensajes existentes con contactos basándose en el teléfono
"""
import requests
from backend.config import DATAVERSE_URL, get_headers

def migrar_mensajes_a_contactos():
    """Asocia mensajes de WhatsApp con contactos existentes"""
    headers = get_headers()
    
    # 1. Obtener todos los contactos
    print("📋 Obteniendo contactos...")
    contactos_url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_contactos?$select=cr321_contactoid,cr321_telefono"
    contactos_response = requests.get(contactos_url, headers=headers)
    contactos = contactos_response.json().get("value", [])
    
    # Crear diccionario teléfono -> contacto_id
    telefono_a_contacto = {
        c["cr321_telefono"]: c["cr321_contactoid"] 
        for c in contactos
    }
    
    print(f"✅ {len(telefono_a_contacto)} contactos encontrados")
    
    # 2. Obtener mensajes sin contacto asignado
    print("\n📨 Obteniendo mensajes sin contacto...")
    mensajes_url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s?$filter=_cr321_contactoid_value eq null&$select=cr321_adatawp0id,cr321_from"
    mensajes_response = requests.get(mensajes_url, headers=headers)
    mensajes = mensajes_response.json().get("value", [])
    
    print(f"📊 {len(mensajes)} mensajes sin contacto")
    
    # 3. Asociar mensajes con contactos
    actualizados = 0
    sin_contacto = 0
    
    for mensaje in mensajes:
        telefono = mensaje["cr321_from"]
        mensaje_id = mensaje["cr321_adatawp0id"]
        
        if telefono in telefono_a_contacto:
            contacto_id = telefono_a_contacto[telefono]
            
            # Actualizar mensaje con contacto
            update_url = f"{DATAVERSE_URL}/api/data/v9.2/cr321_adatawp0s({mensaje_id})"
            payload = {
                "cr321_contactoId@odata.bind": f"/cr321_contactos({contacto_id})"
            }
            
            response = requests.patch(update_url, json=payload, headers=headers)
            
            if response.status_code == 204:
                actualizados += 1
                if actualizados % 10 == 0:
                    print(f"   ✓ {actualizados} mensajes actualizados...")
            else:
                print(f"   ❌ Error al actualizar mensaje {mensaje_id}: {response.text}")
        else:
            sin_contacto += 1
    
    print(f"\n✅ Migración completada:")
    print(f"   - Mensajes actualizados: {actualizados}")
    print(f"   - Mensajes sin contacto: {sin_contacto}")
    
    if sin_contacto > 0:
        print(f"\n💡 Sugerencia: Crear contactos para los {sin_contacto} teléfonos restantes")

if __name__ == "__main__":
    migrar_mensajes_a_contactos()
```

---

## ✅ Beneficios

1. **Relación directa en Dataverse**: Mejor integridad de datos
2. **Queries más eficientes**: Uso de `$expand` para obtener datos relacionados
3. **Filtrado mejorado**: Filtrar por GUID es más rápido que por string
4. **Navegación bidireccional**: Ver mensajes desde contacto y viceversa
5. **Reportes más fáciles**: Power BI puede usar la relación directamente

---

## 📊 Verificación

```python
# Verificar que el campo existe
url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions(LogicalName='cr321_adatawp0')/Attributes"
response = requests.get(url, headers=headers)
atributos = response.json().get("value", [])

campo_contacto = [a for a in atributos if a.get("LogicalName") == "cr321_contactoid"]
if campo_contacto:
    print("✅ Campo cr321_contactoId existe en cr321_adatawp0")
else:
    print("❌ Campo cr321_contactoId NO existe")
```

---

## 📝 Notas Importantes

- ⚠️ El campo es **opcional** para mantener compatibilidad con mensajes antiguos
- 💡 Se recomienda ejecutar el script de migración después de crear el campo
- 🔄 Los nuevos mensajes deben asociarse automáticamente con contactos existentes
- 📱 Si no existe un contacto para un teléfono, el campo queda vacío (null)

---

## 🔗 Archivos Relacionados

- Estructura actualizada: [BACKUP_ESTRUCTURA_COMPLETA.json](BACKUP_ESTRUCTURA_COMPLETA.json)
- Tabla contactos: Ver sección `cr321_contacto` en el backup
- Tabla chats: Ver sección `cr321_adatawp0` en el backup
