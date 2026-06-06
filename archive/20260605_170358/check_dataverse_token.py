import sys

sys.path.insert(0, "rebuild/src")
from whatsapp_manager.services import dataverse as dv

try:
    client = dv.get_dataverse_client()
    token = client._acquire_token()
    print("TOKEN OK" if token else "NO TOKEN")
except Exception as e:
    print("ERROR:", repr(e))
