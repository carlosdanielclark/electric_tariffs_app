from __future__ import annotations
import sqlite3
from datetime import datetime
from decimal import Decimal
from typing import List
from src.domain.entities.reading import Reading
from src.infrastructure.database.connection import get_connection
from src.config import settings


class SQLiteReadingRepository:
    def __init__(self, db_path: str | None = None, connection: sqlite3.Connection | None = None):
        self._db_path = db_path or settings.DB_PATH
        self._conn = connection

    def _get_conn(self) -> sqlite3.Connection:
        if self._conn is not None:
            return self._conn
        return get_connection(self._db_path)

    def create_tables(self) -> None:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("""
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
        """)
        conn.commit()

    def add_reading(
        self,
        user_id: int,
        lectura_actual: Decimal,
        lectura_anterior: Decimal,
        consumo: Decimal,
        costo: Decimal,
    ) -> Reading:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO lecturas (usuario_id, lectura_actual, lectura_anterior, consumo, costo) VALUES (?, ?, ?, ?, ?)",
            (
                user_id,
                float(lectura_actual),
                float(lectura_anterior),
                float(consumo),
                float(costo),
            ),
        )
        conn.commit()
        rowid = cur.lastrowid
        cur.execute("SELECT fecha FROM lecturas WHERE id = ?", (rowid,))
        fecha_row = cur.fetchone()
        # SQLite almacena fecha como ISO string; convertimos a datetime
        fecha = datetime.fromisoformat(fecha_row[0]) if fecha_row and fecha_row[0] else None
        return Reading(
            id=rowid,
            user_id=user_id,
            lectura_actual=lectura_actual,
            lectura_anterior=lectura_anterior,
            consumo=consumo,
            costo=costo,
            fecha=fecha,
        )

    def get_by_user(self, user_id: int) -> List[Reading]:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, usuario_id, lectura_actual, lectura_anterior, consumo, costo, fecha FROM lecturas WHERE usuario_id = ? ORDER BY fecha DESC",
            (user_id,),
        )
        rows = cur.fetchall()
        results: List[Reading] = []
        for r in rows:
            id_, usuario_id, la, lan, cons, cost, fecha_str = r
            fecha = datetime.fromisoformat(fecha_str) if fecha_str else None
            results.append(
                Reading(
                    id=id_,
                    user_id=usuario_id,
                    lectura_actual=Decimal(str(la)),
                    lectura_anterior=Decimal(str(lan)),
                    consumo=Decimal(str(cons)),
                    costo=Decimal(str(cost)),
                    fecha=fecha,
                )
            )
        return results