"""
Script para crear un usuario administrador inicial.
Ejecutar solo una vez al desplegar la app.
"""

import sys
import getpass
import bcrypt
from infrastructure.database.connection import get_db_connection, init_db
from infrastructure.database.repositories.user_repository import UserRepository


def create_admin_user() -> None:
    """Crea un usuario administrador si no existe ninguno."""
    # Inicializar base de datos
    init_db()
    conn = get_db_connection()
    repo = UserRepository(conn)

    # Verificar si ya existe un admin
    admins = [u for u in repo.get_all_active() if u.rol == "admin"]
    if admins:
        print("✅ Ya existe al menos un usuario administrador. Nada que hacer.")
        return

    print("🔐 Creando usuario administrador inicial...")
    username = input("Nombre de usuario para el admin: ").strip()
    if not username:
        print("❌ El nombre de usuario no puede estar vacío.")
        sys.exit(1)

    # Verificar que no exista
    if repo.get_by_username(username):
        print("❌ Ya existe un usuario con ese nombre.")
        sys.exit(1)

    password1 = getpass.getpass("Contraseña (no se verá al escribir): ")
    password2 = getpass.getpass("Repetir contraseña: ")

    if password1 != password2:
        print("❌ Las contraseñas no coinciden.")
        sys.exit(1)

    if len(password1) < 6:
        print("❌ La contraseña debe tener al menos 6 caracteres.")
        sys.exit(1)

    # Hashear contraseña
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password1.encode("utf-8"), salt).decode("utf-8")

    from domain.entities.user import User
    from datetime import datetime

    admin = User(
        id=0,
        nombre="Administrador",
        username=username,
        password_hash=password_hash,
        rol="admin",
        activo=True,
        fecha_creacion=datetime.now(),
    )

    user_id = repo.create(admin)
    print(f"✅ Usuario administrador creado con ID {user_id} y username '{username}'.")


if __name__ == "__main__":
    create_admin_user()