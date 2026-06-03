from typing import Optional

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from ..core.config import settings
from ..services import dataverse as dataverse_svc
from ..services import whatsapp as whatsapp_svc

router = APIRouter()


class WebhookMessageText(BaseModel):
    body: str


@router.get("/webhook")
def verify(hub_verify_token: Optional[str] = None, hub_challenge: Optional[str] = None):
    # FastAPI will map query params; mirror the previous behavior
    if hub_verify_token == settings.verify_token:
        return hub_challenge
    raise HTTPException(status_code=403, detail="Invalid token")


@router.post("/webhook")
async def webhook_handler(request: Request):
    data = await request.json()
    # Very small compatibility layer: iterate entries/changes/messages
    for entry in data.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            messages = value.get("messages", [])
            contacts = value.get("contacts", [])
            fromname = (contacts[0].get("profile", {}).get("name")) if contacts else ""

            for msg in messages:
                message_id = msg.get("id")
                fromphone = msg.get("from")
                timestamp = int(msg.get("timestamp", 0))
                body = msg.get("text", {}).get("body", "")

                # Persist to Dataverse
                try:
                    dataverse_svc.dataverse_client.save_message(
                        message_id,
                        fromphone,
                        timestamp,
                        462410000,
                        body,
                        fromname,
                    )
                except Exception as e:
                    # Log and continue
                    print(f"[WEBHOOK_DATAVERSE_ERROR] {e}")

                # Send an auto-reply (simple fallback)
                try:
                    if body.lower() in ["menu", "hola"]:
                        reply = "Hola, gracias por escribir. Responderemos pronto."
                    else:
                        reply = "Mensaje recibido. Escribe 'menu' para opciones."

                    whatsapp_svc.whatsapp_client.send_text(fromphone, reply)
                except Exception as e:
                    print(f"[WEBHOOK_WA_ERROR] {e}")

    return {"status": "ok"}
