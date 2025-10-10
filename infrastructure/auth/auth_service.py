from typing import Optional
import bcrypt
from domain.entities.user import User
from infrastructure.database.repositories.user_repository import UserRepository


class AuthService:
    """
    Servicio de autenticación.
    Maneja login, hashing y validación de credenciales.
    """

    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def login(self, username: str, password: str) -> Optional[User]:
        """
        Autentica a un usuario por username y contraseña.

        Args:
            username (str): Nombre de usuario.
            password (str): Contraseña en texto plano.

        Returns:
            Optional[User]: Usuario autenticado o None si falla.
        """
        if not username or not password:
            return None

        user = self.user_repository.get_by_username(username)
        if user is None or not user.activo:
            return None

        # Verificar hash
        if bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            return user
        return None