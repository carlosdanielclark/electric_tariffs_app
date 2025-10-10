from typing import List, Optional
from domain.entities.user import User


class UserRepository:
    """
    Repositorio para operaciones CRUD sobre usuarios.
    Requiere una conexión SQLite activa.
    """

    def __init__(self, conn) -> None:
        """
        Inicializa el repositorio con una conexión a la base de datos.

        Args:
            conn: Conexión SQLite3 activa.
        """
        self.conn = conn

    def get_all_active(self) -> List[User]:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, nombre, username, password_hash, rol, activo, fecha_creacion "
            "FROM usuarios WHERE activo = 1 ORDER BY nombre ASC"
        )
        rows = cursor.fetchall()
        return [
            User(
                id=row[0],
                nombre=row[1],
                username=row[2],
                password_hash=row[3],
                rol=row[4],
                activo=bool(row[5]),
                fecha_creacion=row[6]
            )
            for row in rows
        ]

    def get_by_id(self, user_id: int) -> Optional[User]:
        if user_id <= 0:
            return None
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, nombre, username, password_hash, rol, activo, fecha_creacion "
            "FROM usuarios WHERE id = ?",
            (user_id,)
        )
        row = cursor.fetchone()
        if row:
            return User(
                id=row[0],
                nombre=row[1],
                username=row[2],
                password_hash=row[3],
                rol=row[4],
                activo=bool(row[5]),
                fecha_creacion=row[6]
            )
        return None

    def get_by_username(self, username: str) -> Optional[User]:
        if not username or not isinstance(username, str):
            return None
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, nombre, username, password_hash, rol, activo, fecha_creacion "
            "FROM usuarios WHERE username = ?",
            (username,)
        )
        row = cursor.fetchone()
        if row:
            return User(
                id=row[0],
                nombre=row[1],
                username=row[2],
                password_hash=row[3],
                rol=row[4],
                activo=bool(row[5]),
                fecha_creacion=row[6]
            )
        return None

    def delete(self, user_id: int) -> None:
        if user_id <= 0:
            raise ValueError("ID de usuario inválido.")
        cursor = self.conn.cursor()
        cursor.execute("UPDATE usuarios SET activo = 0 WHERE id = ?", (user_id,))
        cursor.execute("DELETE FROM lecturas WHERE usuario_id = ?", (user_id,))
        self.conn.commit()

    def count_deleted(self) -> int:
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE activo = 0")
        return cursor.fetchone()[0]

    def create(self, user: User) -> int:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO usuarios (nombre, username, password_hash, rol, activo)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user.nombre, user.username, user.password_hash, user.rol, user.activo)
        )
        user_id = cursor.lastrowid
        self.conn.commit()
        return user_id