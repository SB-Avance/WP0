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


settings = Settings()  # type: ignore[call-arg]
