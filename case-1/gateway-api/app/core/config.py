from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    rabbitmq_host: str = "rabbitmq"
    rabbitmq_port: int = 5672
    rabbitmq_user: str = "evreka"
    rabbitmq_password: str = "evreka"
    rabbitmq_queue: str = "task_queue"

    class Config:
        env_file = ".env"

settings = Settings()