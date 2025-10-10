import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from presentation.views.login_view import LoginView
from presentation.views.main_window import MainWindow
from infrastructure.database.connection import get_db_connection
from application.services.auth_service import AuthService
from application.services.reading_service import ReadingService
from application.services.user_service import UserService
from infrastructure.logging.activity_logger import ActivityLogger
from infrastructure.database.repositories.user_repository import UserRepository


def main() -> None:
    app = QApplication(sys.argv)
    db = get_db_connection()
    logger = ActivityLogger()

    auth_service = AuthService(db)
    reading_service = ReadingService(db, logger)

    user_repo = UserRepository()
    user_service = UserService(user_repository=user_repo, logger=logger)

    login = LoginView()
    if login.exec() == login.DialogCode.Accepted:
        username = login.username_input.text().strip()
        password = login.password_input.text()
        if not username or not password:
            QMessageBox.warning(login, "Error", "Usuario y contraseña son obligatorios.")
            sys.exit(1)

        user = auth_service.login(username, password)
        if user is None:
            QMessageBox.warning(login, "Error", "Credenciales inválidas.")
            sys.exit(1)

        # Validar rol explícitamente
        if user.role not in ("admin", "usuario"):
            QMessageBox.critical(login, "Error", "Rol de usuario no válido.")
            sys.exit(1)

        main_window = MainWindow(user, reading_service, user_service)
        main_window.show()
        sys.exit(app.exec())

    else:
        sys.exit(0)


if __name__ == "__main__":
    main()