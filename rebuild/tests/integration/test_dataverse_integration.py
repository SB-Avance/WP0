import importlib
import os
import sys

import pytest

REAL = os.getenv("REAL_DATAVERSE_INTEGRATION", "false").lower() == "true"


@pytest.mark.skipif(not REAL, reason="REAL_DATAVERSE_INTEGRATION not enabled")
def test_acquire_dataverse_token_real():
    """Run only with REAL_DATAVERSE_INTEGRATION=true; acquire a real token."""
    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
    )
    dataverse_mod = importlib.import_module("whatsapp_manager.services.dataverse")
    get_dataverse_client = getattr(dataverse_mod, "get_dataverse_client")
    client = get_dataverse_client()
    assert hasattr(
        client, "_acquire_token"
    ), "Dataverse client missing token acquisition method"
    token = client._acquire_token()
    assert token, "Expected a token from Dataverse client"
