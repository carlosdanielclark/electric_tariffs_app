import sys
from PyQt6.QtWidgets import QApplication
from presentation.views.login_view import LoginView
from presentation.views.main_window import MainWindow
from infrastructure.database.connection import get_db_connection
from application.services.auth_service import AuthService
from application.services.reading_service import ReadingService
from application.services.user_service import UserService
from infrastructure.logger.activity_logger import ActivityLogger


def main() -> None:
    app = QApplication(sys.argv)
    db = get_db_connection()
    logger = ActivityLogger()

    auth_service = AuthService(db)
    reading_service = ReadingService(db, logger)

    # Inyectar repositorio en UserService
    from infrastructure.database.repositories.user_repository import UserRepository
    user_repo = UserRepository()
    user_service = UserService(user_repository=user_repo, logger=logger)

    login = LoginView()
    if login.exec() == login.DialogCode.Accepted:
        username = login.username_input.text()
        password = login.password_input.text()
        user = auth_service.login(username, password)
        if user:
            main_window = MainWindow(user, reading_service, user_service)
            main_window.show()
            sys.exit(app.exec())
        else:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(login, "Error", "Credenciales inválidas")
            main()


if __name__ == "__main__":
    main()