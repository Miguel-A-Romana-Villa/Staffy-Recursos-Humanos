from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Staffy API"
    app_env: str = "development"
    database_url: str = "sqlite:///./app/data/db.sqlite3"
    frontend_url: str = "http://localhost:5173"
    auth_secret: str = "staffy-local-secret"
    auth_token_hours: int = 8

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
