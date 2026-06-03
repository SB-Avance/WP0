"""
Crear tablas personalizadas (cr321_*) en Dataverse usando la Web API.

Requisitos:
- Variables en .env o backend/.env: TENANT_ID, CLIENT_ID, CLIENT_SECRET, DATAVERSE_URL
- Permisos en Dataverse: System Customizer o superior (crear tablas y columnas)

Uso:
  python crear_tablas_dataverse.py           # Crear tablas que no existan
  python crear_tablas_dataverse.py --dry-run # Solo listar qué se crearía
  python crear_tablas_dataverse.py --list   # Listar entidades cr321_ existentes

Las relaciones (Lookup) entre tablas deben crearse después en Power Apps o con
el script/API de relaciones (OneToManyRelationship). Este script crea solo las
tablas y sus columnas escalares.
"""

import argparse
import json
import os
import sys

import msal
import requests
from dotenv import load_dotenv

# Cargar .env (raíz o backend)
for path in [
    os.path.join(os.path.dirname(__file__), "backend", ".env"),
    os.path.join(os.path.dirname(__file__), ".env"),
]:
    if os.path.isfile(path):
        load_dotenv(path)
        break

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
DATAVERSE_URL = (os.getenv("DATAVERSE_URL") or "").rstrip("/")
SCOPE = [f"{DATAVERSE_URL}/.default"]
LCID = 1033


def _label(text):
    return {
        "@odata.type": "Microsoft.Dynamics.CRM.Label",
        "LocalizedLabels": [
            {
                "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                "Label": text,
                "LanguageCode": LCID,
            }
        ],
    }


def _required_level(value="None"):
    return {
        "Value": value,
        "CanBeChanged": True,
        "ManagedPropertyLogicalName": "canmodifyrequirementlevelsettings",
    }


def get_access_token():
    """Token de acceso MSAL para Dataverse."""
    if not all([TENANT_ID, CLIENT_ID, CLIENT_SECRET, DATAVERSE_URL]):
        raise ValueError(
            "Faltan TENANT_ID, CLIENT_ID, CLIENT_SECRET o DATAVERSE_URL en .env"
        )
    authority = f"https://login.microsoftonline.com/{TENANT_ID}"
    app = msal.ConfidentialClientApplication(
        CLIENT_ID, authority=authority, client_credential=CLIENT_SECRET
    )
    result = app.acquire_token_for_client(scopes=SCOPE)
    if "access_token" in result:
        return result["access_token"]
    raise RuntimeError(result.get("error_description", "No se pudo obtener token"))


def entity_exists(token, logical_name):
    """Comprueba si existe la entidad por LogicalName."""
    url = (
        f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions(LogicalName='{logical_name}')"
    )
    r = requests.get(url, headers=_headers(token), timeout=30)
    return r.status_code == 200


def _headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0",
    }


def create_entity(
    token, schema_name, display_name, display_collection_name, description, primary_attr
):
    """Crea la entidad con solo el atributo de nombre principal."""
    payload = {
        "@odata.type": "Microsoft.Dynamics.CRM.EntityMetadata",
        "SchemaName": schema_name,
        "DisplayName": _label(display_name),
        "DisplayCollectionName": _label(display_collection_name),
        "Description": _label(description),
        "OwnershipType": "OrganizationOwned",
        "HasActivities": False,
        "HasNotes": False,
        "IsActivity": False,
        "Attributes": [
            {
                "@odata.type": "Microsoft.Dynamics.CRM.StringAttributeMetadata",
                "SchemaName": primary_attr["schema_name"],
                "DisplayName": _label(primary_attr["display_name"]),
                "Description": _label(
                    primary_attr.get("description", primary_attr["display_name"])
                ),
                "RequiredLevel": _required_level(
                    primary_attr.get("required_level", "None")
                ),
                "FormatName": {"Value": "Text"},
                "MaxLength": primary_attr.get("max_length", 100),
                "IsPrimaryName": True,
            }
        ],
    }
    url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions"
    r = requests.post(url, headers=_headers(token), json=payload, timeout=60)
    if r.status_code in (200, 204):
        return True
    print(f"  Error creando entidad {schema_name}: {r.status_code} - {r.text[:500]}")
    return False


def add_string_attribute(
    token, logical_name, schema_name, display_name, max_length=100, required="None"
):
    """Añade una columna de tipo texto."""
    payload = {
        "AttributeType": "String",
        "AttributeTypeName": {"Value": "StringType"},
        "@odata.type": "Microsoft.Dynamics.CRM.StringAttributeMetadata",
        "SchemaName": schema_name,
        "DisplayName": _label(display_name),
        "RequiredLevel": _required_level(required),
        "FormatName": {"Value": "Text"},
        "MaxLength": max_length,
    }
    url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions(LogicalName='{logical_name}')/Attributes"
    r = requests.post(url, headers=_headers(token), json=payload, timeout=30)
    if r.status_code in (200, 204):
        return True
    if (
        r.status_code == 400
        and "already exist" in r.text.lower()
        or "duplicate" in r.text.lower()
    ):
        return True  # Ya existe
    print(f"  Error añadiendo atributo {schema_name}: {r.status_code} - {r.text[:300]}")
    return False


def add_integer_attribute(
    token, logical_name, schema_name, display_name, required="None"
):
    """Añade una columna de tipo entero."""
    payload = {
        "AttributeType": "Integer",
        "AttributeTypeName": {"Value": "IntegerType"},
        "@odata.type": "Microsoft.Dynamics.CRM.IntegerAttributeMetadata",
        "SchemaName": schema_name,
        "DisplayName": _label(display_name),
        "RequiredLevel": _required_level(required),
    }
    url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions(LogicalName='{logical_name}')/Attributes"
    r = requests.post(url, headers=_headers(token), json=payload, timeout=30)
    if r.status_code in (200, 204):
        return True
    if r.status_code == 400 and (
        "already exist" in r.text.lower() or "duplicate" in r.text.lower()
    ):
        return True
    print(f"  Error añadiendo atributo {schema_name}: {r.status_code} - {r.text[:300]}")
    return False


def add_datetime_attribute(
    token, logical_name, schema_name, display_name, required="None"
):
    """Añade una columna de tipo fecha y hora."""
    payload = {
        "AttributeType": "DateTime",
        "AttributeTypeName": {"Value": "DateTimeType"},
        "@odata.type": "Microsoft.Dynamics.CRM.DateTimeAttributeMetadata",
        "SchemaName": schema_name,
        "DisplayName": _label(display_name),
        "RequiredLevel": _required_level(required),
        "Format": "DateOnly",
        "DateTimeBehavior": {"Value": "UserLocal"},
    }
    url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions(LogicalName='{logical_name}')/Attributes"
    r = requests.post(url, headers=_headers(token), json=payload, timeout=30)
    if r.status_code in (200, 204):
        return True
    if r.status_code == 400 and (
        "already exist" in r.text.lower() or "duplicate" in r.text.lower()
    ):
        return True
    print(f"  Error añadiendo atributo {schema_name}: {r.status_code} - {r.text[:300]}")
    return False


def add_boolean_attribute(
    token, logical_name, schema_name, display_name, default_value=False
):
    """Añade una columna booleana."""
    payload = {
        "AttributeType": "Boolean",
        "AttributeTypeName": {"Value": "BooleanType"},
        "@odata.type": "Microsoft.Dynamics.CRM.BooleanAttributeMetadata",
        "SchemaName": schema_name,
        "DisplayName": _label(display_name),
        "RequiredLevel": _required_level("None"),
        "DefaultValue": default_value,
    }
    url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions(LogicalName='{logical_name}')/Attributes"
    r = requests.post(url, headers=_headers(token), json=payload, timeout=30)
    if r.status_code in (200, 204):
        return True
    if r.status_code == 400 and (
        "already exist" in r.text.lower() or "duplicate" in r.text.lower()
    ):
        return True
    print(f"  Error añadiendo atributo {schema_name}: {r.status_code} - {r.text[:300]}")
    return False


# Definición de tablas a crear (sin lookups; los lookups se crean en Power Apps o después)
TABLAS = [
    {
        "logical_name": "cr321_grupo",
        "schema_name": "cr321_grupo",
        "display_name": "Grupo",
        "display_collection_name": "Grupos",
        "description": "Grupos de soporte, ventas, etc.",
        "primary": {
            "schema_name": "cr321_nombre",
            "display_name": "Nombre",
            "max_length": 100,
        },
        "extra_attrs": [
            ("cr321_idgrupo", "int", "Id grupo", {}),
            ("cr321_descripcion", "string", "Descripción", {"max_length": 500}),
        ],
    },
    {
        "logical_name": "cr321_estado",
        "schema_name": "cr321_estado",
        "display_name": "Estado",
        "display_collection_name": "Estados",
        "description": "Estados de tickets",
        "primary": {
            "schema_name": "cr321_nombre",
            "display_name": "Nombre",
            "max_length": 100,
        },
        "extra_attrs": [
            ("cr321_idestado", "int", "Id estado", {}),
            ("cr321_descripcion", "string", "Descripción", {"max_length": 500}),
        ],
    },
    {
        "logical_name": "cr321_contacto",
        "schema_name": "cr321_contacto",
        "display_name": "Contacto",
        "display_collection_name": "Contactos",
        "description": "Contactos de WhatsApp",
        "primary": {
            "schema_name": "cr321_fromnombre",
            "display_name": "Nombre origen",
            "max_length": 100,
        },
        "extra_attrs": [
            ("cr321_telefono", "string", "Teléfono", {"max_length": 20}),
            ("cr321_descripcion", "string", "Descripción", {"max_length": 500}),
            ("cr321_fechacreacion", "datetime", "Fecha creación", {}),
        ],
    },
    {
        "logical_name": "cr321_usuario",
        "schema_name": "cr321_usuario",
        "display_name": "Usuario",
        "display_collection_name": "Usuarios",
        "description": "Usuarios del sistema",
        "primary": {
            "schema_name": "cr321_nombre",
            "display_name": "Nombre",
            "max_length": 100,
        },
        "extra_attrs": [
            ("cr321_correo", "string", "Correo", {"max_length": 200}),
            ("cr321_idusuario", "int", "Id usuario", {}),
        ],
    },
    {
        "logical_name": "cr321_chatbot",
        "schema_name": "cr321_chatbot",
        "display_name": "Chatbot",
        "display_collection_name": "Chatbots",
        "description": "Configuración de menú WhatsApp",
        "primary": {
            "schema_name": "cr321_name",
            "display_name": "Nombre",
            "max_length": 100,
        },
        "extra_attrs": [
            ("cr321_active", "bool", "Activo", {}),
            ("cr321_config", "string", "Config (JSON)", {"max_length": 100000}),
            ("cr321_elemento1", "string", "Elemento 1", {"max_length": 200}),
            ("cr321_elemento2", "string", "Elemento 2", {"max_length": 200}),
            ("cr321_elemento3", "string", "Elemento 3", {"max_length": 200}),
        ],
    },
    {
        "logical_name": "cr321_ticket",
        "schema_name": "cr321_ticket",
        "display_name": "Ticket",
        "display_collection_name": "Tickets",
        "description": "Tickets de soporte",
        "primary": {
            "schema_name": "cr321_fromnombre",
            "display_name": "Nombre origen",
            "max_length": 100,
        },
        "extra_attrs": [
            ("cr321_idticket", "int", "Id ticket", {}),
            ("cr321_telefono", "string", "Teléfono", {"max_length": 20}),
            ("cr321_empresa", "string", "Empresa", {"max_length": 200}),
            ("cr321_descripcion", "string", "Descripción", {"max_length": 2000}),
            ("cr321_tipo", "int", "Tipo", {}),
            ("cr321_fechacreacion", "datetime", "Fecha creación", {}),
            ("cr321_fechaactualizacion", "datetime", "Fecha actualización", {}),
        ],
    },
    {
        "logical_name": "cr321_cotizacion",
        "schema_name": "cr321_cotizacion",
        "display_name": "Cotización",
        "display_collection_name": "Cotizaciones",
        "description": "Cotizaciones",
        "primary": {
            "schema_name": "cr321_nombre",
            "display_name": "Nombre",
            "max_length": 100,
        },
        "extra_attrs": [
            ("cr321_cliente", "string", "Cliente", {"max_length": 200}),
            ("cr321_descripcion", "string", "Descripción", {"max_length": 2000}),
            ("cr321_fecha", "datetime", "Fecha", {}),
        ],
    },
    {
        "logical_name": "cr321_usuariogrupo",
        "schema_name": "cr321_usuariogrupo",
        "display_name": "Usuario Grupo",
        "display_collection_name": "Usuario Grupos",
        "description": "Relación usuario-grupo",
        "primary": {
            "schema_name": "cr321_name",
            "display_name": "Nombre",
            "max_length": 100,
        },
        "extra_attrs": [],
    },
]


def create_table(token, defn, dry_run=False):
    """Crea una tabla y sus atributos extra."""
    logical = defn["logical_name"]
    if dry_run:
        print(
            f"  [DRY-RUN] Crear entidad: {defn['schema_name']} ({defn['display_name']})"
        )
        for attr in defn["extra_attrs"]:
            print(f"    + {attr[0]} ({attr[1]})")
        return True

    if entity_exists(token, logical):
        print(f"  Ya existe: {logical}")
        return True

    if not create_entity(
        token,
        defn["schema_name"],
        defn["display_name"],
        defn["display_collection_name"],
        defn["description"],
        defn["primary"],
    ):
        return False
    print(f"  Creada entidad: {logical}")

    for attr_schema, attr_type, display_name, opts in defn["extra_attrs"]:
        if attr_type == "string":
            add_string_attribute(
                token,
                logical,
                attr_schema,
                display_name,
                max_length=opts.get("max_length", 100),
            )
        elif attr_type == "int":
            add_integer_attribute(token, logical, attr_schema, display_name)
        elif attr_type == "datetime":
            add_datetime_attribute(token, logical, attr_schema, display_name)
        elif attr_type == "bool":
            add_boolean_attribute(token, logical, attr_schema, display_name)
    return True


def list_entities(token):
    """Lista entidades cr321_ existentes."""
    url = f"{DATAVERSE_URL}/api/data/v9.2/EntityDefinitions?$filter=startswith(LogicalName,'cr321_')&$select=LogicalName,SchemaName"
    r = requests.get(url, headers=_headers(token), timeout=30)
    if r.status_code != 200:
        print(f"Error: {r.status_code} - {r.text[:300]}")
        return
    for e in r.json().get("value", []):
        print(f"  {e.get('LogicalName')}")


def main():
    parser = argparse.ArgumentParser(description="Crear tablas cr321_* en Dataverse")
    parser.add_argument(
        "--dry-run", action="store_true", help="Solo mostrar qué se crearía"
    )
    parser.add_argument(
        "--list", action="store_true", help="Listar entidades cr321_ existentes"
    )
    args = parser.parse_args()

    if args.list:
        print("Entidades cr321_ en Dataverse:")
        token = get_access_token()
        list_entities(token)
        return

    print("=" * 60)
    print("CREAR TABLAS EN DATAVERSE (Web API)")
    print("=" * 60)
    if args.dry_run:
        print("Modo: --dry-run (no se modificará Dataverse)\n")
    print()

    try:
        token = get_access_token()
    except Exception as e:
        print(f"Error de autenticación: {e}")
        sys.exit(1)

    ok = 0
    for defn in TABLAS:
        print(f"Tabla: {defn['schema_name']}")
        if create_table(token, defn, dry_run=args.dry_run):
            ok += 1
        print()

    print("=" * 60)
    print(f"Listo. Tablas procesadas: {ok}/{len(TABLAS)}")
    print()
    print("Siguiente paso: Crear relaciones (Lookup) en Power Apps:")
    print(
        "  - cr321_ticket: cr321_grupoId -> cr321_grupo, cr321_estadoId -> cr321_estado, cr321_contactoId -> cr321_contacto"
    )
    print("  - cr321_chatbot: cr321_grupoid -> cr321_grupo")
    print(
        "  - cr321_usuariogrupo: cr321_usuarioid -> cr321_usuario, cr321_grupoid -> cr321_grupo"
    )
    print(
        "  O usar: https://make.powerapps.com -> Tablas -> Editar tabla -> Añadir columna (Tipo: Búsqueda)"
    )


if __name__ == "__main__":
    main()
