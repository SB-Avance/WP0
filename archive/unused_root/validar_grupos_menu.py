"""
Script para Validar Grupos del Menú
===================================

Valida que todos los grupo_id en el JSON del menú correspondan
a registros reales en la tabla cr321_grupos de Dataverse.
"""

import json
import os
from pathlib import Path

import requests

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

DATAVERSE_URL = os.getenv(
    "DATAVERSE_URL", "https://tu-org.crm.dynamics.com/api/data/v9.2"
)
CLIENT_ID = os.getenv("CLIENT_ID", "tu-client-id")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "tu-client-secret")
TENANT_ID = os.getenv("TENANT_ID", "tu-tenant-id")

NOMBRE_CHATBOT = "Chatbot1"


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
        "grant_type": "client_credentials",
    }

    response = requests.post(token_url, data=data)

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"Error obteniendo token: {response.text}")


def obtener_grupos_validos(headers: dict) -> dict:
    """
    Obtiene todos los grupos válidos de cr321_grupos.

    Returns:
        Dict {guid: nombre}
    """

    response = requests.get(
        f"{DATAVERSE_URL}/cr321_grupos",
        headers=headers,
        params={"$select": "cr321_grupoid,cr321_nombre,cr321_descripcion"},
    )

    if response.status_code == 200:
        grupos = {}
        for g in response.json()["value"]:
            grupos[g["cr321_grupoid"].lower()] = {
                "nombre": g.get("cr321_nombre", "Sin nombre"),
                "descripcion": g.get("cr321_descripcion", ""),
            }
        return grupos
    else:
        raise Exception(f"Error obteniendo grupos: {response.text}")


def obtener_config_chatbot(headers: dict, nombre: str) -> dict:
    """Obtiene la configuración del chatbot"""

    response = requests.get(
        f"{DATAVERSE_URL}/cr321_chatbots",
        headers=headers,
        params={
            "$filter": f"cr321_name eq '{nombre}' and cr321_active eq true",
            "$select": "cr321_config",
        },
    )

    if response.status_code == 200:
        data = response.json()["value"]
        if data:
            return json.loads(data[0]["cr321_config"])

    raise Exception(f"No se encontró chatbot activo: {nombre}")


def validar_grupos_menu(config: dict, grupos_validos: dict):
    """
    Valida todos los grupo_id del menú.

    Returns:
        (validos, invalidos, sin_grupo)
    """

    validos = []
    invalidos = []
    sin_grupo = []

    for menu in config.get("menus", []):
        for submenu in menu.get("submenus", []):
            numero = submenu.get("numero")
            nombre = submenu.get("nombre")
            grupo_id = submenu.get("grupo_id")

            if not grupo_id or grupo_id == "null" or grupo_id is None:
                sin_grupo.append(
                    {"numero": numero, "nombre": nombre, "menu": menu.get("nombre")}
                )
            else:
                # Limpiar GUID
                guid_limpio = grupo_id.strip("{}").lower()

                if guid_limpio in grupos_validos:
                    validos.append(
                        {
                            "numero": numero,
                            "nombre": nombre,
                            "menu": menu.get("nombre"),
                            "grupo_id": grupo_id,
                            "grupo_nombre": grupos_validos[guid_limpio]["nombre"],
                        }
                    )
                else:
                    invalidos.append(
                        {
                            "numero": numero,
                            "nombre": nombre,
                            "menu": menu.get("nombre"),
                            "grupo_id": grupo_id,
                        }
                    )

    return validos, invalidos, sin_grupo


# ============================================================================
# MAIN
# ============================================================================


def main():
    """Función principal"""

    print("=" * 60)
    print("VALIDACIÓN DE GRUPOS DEL MENÚ")
    print("=" * 60)
    print()

    try:
        # 1. Obtener token
        print("→ Obteniendo token...")
        token = obtener_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        print("  ✓ Token obtenido")

        # 2. Obtener grupos válidos de cr321_grupos
        print("\n→ Consultando grupos válidos en cr321_grupos...")
        grupos_validos = obtener_grupos_validos(headers)
        print(f"  ✓ {len(grupos_validos)} grupos disponibles")

        # 3. Obtener config del chatbot
        print(f"\n→ Cargando configuración de '{NOMBRE_CHATBOT}'...")
        config = obtener_config_chatbot(headers, NOMBRE_CHATBOT)
        print(f"  ✓ Configuración cargada")

        # 4. Validar grupos
        print("\n→ Validando grupos del menú...")
        validos, invalidos, sin_grupo = validar_grupos_menu(config, grupos_validos)

        # 5. Mostrar resultados
        print("\n" + "=" * 60)
        print("RESULTADOS DE VALIDACIÓN")
        print("=" * 60)

        # Grupos válidos
        if validos:
            print(f"\n✅ GRUPOS VÁLIDOS ({len(validos)}):")
            print("┌" + "─" * 58 + "┐")
            for item in validos:
                print(f"│ {item['numero']:<6} {item['nombre']:<45} │")
                print(f"│        → Grupo: {item['grupo_nombre']:<38} │")
                if item != validos[-1]:
                    print("├" + "─" * 58 + "┤")
            print("└" + "─" * 58 + "┘")

        # Grupos inválidos
        if invalidos:
            print(f"\n❌ GRUPOS INVÁLIDOS ({len(invalidos)}):")
            print("┌" + "─" * 58 + "┐")
            for item in invalidos:
                print(f"│ {item['numero']:<6} {item['nombre']:<45} │")
                print(f"│        ⚠️ GUID no existe: {item['grupo_id'][:30]:<24} │")
                if item != invalidos[-1]:
                    print("├" + "─" * 58 + "┤")
            print("└" + "─" * 58 + "┘")

            print("\n💡 SOLUCIÓN:")
            print("   1. Ejecuta: python listar_grupos_dataverse.py")
            print("   2. Copia los GUIDs correctos de cr321_grupos")
            print("   3. Actualiza el JSON en cr321_config")

        # Sin grupo
        if sin_grupo:
            print(f"\n⚪ SIN GRUPO ASIGNADO ({len(sin_grupo)}):")
            print("┌" + "─" * 58 + "┐")
            for item in sin_grupo:
                print(f"│ {item['numero']:<6} {item['nombre']:<45} │")
                print(f"│        → No requiere grupo                            │")
                if item != sin_grupo[-1]:
                    print("├" + "─" * 58 + "┤")
            print("└" + "─" * 58 + "┘")

        # Resumen
        print("\n" + "=" * 60)
        print("RESUMEN")
        print("=" * 60)
        print(f"✅ Válidos:   {len(validos)}")
        print(f"❌ Inválidos: {len(invalidos)}")
        print(f"⚪ Sin grupo: {len(sin_grupo)}")
        print(f"📊 Total:     {len(validos) + len(invalidos) + len(sin_grupo)}")

        if invalidos:
            print("\n⚠️ ACCIÓN REQUERIDA: Corregir GUIDs inválidos")
            return 1
        else:
            print("\n✅ Todos los grupos son válidos")
            return 0

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
