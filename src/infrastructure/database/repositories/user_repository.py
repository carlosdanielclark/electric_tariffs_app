from typing import List, Optional
from domain.entities.user import User
from infrastructure.database.connection import get_db_connection


class UserRepository:
    """
    Repositorio para operaciones CRUD sobre la entidad Usuario.
    Implementa persistencia en SQLite con soporte para eliminación lógica.
    """

    def __init__(self) -> None:
        """Inicializa el repositorio. La conexión se obtiene bajo demanda."""
        pass

    def get_all_active(self) -> List[User]:
        """
        Obtiene todos los usuarios activos.

        Returns:
            List[User]: Lista de usuarios con `activo = 1`.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, nombre, username, password_hash, rol, activo, fecha_creacion "
            "FROM usuarios WHERE activo = 1 ORDER BY nombre ASC"
        )
        rows = cursor.fetchall()
        conn.close()
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
        """
        Obtiene un usuario por su ID (incluyendo inactivos).

        Args:
            user_id (int): ID del usuario.

        Returns:
            Optional[User]: Usuario si existe, None en caso contrario.
        """
        if user_id <= 0:
            return None
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, nombre, username, password_hash, rol, activo, fecha_creacion "
            "FROM usuarios WHERE id = ?",
            (user_id,)
        )
        row = cursor.fetchone()
        conn.close()
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
        """
        Obtiene un usuario por su nombre de usuario (case-sensitive).

        Args:
            username (str): Nombre de usuario único.

        Returns:
            Optional[User]: Usuario si existe, None en caso contrario.
        """
        if not username or not isinstance(username, str):
            return None
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, nombre, username, password_hash, rol, activo, fecha_creacion "
            "FROM usuarios WHERE username = ?",
            (username,)
        )
        row = cursor.fetchone()
        conn.close()
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
        """
        Elimina lógicamente un usuario (marca como inactivo).
        También elimina en cascada sus lecturas si la BD no lo hace automáticamente.

        Args:
            user_id (int): ID del usuario a eliminar.
        """
        if user_id <= 0:
            raise ValueError("ID de usuario inválido.")

        conn = get_db_connection()
        cursor = conn.cursor()
        # Marcar usuario como inactivo
        cursor.execute("UPDATE usuarios SET activo = 0 WHERE id = ?", (user_id,))
        # Eliminar lecturas asociadas (si no hay ON DELETE CASCADE)
        cursor.execute("DELETE FROM lecturas WHERE usuario_id = ?", (user_id,))
        conn.commit()
        conn.close()

    def count_deleted(self) -> int:
        """
        Cuenta el número total de usuarios eliminados (lógicamente).

        Returns:
            int: Cantidad de usuarios con `activo = 0`.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE activo = 0")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def create(self, user: User) -> int:
        """
        Crea un nuevo usuario en la base de datos.

        Args:
            user (User): Entidad de usuario a persistir.

        Returns:
            int: ID asignado al nuevo usuario.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO usuarios (nombre, username, password_hash, rol, activo)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user.nombre, user.username, user.password_hash, user.rol, user.activo)
        )
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return user_id