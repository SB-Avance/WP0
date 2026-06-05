from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from ..services import dataverse as dataverse_svc

router = APIRouter(prefix="/api")


@router.get("/conversations")
def get_conversations(limit: int = 50, group: Optional[str] = Query(None)):
    try:
        convs, groups = dataverse_svc.get_dataverse_client().query_conversations(
            limit=limit, group_filter=group
        )
        return {
            "success": True,
            "conversations": convs,
            "groups": groups,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/send_message")
def send_message(payload: dict):
    phone = payload.get("phone")
    message = payload.get("message")
    group = payload.get("group", "GENERAL")

    if not phone or not message:
        raise HTTPException(status_code=400, detail="Missing phone or message")

    try:
        # Send via WhatsApp client
        from ..services import whatsapp as whatsapp_svc

        wa_client = whatsapp_svc.get_whatsapp_client()
        resp = wa_client.send_text(phone.replace("+", ""), message)

        # Save to Dataverse (simple save)
        dv = dataverse_svc.get_dataverse_client()
        dv.save_message(
            resp.get("messages", [{}])[0].get("id", ""),
            phone,
            0,
            462410001,
            message,
            "",
            group,
        )

        return {"success": True, "message_id": resp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
