from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from typing import List
from app.infrastructure.repositories.sqlite_reading_repository import SQLiteReadingRepository
from app.application.services.tariff_service import TariffCalculator
from app.domain.entities.reading import Reading


@dataclass
class NewReading:
    user_id: int
    lectura_actual: Decimal | float
    lectura_anterior: Decimal | float


class ReadingService:
    def __init__(
        self,
        reading_repo: SQLiteReadingRepository | None = None,
        tariff_calculator: TariffCalculator | None = None,
    ):
        self.reading_repo = reading_repo or SQLiteReadingRepository()
        self.tariff_calculator = tariff_calculator or TariffCalculator()

    def record_reading(self, reading: NewReading) -> Reading:
        actual = Decimal(str(reading.lectura_actual))
        anterior = Decimal(str(reading.lectura_anterior))

        if actual < anterior:
            raise ValueError("Lectura actual no puede ser menor que lectura anterior")
        consumo = actual - anterior
        tarifa = self.tariff_calculator.calculate(consumo)
        costo = tarifa["total"]
        return self.reading_repo.add_reading(
            user_id=reading.user_id,
            lectura_actual=actual,
            lectura_anterior=anterior,
            consumo=consumo,
            costo=costo,
        )

    def get_readings_for_user(self, user_id: int) -> List[Reading]:
        return self.reading_repo.get_by_user(user_id)