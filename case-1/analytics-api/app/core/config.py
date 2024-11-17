from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "evreka-db"
    postgres_host: str = "postgres"
    postgres_port: int = 5432

    class Config:
        env_file = ".env"

settings = Settings()