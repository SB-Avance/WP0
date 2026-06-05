import sys
sys.path.insert(0,'c:/VS/BIN/rebuild/src')
from whatsapp_manager.core.config import settings
from msal import ConfidentialClientApplication

print('Using settings:')
print('TENANT_ID=', settings.tenant_id)
print('CLIENT_ID=', settings.client_id)
print('DATAVERSE_URL=', settings.dataverse_url)

authority = f"https://login.microsoftonline.com/{settings.tenant_id}"
app = ConfidentialClientApplication(settings.client_id, authority=authority, client_credential=settings.client_secret)
res = app.acquire_token_for_client(scopes=[f"{settings.dataverse_url}/.default"])
print('Response:', res)
