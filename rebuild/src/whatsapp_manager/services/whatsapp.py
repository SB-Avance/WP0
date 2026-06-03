import requests

from ..core.config import settings


class WhatsAppClient:
    def __init__(self):
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


whatsapp_client = WhatsAppClient()
