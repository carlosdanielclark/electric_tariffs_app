import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from infrastructure.database.connection import get_db_connection
from infrastructure.database.repositories.user_repository import UserRepository
from infrastructure.auth.auth_service import AuthService
from application.services.reading_service import ReadingService
from application.services.user_service import UserService
from presentation.views.login_view import LoginView
from presentation.views.main_window import MainWindow


def main() -> None:
    app = QApplication(sys.argv)
    conn = get_db_connection()

    # Inicializar dependencias
    user_repo = UserRepository(conn)
    auth_service = AuthService(user_repo)
    logger = None  # Pendiente: inyectar logger real
    reading_service = ReadingService(conn, logger)
    user_service = UserService(user_repo, logger)

    # Mostrar login
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