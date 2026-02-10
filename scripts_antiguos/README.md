# Scripts Antiguos

Esta carpeta contiene scripts de utilidad, migración y verificación que fueron utilizados durante el desarrollo y configuración inicial del sistema.

## Contenido

### Scripts de Análisis
- `analizar_relacion_chats_grupo.py` - Analiza relaciones entre chats y grupos
- `analizar_requisitos_vs_actual.py` - Compara requisitos originales con implementación actual

### Scripts de Creación
- `crear_campo_contacto_chats.py` - Crea campo de contacto en tabla de chats
- `crear_contacto_auto_desde_mensaje.py` - Crea contactos automáticamente desde mensajes
- `crear_tablas_auto.py` - Script de creación automática de tablas

### Scripts de Migración
- `migrar_contactos_chats.py` - Migra contactos a nueva estructura de chats
- `migrar_grupos_booleanos_a_relaciones.py` - Migra grupos de booleanos a relaciones
- `migrar_grupo_integer_a_lookup.py` - Migra campo grupo de integer a lookup

### Scripts de Verificación
- `verificar_cambios_tabla.py` - Verifica cambios en tablas
- `verificar_campos_tablas.py` - Verifica campos de tablas
- `verificar_datos_tablas.py` - Verifica datos en tablas
- `verificar_permisos.py` - Verifica permisos de usuarios
- `verificar_usuario_grupos.py` - Verifica relación usuario-grupos

### Scripts de Visualización
- `ver_campos_tabla.py` - Muestra campos de una tabla
- `ver_dependencias.py` - Visualiza dependencias del sistema
- `ver_dependencias_campos.py` - Visualiza dependencias de campos específicos
- `ver_estado_migracion.py` - Muestra estado de migraciones

### Scripts de Utilidad
- `check_guids.py` - Verifica GUIDs en el sistema
- `check_routes.py` - Verifica rutas registradas en Flask
- `encontrar_campo_lookup.py` - Encuentra campos de tipo lookup

## Nota

Estos scripts se conservan con fines de referencia histórica. La mayoría ya cumplieron su propósito durante la fase de desarrollo inicial y migración del sistema.

**Estado:** Archivos movidos el 2026-02-08
**Razón:** Limpieza y organización del workspace principal
