from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    #1 Identidad de la api
    PROJECT_NAME: str = "Inventario & Auditoria RBAC API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    #2 conexion a BAe de Datos (SQlite local por defecto, PostgreSQL en produccion)
    DATABASE_URL: str = "sqlite+aiosqlite:///./inventory.db"

    #3 Configuracion Criptografica JWT
    SECRET_KEY: str = "dev-secret-key-change-in-production-9f8e7d6c5b4a3f2e1d"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*24 #24Horas

    #4 Regala de lectura de archivo .env
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive= True,
        extra="ignore"
    )

settings = Settings()