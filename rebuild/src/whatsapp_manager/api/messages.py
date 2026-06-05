from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from ..services import dataverse as dataverse_svc

router = APIRouter(prefix="/api")


@router.get("/messages/{phone_number}")
def get_messages(phone_number: str, group: Optional[str] = Query(None)):
    try:
        # Use get_dataverse_client() so we respect mocks or configured client
        records = dataverse_svc.get_dataverse_client().query_messages(phone_number, group)
        messages = []
        for record in records:
            messages.append(
                {
                    "id": record.get("cr321_messageid"),
                    "body": record.get("cr321_body"),
                    "timestamp": record.get("cr321_timestamp"),
                    "direction": (
                        "incoming"
                        if record.get("cr321_direction") == 462410000
                        else "outgoing"
                    ),
                    "type": record.get("cr321_messagetype"),
                }
            )
        return {"success": True, "messages": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
