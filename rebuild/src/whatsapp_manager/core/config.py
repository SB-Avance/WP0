from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    environment: str = Field("local")
    dataverse_url: str = Field(...)
    tenant_id: str = Field(...)
    client_id: str = Field(...)
    client_secret: str = Field(...)
    phone_number_id: str = Field(...)
    access_token: str = Field(...)
    verify_token: str = Field(...)

    # Use model_config for pydantic v2: ignore extra env inputs and load .env
    model_config = {"env_file": ".env", "extra": "ignore"}


class _LazySettings:
    """Lazily instantiate Settings on first attribute access to avoid import-time side effects."""

    _instance: Settings | None = None

    def _load(self) -> Settings:
        if self._instance is None:
            self._instance = Settings()  # type: ignore[call-arg]
        return self._instance

    def __getattr__(self, item: str):
        return getattr(self._load(), item)


settings = _LazySettings()
