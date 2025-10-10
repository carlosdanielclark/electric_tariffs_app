"""Manejo de conexión y esquema SQLite."""

from __future__ import annotations
import sqlite3
import os
from pathlib import Path
from src.config import settings
from datetime import datetime

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    rol TEXT NOT NULL CHECK (rol IN ('admin', 'usuario')),
    activo INTEGER NOT NULL DEFAULT 1,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_usuarios_username ON usuarios(username);
CREATE INDEX IF NOT EXISTS idx_usuarios_activo ON usuarios(activo);

CREATE TABLE IF NOT EXISTS lecturas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    lectura_actual REAL NOT NULL CHECK (lectura_actual >= 0),
    lectura_anterior REAL NOT NULL CHECK (lectura_anterior >= 0),
    consumo REAL NOT NULL CHECK (consumo >= 0),
    costo REAL NOT NULL CHECK (costo >= 0),
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_lecturas_usuario_id ON lecturas(usuario_id);
CREATE INDEX IF NOT EXISTS idx_lecturas_fecha ON lecturas(fecha);
"""


def get_connection(db_path: str | None = None) -> sqlite3.Connection:
    """Retorna una conexión SQLite. Crea directorio si hace falta."""
    db_path = db_path or settings.DB_PATH
    db_file = Path(db_path)
    db_file.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_file), check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(db_path: str | None = None) -> None:
    """Inicializa la base de datos creando las tablas necesarias."""
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.executescript(SCHEMA_SQL)
        conn.commit()
    finally:
        conn.close()
