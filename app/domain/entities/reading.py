from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Reading:
    id: Optional[int]
    user_id: int
    lectura_actual: float
    lectura_anterior: float
    consumo: float
    costo: float
    fecha: datetime | None = None
