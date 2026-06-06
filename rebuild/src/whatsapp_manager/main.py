import os

from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

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


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


# Serve a minimal dashboard UI
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/dashboard", include_in_schema=False)
def dashboard():
    file_path = os.path.join(static_dir, "dashboard.html")
    return FileResponse(file_path)
