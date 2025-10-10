import sqlite3
from src.infrastructure.repositories.sqlite_user_repository import SQLiteUserRepository


def test_create_tables_in_memory() -> None:  # ← Añadido "-> None"
    conn = sqlite3.connect(":memory:")
    repo = SQLiteUserRepository(connection=conn)
    # Should not raise
    repo.create_tables()
