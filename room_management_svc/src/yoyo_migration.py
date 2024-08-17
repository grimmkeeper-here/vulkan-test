import os
import sys

# Add the path to the parent directory
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

from yoyo import get_backend, read_migrations

from src.config import settings


def apply_migrations():
    backend = get_backend(
        f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
    )
    migrations = read_migrations(
        os.path.join(os.path.dirname(__file__), "../migrations")
    )
    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))


if __name__ == "__main__":
    apply_migrations()
