import sys
from PyQt6.QtWidgets import QApplication
from ui.views.login_view import LoginView
from ui.views.main_window import MainWindow
from infrastructure.database.connection import get_db_connection
from application.services.auth_service import AuthService
from application.services.reading_service import ReadingService
from application.services.user_service import UserService

def main() -> None:
    app = QApplication(sys.argv)
    db = get_db_connection()

    auth_service = AuthService(db)
    reading_service = ReadingService(db)
    user_service = UserService(db)

    login = LoginView()
    if login.exec_() == LoginView.Accepted:
        username = login.username_input.text()
        password = login.password_input.text()
        user = auth_service.login(username, password)
        if user:
            main_window = MainWindow(user, reading_service, user_service)
            main_window.show()
            sys.exit(app.exec_())
        else:
            # Mostrar error en login real
            pass

if __name__ == "__main__":
    main()