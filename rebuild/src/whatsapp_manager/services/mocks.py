from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional, Tuple


class MockDataverseClient:
    def __init__(self):
        # in-memory store of messages
        # each message: dict with keys used by app
        self._messages: List[dict] = []

    def save_message(
        self,
        message_id: str,
        phone: str,
        timestamp: int,
        message_type: int,
        body: str,
        fromname: str,
        group: Optional[str] = None,
    ) -> dict:
        ts = None
        try:
            ts = datetime.fromtimestamp(int(timestamp), tz=timezone.utc).isoformat()
        except Exception:
            ts = datetime.now(timezone.utc).isoformat()

        record = {
            "cr321_messageid": str(message_id),
            "cr321_phone": phone,
            "cr321_timestamp": ts,
            "cr321_messagetype": message_type,
            "cr321_body": body,
            "cr321_fromname": fromname,
            "cr321_direction": 462410000,
            "cr321_grupoid": {"cr321_nombre": group} if group else None,
        }
        self._messages.append(record)
        print(f"[MOCK_DATAVERSE] Saved message {message_id} from {phone}")
        return record

    def query_messages(self, phone_number: str, group_filter: Optional[str] = None):
        results = [m for m in self._messages if m.get("cr321_phone") == phone_number]
        if group_filter:
            results = [
                m
                for m in results
                if (m.get("cr321_grupoid") or {}).get("cr321_nombre") == group_filter
            ]
        return results

    def query_conversations(
        self, limit: int = 50, group_filter: Optional[str] = None
    ) -> Tuple[List[dict], List[str]]:
        # aggregate by phone
        conversations = {}
        groups = set()
        for m in sorted(
            self._messages, key=lambda r: r.get("cr321_timestamp") or "", reverse=True
        ):
            phone = m.get("cr321_phone")
            group = (m.get("cr321_grupoid") or {}).get("cr321_nombre") or "General"
            groups.add(group)
            if (
                group_filter
                and group_filter.upper() != "TODOS"
                and group != group_filter
            ):
                continue
            if phone and phone not in conversations:
                conversations[phone] = {
                    "phone": phone,
                    "name": m.get("cr321_fromname", "Desconocido"),
                    "last_message": m.get("cr321_body", ""),
                    "timestamp": m.get("cr321_timestamp"),
                    "group": group,
                    "unread": 0,
                }
        return list(conversations.values())[:limit], list(groups)


class MockWhatsAppClient:
    def __init__(self):
        self.sent: List[dict] = []

    def send_text(self, to: str, body: str):
        msg = {
            "to": to,
            "body": body,
            "ts": datetime.now(timezone.utc).isoformat(),
        }
        self.sent.append(msg)
        print(f"[MOCK_WHATSAPP] send_text to={to} body={body}")
        return {"messages": [{"id": "mock-msg-id"}]}
