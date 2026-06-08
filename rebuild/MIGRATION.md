# Migration Plan — rebuild subproject

Resumen
Este documento lista pasos prácticos y priorizados para terminar de migrar el trabajo productivo al subdirectorio `rebuild/`, validar integraciones externas y mantener el código legado archivado sin bloquear CI.

Checklist corto

- [ ] Crear rama `chore/migration-plan` (docs + scripts)
- [ ] Validar CI: excluir `archive/` (ya aplicado en pre-commit)
- [ ] Provisionar secretos en CI (Dataverse + WhatsApp)
- [ ] Añadir endpoints mínimos y tests: webhook ingest, messages, conversations
- [ ] Validar token Dataverse con `check_token_verbose.py` y health token-check
- [ ] Añadir logging, retries y timeouts para llamadas externas
- [ ] Añadir CI workflow: lint, mypy, tests, build
- [ ] Tag/release v0.1.0 y documento de despliegue

Fases detalladas

1) Preparación (inmediato)
   - Documentar plan (este archivo). Crear branch `chore/migration-plan`.
   - Confirmar que `archive/` está excluido de hooks (hecho).

2) Infra & seguridad (1-2 días)
   - Añadir secrets en GitHub Actions y/o el proveedor de CI. Recomendado: usar los siguientes nombres y mapearlos a variables de entorno en los workflows:
     - `DATAVERSE_URL` — URL base de Dataverse (ej: https://org.crm.dynamics.com)
     - `TENANT_ID` — Azure AD tenant id
     - `CLIENT_ID` — Azure AD app (client) id
     - `CLIENT_SECRET` — Azure AD app client secret (sensitive)
     - `PHONE_NUMBER_ID` — WhatsApp business phone number id
     - `WHATSAPP_ACCESS_TOKEN` — WhatsApp Graph API access token (sensitive)
     - `VERIFY_TOKEN` — Webhook verification token (used for challenge responses)
   - En los workflows, exportar estos secretos como variables de entorno para los pasos de test/ci/deploy.
   - Añadir `rebuild/.env.example` (hecho) y bloquear commit de `.env` (añadir a `.gitignore`).
   - Permisos & alcance: la app de Azure AD usada por `CLIENT_ID/CLIENT_SECRET` debe tener permisos para el recurso Dataverse. Usar el scope `{DATAVERSE_URL}/.default` en MSAL client-credentials.
   - Seguridad: no imprimir secretos en logs; rotar `CLIENT_SECRET` y `WHATSAPP_ACCESS_TOKEN` periódicamente; restringir acceso a secretos en la UI de repositorio.

3) Desarrollo incremental (iterativo)
   - Implementar y testear webhook ingest con `mocks`.
   - Implementar `DataverseClient` (token refresh) y pruebas unitarias.
   - Añadir `get_dataverse_client()` y `get_whatsapp_client()` factories (ya presentes).

4) Validación y CI (paralela)
   - Ejecutar hooks y tests en PRs pequeños.
   - Añadir integración de smoke tests que usen `mocks` en CI.

5) Hardening y producción
   - Añadir logging estructurado, retries con backoff, métricas y health endpoints.
   - Crear workflow de despliegue (build image, push, deploy).

6) Archivado del legado
   - Mantener `archive/` en repo para historial; no ejecutar hooks sobre él.
   - Opcional: mover `archive/` a repo separado si el tamaño o ruido aumenta.

   Estado del archivado

   - `archive/` contiene la mayoría del código legado y ejemplos. Se mantuvo en el repositorio para preservar historial, pero se excluye de los hooks de lint/mypy/flake8 para evitar ruido en CI.
   - Fecha de finalización: 2026-06-08 — los archivos legacy fueron consolidados en `archive/` y las configuraciones de pre-commit actualizadas.

Notas
- Priorizar tests y mocks para que la integración con MSAL/Dataverse se haga sólo en entornos controlados.
- Evitar inicializadores con efectos colaterales en import-time (seguir `_LazySettings`).
