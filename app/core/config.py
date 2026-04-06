from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    api_env: str = "development"
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 30

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/appdb"

    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:8080"]

    @property
    def is_production(self) -> bool:
        return self.api_env == "production"


settings = Settings()
