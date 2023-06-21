from datetime import timedelta
from typing import Optional, List, Union, Dict, Any

from pydantic import PostgresDsn, AnyHttpUrl, BaseSettings, validator


class Settings(BaseSettings):
    # Axis cards
    PROJECT_NAME: str = "FastAPI Product"
    DEBUG: bool = True
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # Database
    DATABASE_HOST: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_DB: str
    DATABASE_PORT: int
    DATABASE_URI: Optional[PostgresDsn] = None

    # AuthJWT
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access", "refresh"}
    access_expires = timedelta(minutes=15)
    refresh_expires = timedelta(days=30)
    AUTHJWT_SECRET_KEY: str

    # Redis
    REDIS_SERVER: str
    REDIS_PORT: int

    # Static path
    STATIC_PATH: str
    MEDIA_PATH: str

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("DATABASE_USER"),
            password=values.get("DATABASE_PASSWORD"),
            host=values.get("DATABASE_HOST"),
            path=f"/{values.get('DATABASE_DB') or ''}",
            port=str(values.get("DATABASE_PORT"))
        )

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
