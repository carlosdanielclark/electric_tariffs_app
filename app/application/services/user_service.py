from typing import List
from domain.entities.user import User
from infrastructure.database.repositories.user_repository import UserRepository
from infrastructure.logger.activity_logger import ActivityLogger


class UserService:
    """
    Servicio de gestión de usuarios.
    Coordina operaciones de negocio relacionadas con usuarios,
    delegando persistencia al repositorio y registrando eventos.
    """

    def __init__(self, user_repository: UserRepository, logger: ActivityLogger) -> None:
        """
        Inicializa el servicio con sus dependencias.

        Args:
            user_repository (UserRepository): Repositorio para operaciones CRUD.
            logger (ActivityLogger): Sistema de registro de actividades.
        """
        self.user_repository = user_repository
        self.logger = logger

    def get_all_users(self) -> List[User]:
        """
        Obtiene todos los usuarios activos.

        Returns:
            List[User]: Lista de usuarios activos.
        """
        users = self.user_repository.get_all_active()
        return users

    def delete_user(self, user_id: int) -> None:
        """
        Elimina un usuario (lógicamente o físicamente, según implementación del repositorio).
        Registra el evento en el sistema de logs.

        Args:
            user_id (int): ID del usuario a eliminar.

        Raises:
            ValueError: Si el ID es inválido o el usuario no existe.
        """
        if user_id <= 0:
            raise ValueError("ID de usuario inválido.")

        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("Usuario no encontrado.")

        self.user_repository.delete(user_id)
        self.logger.log_event(
            user_id=user_id,
            event="eliminacion_usuario",
            details=f"Usuario '{user.username}' eliminado por administrador."
        )

    def get_deleted_user_count(self) -> int:
        """
        Obtiene el número total de usuarios eliminados (lógicamente o físicamente).

        Returns:
            int: Cantidad de usuarios eliminados.
        """
        return self.user_repository.count_deleted()