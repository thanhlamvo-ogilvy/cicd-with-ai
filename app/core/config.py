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

    # CORS — stored as comma-separated string for dotenv compatibility
    cors_origins: str = "http://localhost:3000,http://localhost:5173,http://localhost:8080"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    # AI Providers
    openai_api_key: str = ""
    openai_base_url: str = ""
    anthropic_api_key: str = ""
    google_api_key: str = ""

    # AI Defaults
    default_provider: str = "openai"
    default_model: str = "gpt-4o"

    @property
    def is_production(self) -> bool:
        return self.api_env == "production"

    @property
    def available_providers(self) -> list[str]:
        providers = []
        if self.openai_api_key or self.openai_base_url:
            providers.append("openai")
        if self.anthropic_api_key:
            providers.append("anthropic")
        if self.google_api_key:
            providers.append("google")
        return providers


settings = Settings()
