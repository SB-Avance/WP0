from fastapi import APIRouter, HTTPException

from ..services import dataverse as dataverse_svc

router = APIRouter(prefix="/api/admin")


@router.get("/check_dataverse_token")
def check_dataverse_token():
    """Attempt to acquire a Dataverse token and return basic info.

    Returns a small JSON with success or error. In `LOCAL` environment the
    mock client is used and the endpoint reports mock status.
    """
    client = dataverse_svc.get_dataverse_client()

    # Mock clients may not implement token acquisition
    acquire = getattr(client, "_acquire_token", None)
    if acquire is None:
        return {"success": True, "message": "LOCAL mock client - no token acquired"}

    try:
        token = acquire()
        if token:
            return {"success": True, "token_preview": token[:8] + "..."}
        return {"success": False, "error": "no_token_returned"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
