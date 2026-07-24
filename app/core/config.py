from typing import Annotated, Literal

from pydantic import BeforeValidator, EmailStr, Field, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


def _parse_cors_allowed_origins(v: str | list[str] | None) -> list[str]:
    """Parsea y limpia orígenes CORS desde una lista o cadena separada por comas."""
    if isinstance(v, list):
        return v
    if v and isinstance(v, str):
        return [origin.strip() for origin in v.split(",")]

    return []


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        case_sensitive=True,
        extra="forbid",
        frozen=True,
    )

    # App
    NAME: str
    DESCRIPTION: str
    VERSION: str = Field(pattern=r"^\d+\.\d+\.\d+$")

    # Security
    SECRET_KEY: str = Field(min_length=32)
    CORS_ALLOWED_ORIGINS: Annotated[
        list[str] | str,
        BeforeValidator(_parse_cors_allowed_origins),
    ] = []
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # PostgreSQL
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    # Email SMTP
    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USER: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: EmailStr

    # Frontend
    FRONTEND_URL: str

    # Entorno (Dependiendo de la configuración del contenedor)
    ENVIRONMENT: Literal["local", "production"]

    @property
    def is_debug(self) -> bool:
        """
        Determina si la aplicación está en modo debug basándose en el entorno.
        Se realiza de manera automática.
        """
        return self.ENVIRONMENT == "local"

    def get_postgres_dsn(self, host: str) -> PostgresDsn:
        """
        Construye el DSN de Postgres permitiendo la sobreescritura del host.
        Útil en entornos como pruebas donde el host suele cambiar.
        """
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=host,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    @computed_field
    @property
    def postgres_dsn(self) -> PostgresDsn:
        """DSN predeterminado de la aplicación."""
        return self.get_postgres_dsn(host=self.POSTGRES_HOST)


settings = AppSettings()  # type: ignore
