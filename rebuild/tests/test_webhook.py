from fastapi.testclient import TestClient

from whatsapp_manager.main import app
from whatsapp_manager.services import dataverse as dataverse_svc
from whatsapp_manager.services import whatsapp as whatsapp_svc


def test_webhook_calls_dataverse_and_whatsapp(monkeypatch):
    called = {"dataverse": 0, "whatsapp": 0}

    def fake_save_message(*args, **kwargs):
        called["dataverse"] += 1
        return {}

    def fake_send_text(to, body):
        called["whatsapp"] += 1
        return {"messages": [{"id": "msg123"}]}

    monkeypatch.setattr(
        dataverse_svc.dataverse_client, "save_message", fake_save_message
    )
    monkeypatch.setattr(whatsapp_svc.whatsapp_client, "send_text", fake_send_text)

    client = TestClient(app)

    payload = {
        "entry": [
            {
                "changes": [
                    {
                        "value": {
                            "messages": [
                                {
                                    "id": "1",
                                    "from": "12345",
                                    "timestamp": "1672531200",
                                    "type": "text",
                                    "text": {"body": "hola"},
                                }
                            ],
                            "contacts": [{"profile": {"name": "Test User"}}],
                        }
                    }
                ]
            }
        ]
    }

    resp = client.post("/api/webhook", json=payload)
    assert resp.status_code == 200
    assert called["dataverse"] == 1
    assert called["whatsapp"] == 1
