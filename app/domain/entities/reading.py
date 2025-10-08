from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

@dataclass
class Reading:
    id: Optional[int]
    user_id: int
    lectura_actual: Decimal
    lectura_anterior: Decimal
    consumo: Decimal
    costo: Decimal
    fecha: datetime | None = None