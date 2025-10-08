from __future__ import annotations
import sys
from app.infrastructure.database.connection import init_db


def main_cli() -> None:
    import argparse
    from app.infrastructure.repositories.sqlite_user_repository import SQLiteUserRepository
    from app.application.services.auth_service import AuthService

    parser = argparse.ArgumentParser(
        prog="electric_app",
        description="Gestor de lecturas eléctricas - Fase 1/2/3"
    )
    parser.add_argument(
        "command",
        choices=["init-db", "create-admin", "gui"],
        nargs="?",
        default="gui"
    )
    parser.add_argument("--username", "-u")
    parser.add_argument("--password", "-p")
    args = parser.parse_args()

    if args.command == "init-db":
        init_db()
        print("DB inicializada.")
    elif args.command == "create-admin":
        repo = SQLiteUserRepository()
        auth = AuthService(repo)
        username = args.username or input("Admin username: ")
        password = args.password or input("Admin password: ")
        auth.create_user(name="Administrador", username=username, password=password, role="admin")
        print("Admin creado.")
    elif args.command == "gui":
        main_gui()


def main_gui() -> None:
    try:
        from PyQt6.QtWidgets import QApplication
        from app.ui.main_window import MainWindow
    except Exception as e:
        print("No se pudo iniciar la GUI. Asegúrate de tener PyQt6 y matplotlib instalados.", e)
        sys.exit(1)

    app = QApplication(sys.argv)
    try:
        from pathlib import Path
        style_path = Path(__file__).resolve().parent / "ui" / "resources" / "style.qss"
        if style_path.exists():
            with open(style_path, "r", encoding="utf-8") as f:
                app.setStyleSheet(f.read())
    except Exception:
        pass

    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main_cli()