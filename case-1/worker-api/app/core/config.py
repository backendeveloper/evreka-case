from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    rabbitmq_host: str = "rabbitmq"
    rabbitmq_port: int = 5672
    rabbitmq_user: str = "evreka"
    rabbitmq_password: str = "evreka"
    rabbitmq_queue: str = "task_queue"

    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "evreka-db"
    postgres_host: str = "postgres"
    postgres_port: int = 5432

    class Config:
        env_file = ".env"

settings = Settings()