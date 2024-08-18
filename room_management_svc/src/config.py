from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        validate_default=False, env_file=[".env", "prod.env"], env_file_encoding="utf-8"
    )

    db_name: str = "db_name"
    db_user: str = "db_user"
    db_password: str = "db_password"
    db_host: str = "db_host"
    db_port: int = 5432

    worker_count: int = 10
    grpc_port: int = 50051
    grpc_host: str = "localhost"

    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_key_ttl: int = 600

    min_distance: int = 5


# Create a singleton instance of the settings to be used throughout the application
settings = Settings()
