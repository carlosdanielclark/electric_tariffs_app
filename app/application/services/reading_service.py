from __future__ import annotations
from typing import List
from app.infrastructure.repositories.sqlite_reading_repository import (
    SQLiteReadingRepository,
)
from app.application.services.tariff_service import TariffCalculator
from app.domain.entities.reading import Reading


class ReadingService:
    def __init__(
        self,
        reading_repo: SQLiteReadingRepository | None = None,
        tariff_calculator: TariffCalculator | None = None,
    ):
        self.reading_repo = reading_repo or SQLiteReadingRepository()
        self.tariff_calculator = tariff_calculator or TariffCalculator()

    def record_reading(
        self, user_id: int, lectura_actual: float, lectura_anterior: float
    ) -> Reading:
        if lectura_actual < lectura_anterior:
            raise ValueError("Lectura actual no puede ser menor que lectura anterior")
        consumo = round(float(lectura_actual - lectura_anterior), 6)
        tarifa = self.tariff_calculator.calculate(consumo)
        costo = tarifa["total"]
        return self.reading_repo.add_reading(
            user_id=user_id,
            lectura_actual=lectura_actual,
            lectura_anterior=lectura_anterior,
            consumo=consumo,
            costo=costo,
        )

    def get_readings_for_user(self, user_id: int) -> List[Reading]:
        return self.reading_repo.get_by_user(user_id)
