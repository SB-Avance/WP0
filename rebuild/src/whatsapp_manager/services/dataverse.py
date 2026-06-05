from time import time
from typing import Optional

import requests
from msal import ConfidentialClientApplication

from ..core.config import settings


class DataverseClient:
    def __init__(self):
        self._token = None
        self._token_expiry = 0

    def _acquire_token(self) -> Optional[str]:
        if self._token and time() < self._token_expiry - 60:
            return self._token

        authority = f"https://login.microsoftonline.com/{settings.tenant_id}"
        app = ConfidentialClientApplication(
            settings.client_id,
            authority=authority,
            client_credential=settings.client_secret,
        )
        token = app.acquire_token_for_client(
            scopes=[f"{settings.dataverse_url}/.default"]
        )
        if "access_token" in token:
            self._token = token["access_token"]
            self._token_expiry = time() + int(token.get("expires_in", 3600))
            return self._token
        return None

    def save_message(
        self,
        message_id: str,
        phone: str,
        timestamp: int,
        message_type: int,
        body: str,
        fromname: str,
        group: Optional[str] = None,
    ):
        token = self._acquire_token()
        if not token:
            raise RuntimeError("No Dataverse token")

        timestamp_iso = None
        try:
            from datetime import datetime, timezone

            timestamp_iso = (
                datetime.fromtimestamp(int(timestamp), tz=timezone.utc)
                .isoformat()
                .replace("+00:00", "Z")
            )
        except Exception:
            from datetime import datetime, timezone

            timestamp_iso = (
                datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            )

        url = f"{settings.dataverse_url}/api/data/v9.2/cr321_adatawp0s"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        payload = {
            "cr321_messageid": str(message_id),
            "cr321_phone": phone,
            "cr321_timestamp": timestamp_iso,
            "cr321_messagetype": message_type,
            "cr321_body": body,
            "cr321_fromname": fromname,
            "cr321_direction": 462410000,
        }

        if group:
            # binding by GUID would require lookup; implement later
            payload["cr321_grupoid@odata.bind"] = group

        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        resp.raise_for_status()
        return resp.json() if resp.content else {}

    def query_messages(self, phone_number: str, group_filter: Optional[str] = None):
        token = self._acquire_token()
        if not token:
            raise RuntimeError("No Dataverse token")

        # Build OData query
        base = f"{settings.dataverse_url}/api/data/v9.2/cr321_adatawp0s"
        query = f"?$filter=cr321_phone eq '{phone_number}'&$orderby=cr321_timestamp asc"
        url = base + query
        if group_filter and group_filter.upper() not in ["TODOS", "NONE", "NULL"]:
            # group_filter expected to be GUID or name; simple contains fallback
            query = (
                "?$filter=cr321_phone eq '"
                + phone_number
                + "' and cr321_grupoid eq '"
                + group_filter
                + "'&$orderby=cr321_timestamp asc"
            )
            url = base + query

        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json().get("value", [])

    def query_conversations(self, limit: int = 50, group_filter: Optional[str] = None):
        token = self._acquire_token()
        if not token:
            raise RuntimeError("No Dataverse token")

        base = f"{settings.dataverse_url}/api/data/v9.2/cr321_adatawp0s"
        query = (
            f"?$top={limit}&$orderby=cr321_timestamp desc"
            + "&$expand=cr321_grupoid($select=cr321_nombre)"
        )
        url = base + query
        if group_filter and group_filter.upper() != "TODOS":
            # Attempt to filter by expanded group name
            # fallback to client-side filtering later
            url += "&$filter=_cr321_grupoid_value eq " + group_filter

        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        records = data.get("value", [])

        # Aggregate conversations by phone
        conversations = {}
        groups = set()
        for record in records:
            phone = record.get("cr321_phone")
            grupo_obj = record.get("cr321_grupoid")
            group = grupo_obj.get("cr321_nombre") if grupo_obj else "General"
            groups.add(group)

            if phone:
                if phone not in conversations:
                    conversations[phone] = {
                        "phone": phone,
                        "name": record.get("cr321_fromname", "Desconocido"),
                        "last_message": record.get("cr321_body", ""),
                        "timestamp": record.get("cr321_timestamp"),
                        "group": group,
                        "unread": 0,
                    }

        return list(conversations.values()), list(groups)


# Backwards-compatible module-level client for tests that patch `dataverse_client`
dataverse_client: DataverseClient = DataverseClient()


def get_dataverse_client() -> DataverseClient:
    # Prefer module-level `dataverse_client` (test compatibility); otherwise create one lazily
    global dataverse_client
    if dataverse_client is None:
        dataverse_client = DataverseClient()
    return dataverse_client
