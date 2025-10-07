import pytest
import sqlite3
from app.infrastructure.repositories.sqlite_user_repository import SQLiteUserRepository
from app.application.services.auth_service import AuthService

bcrypt = pytest.importorskip("bcrypt")  # skip tests if bcrypt not installed


def test_create_and_authenticate_user():
    conn = sqlite3.connect(":memory:")
    repo = SQLiteUserRepository(connection=conn)
    repo.create_tables()

    auth = AuthService(repo)
    user = auth.create_user(
        name="Test User", username="testuser", password="secret123", role="usuario"
    )
    assert user.id is not None

    found = auth.authenticate("testuser", "secret123")
    assert found is not None
    assert found.username == "testuser"


def test_duplicate_username_raises():
    conn = sqlite3.connect(":memory:")
    repo = SQLiteUserRepository(connection=conn)
    repo.create_tables()

    auth = AuthService(repo)
    auth.create_user(name="User A", username="sameuser", password="p1")
    with pytest.raises(ValueError):
        auth.create_user(name="User B", username="sameuser", password="p2")
