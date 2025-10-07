from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database settings
    database_url: str = "postgresql+asyncpg://ephemeral_user:ephemeral_pass@localhost:5433/ephemeral_db"
    ephemeral_database_url: str = "postgresql+asyncpg://ephemeral_user:ephemeral_pass@localhost:5433/ephemeral_db"

    # Gemini AI settings
    gemini_api_key: Optional[str] = None

    # JWT settings
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # App settings
    app_name: str = "Tourism Chatbot Backend"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"

    class Config:
        env_file = ".env"


settings = Settings()
