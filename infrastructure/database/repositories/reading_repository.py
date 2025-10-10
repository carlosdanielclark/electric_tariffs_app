from typing import List, Optional
from decimal import Decimal
from datetime import datetime
from domain.entities.reading import Reading


class ReadingRepository:
    """
    Repositorio para gestionar operaciones CRUD sobre lecturas eléctricas.
    Implementa el patrón Repository con SQLite como backend.
    """

    def __init__(self, conn) -> None:
        """
        Inicializa el repositorio con una conexión activa a la base de datos.

        Args:
            conn: Conexión SQLite3 activa.
        """
        self.conn = conn

    def save(self, reading: Reading) -> Reading:
        """
        Guarda una nueva lectura en la base de datos.

        Args:
            reading (Reading): Entidad de lectura a persistir.

        Returns:
            Reading: Entidad guardada con ID y fecha asignados por la BD.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO lecturas (
                usuario_id, lectura_actual, lectura_anterior, consumo, costo
            ) VALUES (?, ?, ?, ?, ?)
            """,
            (
                reading.user_id,
                float(reading.lectura_actual),
                float(reading.lectura_anterior),
                float(reading.consumo),
                float(reading.costo),
            ),
        )
        reading_id = cursor.lastrowid
        self.conn.commit()

        # Recuperar la fecha asignada por la base de datos
        cursor.execute("SELECT fecha FROM lecturas WHERE id = ?", (reading_id,))
        row = cursor.fetchone()
        if row is None:
            raise RuntimeError("No se pudo recuperar la lectura guardada.")
        fecha = datetime.fromisoformat(row[0])

        return Reading(
            id=reading_id,
            user_id=reading.user_id,
            lectura_actual=reading.lectura_actual,
            lectura_anterior=reading.lectura_anterior,
            consumo=reading.consumo,
            costo=reading.costo,
            fecha=fecha,
        )

    def get_by_user_id(self, user_id: int) -> List[Reading]:
        """
        Obtiene todas las lecturas de un usuario, ordenadas por fecha descendente.

        Args:
            user_id (int): ID del usuario.

        Returns:
            List[Reading]: Lista de lecturas del usuario.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT id, usuario_id, lectura_actual, lectura_anterior, consumo, costo, fecha
            FROM lecturas
            WHERE usuario_id = ?
            ORDER BY fecha DESC
            """,
            (user_id,),
        )
        rows = cursor.fetchall()
        return [
            Reading(
                id=row[0],
                user_id=row[1],
                lectura_actual=Decimal(str(row[2])),
                lectura_anterior=Decimal(str(row[3])),
                consumo=Decimal(str(row[4])),
                costo=Decimal(str(row[5])),
                fecha=datetime.fromisoformat(row[6]),
            )
            for row in rows
        ]

    def get_last_by_user(self, user_id: int) -> Optional[Reading]:
        """
        Obtiene la última lectura registrada por un usuario.

        Args:
            user_id (int): ID del usuario.

        Returns:
            Optional[Reading]: Última lectura o None si no existe.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT id, usuario_id, lectura_actual, lectura_anterior, consumo, costo, fecha
            FROM lecturas
            WHERE usuario_id = ?
            ORDER BY fecha DESC
            LIMIT 1
            """,
            (user_id,),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return Reading(
            id=row[0],
            user_id=row[1],
            lectura_actual=Decimal(str(row[2])),
            lectura_anterior=Decimal(str(row[3])),
            consumo=Decimal(str(row[4])),
            costo=Decimal(str(row[5])),
            fecha=datetime.fromisoformat(row[6]),
        )

    def get_by_id(self, reading_id: int) -> Optional[Reading]:
        """
        Obtiene una lectura por su ID.

        Args:
            reading_id (int): ID de la lectura.

        Returns:
            Optional[Reading]: Lectura encontrada o None.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT id, usuario_id, lectura_actual, lectura_anterior, consumo, costo, fecha
            FROM lecturas
            WHERE id = ?
            """,
            (reading_id,),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return Reading(
            id=row[0],
            user_id=row[1],
            lectura_actual=Decimal(str(row[2])),
            lectura_anterior=Decimal(str(row[3])),
            consumo=Decimal(str(row[4])),
            costo=Decimal(str(row[5])),
            fecha=datetime.fromisoformat(row[6]),
        )

    def delete(self, reading_id: int) -> None:
        """
        Elimina una lectura por su ID.

        Args:
            reading_id (int): ID de la lectura a eliminar.
        """
        if reading_id <= 0:
            raise ValueError("ID de lectura inválido.")
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM lecturas WHERE id = ?", (reading_id,))
        self.conn.commit()