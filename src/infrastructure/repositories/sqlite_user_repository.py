from __future__ import annotations
import sqlite3
from typing import Optional
from src.domain.entities.user import User
from src.infrastructure.database.connection import get_connection
from src.config import settings


class SQLiteUserRepository:
    """Repositorio simple de usuarios usando SQLite."""

    def __init__(
        self, db_path: str | None = None, connection: sqlite3.Connection | None = None
    ):
        self._db_path = db_path or settings.DB_PATH
        self._conn = connection

    def _get_conn(self) -> sqlite3.Connection:
        if self._conn is not None:
            return self._conn
        return get_connection(self._db_path)

    def create_tables(self) -> None:
        """Crear tablas (usa el script de connection.init_db si se quiere)."""
        conn = self._get_conn()
        cur = conn.cursor()
        # DDL idempotente: crear tablas si no existen
        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            rol TEXT NOT NULL CHECK (rol IN ('admin', 'usuario')),
            activo INTEGER NOT NULL DEFAULT 1,
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
        );"""
        )
        conn.commit()

    def add_user(
        self, name: str, username: str, password_hash: str, role: str = "usuario"
    ) -> User:
        conn = self._get_conn()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO usuarios (nombre, username, password_hash, rol) VALUES (?, ?, ?, ?)",
                (name, username, password_hash, role),
            )
            conn.commit()
            user_id = cur.lastrowid
            assert user_id is not None, "Usuario insertado pero lastrowid es None (esto no debería ocurrir)"
            return User(
                id=user_id,
                name=name,
                username=username,
                password_hash=password_hash,
                role=role,
                active=True,
            )
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Username ya existe: {username}") from e

    def get_by_username(self, username: str) -> Optional[User]:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, nombre, username, password_hash, rol, activo, fecha_creacion FROM usuarios WHERE username = ?",
            (username,),
        )
        row = cur.fetchone()
        if not row:
            return None
        user_id, nombre, uname, password_hash, rol, activo, fecha_creacion = row
        return User(
            id=user_id,
            name=nombre,
            username=uname,
            password_hash=password_hash,
            role=rol,
            active=bool(activo),
        )
