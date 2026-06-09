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

# Provide dummy values for all required Settings fields
os.environ.setdefault("ENVIRONMENT", "local")
os.environ.setdefault("DATAVERSE_URL", "http://fake.dataverse.test")
os.environ.setdefault("TENANT_ID", "fake-tenant-id")
os.environ.setdefault("CLIENT_ID", "fake-client-id")
os.environ.setdefault("CLIENT_SECRET", "fake-client-secret")
os.environ.setdefault("PHONE_NUMBER_ID", "fake-phone-id")
os.environ.setdefault("WHATSAPP_ACCESS_TOKEN", "fake-access-token")
os.environ.setdefault("VERIFY_TOKEN", "fake-verify-token")
