# Changelog

All notable changes to this repository are documented in this file.

## Unreleased - 2026-06-05

- Archive: moved legacy and unused root scripts into `archive/unused_root/` and `archive/legacy/` to tidy repository layout. (see PR #1)
- Rebuild service: created a canonical FastAPI service under `rebuild/` and implemented lazy initialization for runtime `Settings` and clients to avoid import-time side effects.
- Tests & typing: fixed pytest collection issues and mypy typing problems; added `# type: ignore[import]` for `msal` where stubs are missing.
- CI: bumped `rebuild` GitHub Actions workflow to use `python-version: '3.12'` and ensured the pipeline installs test and typing tools (`pytest`, `mypy`, `types-requests`). (see PR #3)
- Pydantic: prepared code for migration to `pydantic v2` and added `pydantic-settings` to `rebuild/requirements.txt`; audit of validators/types in `rebuild/src` started.

### Notes

- Key branches: `fix/lazy-settings-startup` (lazy Settings + clients), `ci/python-3-12` (CI bump). Both branches were merged/closed.
- Actions performed: ran local `pytest` and `mypy`, fixed failing tests, pushed fixes and monitored CI until green.

If you want a release entry, tell me the version string and I will create a tagged release and update `CHANGELOG.md` accordingly.
