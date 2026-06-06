# WhatsApp Manager (rebuild)

Resumen rápido
- FastAPI service to receive WhatsApp webhook events, persist messages in MS Dataverse and send replies via WhatsApp Graph API.
- Local-friendly: in-memory mocks used when `ENVIRONMENT=local`.

Requisitos
- Python 3.11+
- Virtual environment (recommended)

Instalación (dev)
```powershell
python -m venv .venv
. .venv\Scripts\Activate.ps1
pip install -r rebuild/requirements.txt
pip install -r requirements-dev.txt
```

Variables de entorno
Rellena `.env` a partir de `rebuild/.env.example`.
- `ENVIRONMENT` — `local` | `production` (default: `local`)
- `DATAVERSE_URL` — URL base de Dataverse (e.g. https://org.crm.dynamics.com)
- `TENANT_ID` — Azure tenant id
- `CLIENT_ID` — MSAL client id
- `CLIENT_SECRET` — MSAL client secret
- `PHONE_NUMBER_ID` — WhatsApp Business phone id
- `ACCESS_TOKEN` — token de acceso (opcional para mocks)
- `VERIFY_TOKEN` — token para la verificación del webhook

Ejecutar localmente
```powershell
cd rebuild
. .venv\Scripts\Activate.ps1
.\run_local.ps1
```

Tests
```powershell
pip install -r rebuild/requirements.txt
pip install -r requirements-dev.txt
pytest -q rebuild/tests
```

Notas
- No incluyas secretos en el repositorio. Usa `rebuild/.env.example` como plantilla.
- PowerShell scripts usan `try/catch` y no contienen `; true` de Bash.

Estructura relevante
- `rebuild/src/whatsapp_manager/` — código fuente
- `rebuild/tests/` — suite de pruebas
- `rebuild/scripts/` — helpers y scripts de desarrollo

Contacto
- Equipo/maintainers: revisa `CHANGELOG.md` y los archivos en `archive/` para migrar código legado.
# Rebuild - FastAPI + Dataverse skeleton

Estructura mínima para comenzar la migración desde el backend existente hacia una API modular usando Dataverse.

Instrucciones rápidas:

1. Copiar las variables de entorno necesarias en un `.env`:

```
DATAVERSE_URL=
TENANT_ID=
CLIENT_ID=
CLIENT_SECRET=
PHONE_NUMBER_ID=
ACCESS_TOKEN=
VERIFY_TOKEN=
```

2. Levantar localmente con Docker Compose:

```bash
docker-compose up --build
```
