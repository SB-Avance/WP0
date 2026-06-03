from fastapi import FastAPI

from .api import conversations, messages, webhook
from .core.config import settings

app = FastAPI(title="WhatsApp Manager (rebuild)")

# Routers
app.include_router(webhook.router, prefix="/api")
app.include_router(conversations.router)
app.include_router(messages.router)


@app.get("/health")
def health():
    return {"status": "healthy", "environment": settings.environment}
