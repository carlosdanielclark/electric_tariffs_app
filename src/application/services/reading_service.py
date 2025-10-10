from decimal import Decimal, InvalidOperation
from typing import List, Optional
from domain.entities.reading import Reading
from infrastructure.database.repositories.reading_repository import ReadingRepository
from infrastructure.logging.activity_logger import ActivityLogger
from services.tariff_calculator import TariffCalculator


class ReadingService:
    def __init__(self, db_connection, logger: ActivityLogger) -> None:
        self.repository = ReadingRepository(db_connection)
        self.logger = logger

    def register_reading(self, user_id: int, lectura_actual_str: str, lectura_anterior_str: str) -> Reading:
        """
        Registra una nueva lectura. Recibe strings para validación segura.

        Args:
            user_id (int): ID del usuario autenticado.
            lectura_actual_str (str): Lectura actual como string.
            lectura_anterior_str (str): Lectura anterior como string.

        Returns:
            Reading: Entidad guardada.

        Raises:
            ValueError: Si los valores no son numéricos o el consumo no es positivo.
        """
        try:
            lectura_actual = Decimal(lectura_actual_str.strip())
            lectura_anterior = Decimal(lectura_anterior_str.strip())
        except InvalidOperation as e:
            raise ValueError(f"Valores no numéricos: {e}")

        if lectura_actual <= lectura_anterior:
            raise ValueError("La lectura actual debe ser mayor que la anterior.")

        consumo = lectura_actual - lectura_anterior
        costo = TariffCalculator.calcular_costo(consumo)

        reading = Reading(
            id=0,
            user_id=user_id,
            lectura_actual=lectura_actual,
            lectura_anterior=lectura_anterior,
            consumo=consumo,
            costo=costo,
            fecha=None
        )

        saved = self.repository.save(reading)
        self.logger.log_event(user_id, "registro_lectura", f"consumo: {consumo} kWh, costo: {costo} CUP")
        return saved

    def get_all_readings_by_user(self, user_id: int) -> List[Reading]:
        return self.repository.get_by_user_id(user_id)

    def get_last_reading_by_user(self, user_id: int) -> Optional[Reading]:
        return self.repository.get_last_by_user(user_id)

    def delete_reading(self, reading_id: int) -> None:
        reading = self.repository.get_by_id(reading_id)
        if reading:
            self.repository.delete(reading_id)
            self.logger.log_event(
                reading.user_id,
                "eliminacion_lectura",
                f"Lectura ID {reading_id} eliminada"
            )