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
   - Añadir secrets en GitHub Actions (DATAVERSE_URL, TENANT_ID, CLIENT_ID, CLIENT_SECRET, PHONE_NUMBER_ID, ACCESS_TOKEN, VERIFY_TOKEN).
   - Añadir `.env.example` (hecho) y bloquear commit de `.env`.

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

Notas
- Priorizar tests y mocks para que la integración con MSAL/Dataverse se haga sólo en entornos controlados.
- Evitar inicializadores con efectos colaterales en import-time (seguir `_LazySettings`).
