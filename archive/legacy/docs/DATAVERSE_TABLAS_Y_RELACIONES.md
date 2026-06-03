# Tablas de Dataverse y Relaciones

Resumen de las tablas personalizadas (`cr321_*`) usadas en el proyecto y sus relaciones, extraído del código y documentación.

## Crear tablas desde código

Para crear las tablas en Dataverse desde este proyecto:

```bash
python crear_tablas_dataverse.py           # Crear tablas que no existan
python crear_tablas_dataverse.py --dry-run # Solo simular (no escribe en Dataverse)
python crear_tablas_dataverse.py --list    # Listar entidades cr321_ existentes
```

Requisitos: `.env` o `backend/.env` con `TENANT_ID`, `CLIENT_ID`, `CLIENT_SECRET`, `DATAVERSE_URL`. El script crea las tablas y columnas escalares; las **relaciones (Lookup)** deben configurarse después en [Power Apps](https://make.powerapps.com) (Tablas → Editar tabla → Añadir columna → Tipo: Búsqueda).

---

## Tablas (entidades)

| Tabla (EntitySet)   | Descripción                    | PK / Campos principales |
|---------------------|--------------------------------|--------------------------|
| **cr321_grupos**    | Grupos de soporte/ventas       | `cr321_grupoid` (GUID), `cr321_nombre`, `cr321_idgrupo`, `cr321_tipo`, `cr321_descripcion` |
| **cr321_chatbots**  | Configuración de menú WhatsApp | `cr321_chatbotid`, `cr321_name`, `cr321_active`, `cr321_config` (JSON), `cr321_elemento1`-5, **cr321_grupoid** (Lookup → grupo) |
| **cr321_tickets**   | Tickets de soporte             | `cr321_ticketid`, `cr321_idticket`, `cr321_fromnombre`, `cr321_telefono`, `cr321_empresa`, `cr321_descripcion`, `cr321_tipo`, **cr321_grupoId** (→ grupo), **cr321_estadoId** (→ estado), **cr321_contactoId** (→ contacto) |
| **cr321_estados**   | Estados de tickets             | `cr321_estadoid`, `cr321_idestado`, `cr321_nombre`, `cr321_descripcion` |
| **cr321_contactos** | Contactos WhatsApp             | `cr321_contactoid`, `cr321_fromnombre`, `cr321_telefono`, `cr321_descripcion`, `cr321_fechacreacion` |
| **cr321_cotizacions** | Cotizaciones                 | `cr321_nombre`, `cr321_cliente`, `cr321_descripcion`, `cr321_fecha` |
| **cr321_usuarios**  | Usuarios del sistema           | `cr321_usuariosid`, `cr321_nombre`, `cr321_correo`, `cr321_idusuario`, `cr321_rol` |
| **cr321_usuariogrupos** | Asignación usuario–grupo (N:N) | `cr321_usuariogruposid`, **cr321_usuarioid** (→ usuario), **cr321_grupoid** (→ grupo) |

---

## Relaciones (Lookups)

```
                    ┌─────────────────┐
                    │ cr321_estados   │
                    │ (Estados)       │
                    └────────▲────────┘
                             │ cr321_estadoId
                    ┌────────┴────────┐
                    │                 │
┌───────────────────┴───┐   ┌─────────┴────────────┐
│ cr321_grupos          │   │ cr321_tickets        │
│ (Grupos)              │◄──│ (Tickets)            │
└──────────▲────────────┘   │ cr321_grupoId        │
           │                │ cr321_contactoId     │
           │                └──────────┬──────────┘
           │ cr321_grupoid              │
           │                ┌──────────▼──────────┐
┌──────────┴────────────┐   │ cr321_contactos      │
│ cr321_chatbots        │   │ (Contactos WhatsApp) │
│ (Menú / Chatbots)     │   └─────────────────────┘
└───────────────────────┘

           ┌─────────────────┐
           │ cr321_grupos    │
           └────────▲────────┘
                    │ cr321_grupoid
           ┌───────┴────────┐
           │ cr321_usuariogrupos │  cr321_usuarioid
           │ (Usuario-Grupo)    │──────────────► cr321_usuarios
           └───────────────────┘
```

### Detalle por tabla

| Desde (tabla)       | Campo Lookup        | Hacia (tabla)   | Descripción              |
|---------------------|---------------------|------------------|--------------------------|
| cr321_chatbots      | cr321_grupoid       | cr321_grupos     | Grupo asignado al chatbot |
| cr321_tickets       | cr321_grupoId       | cr321_grupos     | Grupo del ticket          |
| cr321_tickets       | cr321_estadoId      | cr321_estados    | Estado del ticket         |
| cr321_tickets       | cr321_contactoId    | cr321_contactos  | Contacto que abre ticket  |
| cr321_usuariogrupos | cr321_grupoid       | cr321_grupos     | Grupo del usuario         |
| cr321_usuariogrupos | cr321_usuarioid     | cr321_usuarios   | Usuario del grupo         |

---

## Notas de API (EntitySet en URLs)

En las URLs de la API de Dataverse se usan estos **conjuntos de entidad** (pueden variar según el esquema):

- Grupos: `cr321_grupos` o `cr321_grups` (según referencia en código)
- Tickets: `cr321_ticketses`
- Usuarios: `cr321_usuarioses` (expand/bind)
- Resto: `cr321_chatbots`, `cr321_estados`, `cr321_contactos`, `cr321_cotizacions`, `cr321_usuariogrupos`

---

## Diagrama gráfico

En este mismo directorio:

- **dataverse_relaciones_graphviz.dot** – Código Graphviz del diagrama.
- **dataverse_relaciones.svg** – Diagrama en SVG (incluido; para versión con Graphviz usar el .dot).
- **dataverse_relaciones.png** – Opcional: generar con `dot -Tpng` si tienes Graphviz instalado.

Para regenerar las imágenes (con Graphviz instalado):

```bash
cd docs
dot -Tsvg dataverse_relaciones_graphviz.dot -o dataverse_relaciones.svg
dot -Tpng dataverse_relaciones_graphviz.dot -o dataverse_relaciones.png
```

En PowerShell:

```powershell
dot -Tsvg docs\dataverse_relaciones_graphviz.dot -o docs\dataverse_relaciones.svg
dot -Tpng docs\dataverse_relaciones_graphviz.dot -o docs\dataverse_relaciones.png
```
