from __future__ import annotations
from typing import Optional
from infrastructure.repositories.sqlite_user_repository import SQLiteUserRepository
from domain.entities.user import User


def _hash_password(password: str) -> str:
    """Hash de password con bcrypt. Import lazy para no romper imports cuando bcrypt no esté instalado."""
    try:
        import bcrypt
    except ImportError as e:
        raise RuntimeError(
            "bcrypt no está instalado. Instala dependencias con `pip install -r requirements.txt`"
        ) from e
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def _verify_password(password: str, hashed: str) -> bool:
    try:
        import bcrypt
    except ImportError as e:
        raise RuntimeError(
            "bcrypt no está instalado. Instala dependencias con `pip install -r requirements.txt`"
        ) from e
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


class AuthService:
    def __init__(self, user_repo: SQLiteUserRepository):
        self.user_repo = user_repo

    def create_user(
        self, name: str, username: str, password: str, role: str = "usuario"
    ) -> User:
        """Crear usuario con password hasheada."""
        password_hash = _hash_password(password)
        return self.user_repo.add_user(
            name=name, username=username, password_hash=password_hash, role=role
        )

    def authenticate(
        self, username: str, password: str
    ) -> Optional[User]:  # ← Corregido typo: "authenticat e"
        user = self.user_repo.get_by_username(username)
        if not user:
            return None
        if _verify_password(password, user.password_hash):
            return user
        return None
