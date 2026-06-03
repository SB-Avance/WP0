# Documentación Dataverse del Proyecto

## Índice
1. Introducción y Arquitectura
2. Campos y Tablas en Dataverse
3. Ejemplos de Uso y Validación
4. Relación JSON ↔ Tabla cr321_grupos
5. Resultados de Pruebas Backend
6. Mapa de relaciones entre archivos

---

## 1. Introducción y Arquitectura

### Conexión con Tabla cr321_grupos

El campo `grupo_id` en el JSON debe contener GUIDs reales de la tabla `cr321_grupos` de Dataverse. Esto garantiza:
- Integridad referencial
- Grupos válidos y activos
- Correcta asignación de tickets

#### Arquitectura de Conexión
(ver NOTAS_GRUPOS_DATAVERSE.md para diagrama)

---

## 2. Campos y Tablas en Dataverse

### Campos que YA EXISTEN (no crear nuevos)
En la tabla `cr321_chatbots` ya tienes estos campos disponibles:
- cr321_config    (Texto)  - Para código del handler
- cr321_grupoid   (Lookup) - Para GUID del grupo asignado
- cr321_elemento1 (Texto)  - Nombre visible en menú

#### Ejemplo de uso:
- cr321_elemento1: "Incidente Técnico"      -- Texto visible
- cr321_config:    "A001"                   -- Código del handler
- cr321_grupoid:   {GUID-SOPORTE-TI}        -- Grupo destino

---

## 3. Ejemplos de Uso y Validación

### Validación de grupos en JSON
Al inicializar el sistema, se valida que todos los `grupo_id` del menú existan en `cr321_grupos`.

#### Ejemplo de validación en Python:
```python
response = requests.get(f"{DATAVERSE_URL}/cr321_grupos")
grupos_validos = {g['cr321_grupoid']: g['cr321_nombre'] for g in response.json()["value"]}
for menu in self.config_menu.menus:
    for submenu in menu.get('submenus', []):
        grupo_id = submenu.get('grupo_id')
        if grupo_id and grupo_id not in grupos_validos:
            print(f"⚠️ GUID inválido: {grupo_id}")
```

---

## 4. Relación JSON ↔ Tabla cr321_grupos

### Ejemplo de relación
```json
{
  "numero": "1.1",
  "nombre": "Incidente Técnico",
  "handler": "A001",
  "grupo_id": "{067c7ba2-9f03-f111-8d07-7ced8}"
}
```
Se conecta con:
- Tabla cr321_grupos
- cr321_grupoid: 067c7ba2-9f03-f111-8d07-7ced8

---

## 5. Resultados de Pruebas Backend

- Servidor Flask: Operacional
- 14 de 15 Blueprints funcionando
- Chats Extended: 6 endpoints activos
- Dashboard: 6 endpoints activos
- Estados: API completamente funcional
- Sin credenciales Dataverse: Error 400 esperado en grupos

---

## 6. Mapa de relaciones entre archivos

El archivo central es `backend/back.py`, que importa todos los módulos de la API y la configuración. `backend/goot.py` es el núcleo de utilidades y configuración, usado por casi todos los módulos. Cada archivo en `backend/api/` (como `auth.py`, `users.py`, `grupos.py`, etc.) depende de `goot.py` y, en muchos casos, de otros módulos de la API.

### Diagrama de dependencias (texto):

- backend/back.py
  - backend/goot.py
  - backend/api/auth.py
  - backend/api/users.py
  - backend/api/messages.py
  - backend/api/conversations.py
  - backend/api/webhook.py
  - backend/api/reportes.py
  - backend/api/settings.py
  - backend/api/grupos.py
  - backend/api/estados.py
  - backend/api/tickets.py
  - backend/api/usuario_grupos.py
  - backend/api/chatbots.py
  - backend/api/templates.py
  - backend/api/whatsapp_accounts.py
  - backend/api/chats_extended.py
  - backend/api/dashboard.py

Todos los módulos de la API dependen de backend/goot.py.

---

**Fin del documento**
