from PyQt6.QtCore import QObject, pyqtSignal
from typing import List
from domain.entities.user import User

class UserViewModel(QObject):
    """
    ViewModel para la gestión de usuarios en la vista de estadísticas.
    Actúa como intermediario entre la vista (UserStatsView) y los servicios de dominio.
    """
    users_loaded = pyqtSignal(list)  # Emite lista de User
    user_deleted = pyqtSignal(int)   # Emite ID del usuario eliminado
    error_occurred = pyqtSignal(str) # Emite mensaje de error

    def __init__(self, user_service) -> None:
        """
        Inicializa el ViewModel con el servicio de usuarios.

        Args:
            user_service: Implementación de la interfaz de gestión de usuarios.
        """
        super().__init__()
        self.user_service = user_service

    def load_all_users(self) -> None:
        """
        Carga todos los usuarios activos y emite la señal con la lista.
        """
        try:
            users: List[User] = self.user_service.get_all_users()
            self.users_loaded.emit(users)
        except Exception as e:
            self.error_occurred.emit(f"Error al cargar usuarios: {str(e)}")

    def delete_user(self, user_id: int) -> None:
        """
        Elimina un usuario por su ID y emite señal de éxito o error.

        Args:
            user_id (int): ID del usuario a eliminar.
        """
        if user_id <= 0:
            self.error_occurred.emit("ID de usuario inválido.")
            return

        try:
            self.user_service.delete_user(user_id)
            self.user_deleted.emit(user_id)
        except Exception as e:
            self.error_occurred.emit(f"Error al eliminar usuario: {str(e)}")

    def get_deleted_user_count(self) -> int:
        """
        Obtiene el número total de usuarios eliminados (lógicamente o físicamente).

        Returns:
            int: Cantidad de usuarios eliminados.
        """
        try:
            return self.user_service.get_deleted_user_count()
        except Exception:
            return 0