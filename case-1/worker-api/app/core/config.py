from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    rabbitmq_host: str
    rabbitmq_port: int
    rabbitmq_user: str
    rabbitmq_password: str
    rabbitmq_queue: str

    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: int

    class Config:
        env_file = ".env"


settings = Settings()
