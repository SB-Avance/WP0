"""
Global pytest fixtures and environment setup for unit tests.

Sets all required Settings fields to dummy values so tests can run
without real credentials. Must run before any whatsapp_manager imports.
"""

import os
import sys

# Ensure the package is importable
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")),
)

# Force dummy values for all required Settings fields.
# Use "or" fallback so empty CI-injected env vars are replaced too.
# pydantic-settings maps field names to uppercase env vars:
#   access_token  → ACCESS_TOKEN  (NOT WHATSAPP_ACCESS_TOKEN)
_DEFAULTS = {
    "ENVIRONMENT": "local",
    "DATAVERSE_URL": "http://fake.dataverse.test",
    "TENANT_ID": "fake-tenant-id",
    "CLIENT_ID": "fake-client-id",
    "CLIENT_SECRET": "fake-client-secret",
    "PHONE_NUMBER_ID": "fake-phone-id",
    "ACCESS_TOKEN": "fake-access-token",
    "VERIFY_TOKEN": "fake-verify-token",
}
for _key, _val in _DEFAULTS.items():
    if not os.environ.get(_key):
        os.environ[_key] = _val
