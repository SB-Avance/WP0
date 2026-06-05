import requests

from ..core.config import settings
from . import mocks


class WhatsAppClient:
    def __init__(self):
        # Defer reading settings until instance creation
        self.phone_id = settings.phone_number_id
        self.token = settings.access_token

    def send_text(self, to: str, body: str):
        url = f"https://graph.facebook.com/v17.0/{self.phone_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": body},
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        resp.raise_for_status()
        return resp.json()


_whatsapp_client: WhatsAppClient | None = None


def get_whatsapp_client() -> WhatsAppClient:
    global _whatsapp_client, whatsapp_client
    # If running locally, prefer a mock implementation
    if settings.environment and str(settings.environment).upper() == "LOCAL":
        if not isinstance(whatsapp_client, mocks.MockWhatsAppClient):
            whatsapp_client = mocks.MockWhatsAppClient()  # type: ignore[assignment]
        return whatsapp_client  # type: ignore[return-value]

    # If we were previously using a mock but now running non-LOCAL, reset to allow real client
    if isinstance(whatsapp_client, mocks.MockWhatsAppClient):
        whatsapp_client = None

    # If a module-level client (or placeholder) exists, prefer it for compatibility/tests
    if whatsapp_client is not None:
        return whatsapp_client  # type: ignore[return-value]

    if _whatsapp_client is None:
        _whatsapp_client = WhatsAppClient()
    return _whatsapp_client


# Backwards-compatible module-level placeholder client so tests can monkeypatch
class _WhatsAppPlaceholder:
    def send_text(self, to: str, body: str):
        raise RuntimeError("WhatsApp client not configured")


whatsapp_client: WhatsAppClient | _WhatsAppPlaceholder = _WhatsAppPlaceholder()
