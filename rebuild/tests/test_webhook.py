import importlib
import os
import sys

from fastapi.testclient import TestClient


def test_webhook_calls_dataverse_and_whatsapp(monkeypatch):
    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
    )
    app = importlib.import_module("whatsapp_manager.main").app
    dataverse_svc = importlib.import_module("whatsapp_manager.services.dataverse")
    whatsapp_svc = importlib.import_module("whatsapp_manager.services.whatsapp")
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
