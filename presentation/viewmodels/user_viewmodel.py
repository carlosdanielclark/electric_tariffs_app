from PyQt6.QtCore import QObject, pyqtSignal as Signal
from typing import List
from domain.entities.user import User


class UserViewModel(QObject):
    users_loaded = Signal(list)
    user_deleted = Signal(int)
    error_occurred = Signal(str)

    def __init__(self, user_service) -> None:
        super().__init__()
        self.user_service = user_service

    def load_all_users(self) -> None:
        try:
            users: List[User] = self.user_service.get_all_users()
            self.users_loaded.emit(users)
        except Exception as e:
            self.error_occurred.emit(f"Error al cargar usuarios: {str(e)}")

    def delete_user(self, user_id: int) -> None:
        if user_id <= 0:
            self.error_occurred.emit("ID de usuario inválido.")
            return
        try:
            self.user_service.delete_user(user_id)
            self.user_deleted.emit(user_id)
        except Exception as e:
            self.error_occurred.emit(f"Error al eliminar usuario: {str(e)}")

    def get_deleted_user_count(self) -> int:
        try:
            return self.user_service.get_deleted_user_count()
        except Exception:
            return 0