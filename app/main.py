"""Punto de entrada mínimo para la aplicación - Fase 1."""

from __future__ import annotations
import argparse
from app.infrastructure.database.connection import init_db
from app.infrastructure.repositories.sqlite_user_repository import SQLiteUserRepository
from app.application.services.auth_service import AuthService
from app.infrastructure.logger.activity_logger import ActivityLogger


def main():
    parser = argparse.ArgumentParser(
        prog="electric_app", description="Gestor de lecturas eléctricas - Fase 1"
    )
    parser.add_argument(
        "command",
        choices=["init-db", "create-admin", "help"],
        nargs="?",
        default="help",
    )
    parser.add_argument("--username", "-u", help="Username del admin a crear")
    parser.add_argument(
        "--password", "-p", help="Password del admin a crear (inseguro en CLI)"
    )
    args = parser.parse_args()

    if args.command == "init-db":
        init_db()
        print("Base de datos inicializada.")
    elif args.command == "create-admin":
        repo = SQLiteUserRepository()
        auth = AuthService(repo)
        username = args.username or input("Admin username: ")
        password = args.password or input("Admin password: ")
        try:
            user = auth.create_user(
                name="Administrador", username=username, password=password, role="admin"
            )
            ActivityLogger().log_event(
                user.id, "create_admin", f"Admin {username} creado"
            )
            print(f"Admin creado: id={user.id} username={user.username}")
        except Exception as e:
            print(f"Error creando admin: {e}")
    else:
        print("Uso:")
        print("  python -m app.main init-db         -> inicializar la base de datos")
        print(
            "  python -m app.main create-admin    -> crear usuario admin (pide username/password)"
        )


if __name__ == "__main__":
    main()
