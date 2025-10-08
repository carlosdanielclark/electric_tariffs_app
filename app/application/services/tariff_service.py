from __future__ import annotations
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List, Tuple


def _to_decimal(value: float | Decimal) -> Decimal:
    return Decimal(str(value)) if isinstance(value, float) else value


class TariffCalculator:
    """
    Calculadora de tarifa simple por tramos.
    Configuración por defecto:
      - cargo_fijo: monto fijo por periodo
      - tramos: lista de (limite_kwh, precio_por_kwh)
        El último tramo puede tener limite None (infinito)
      - impuesto: porcentaje (ej. Decimal('0.13') para 13% IVA)
    """

    def __init__(
        self,
        tramos: List[Tuple[Decimal | None, Decimal]] | None = None,
        cargo_fijo: Decimal | float = Decimal("0.0"),
        impuesto: Decimal | float = Decimal("0.0"),
    ):
        self.tramos = tramos or [
            (Decimal("100.0"), Decimal("0.40")),
            (Decimal("150.0"), Decimal("1.30")),
            (None, Decimal("0.20")),
        ]
        self.cargo_fijo = _to_decimal(cargo_fijo)
        self.impuesto = _to_decimal(impuesto)

    def calculate(self, consumo_kwh: Decimal | float) -> Dict[str, Decimal]:
        consumo = _to_decimal(consumo_kwh)
        if consumo < 0:
            raise ValueError("Consumo no puede ser negativo")

        remaining = consumo
        last_limit = Decimal("0.0")
        subtotal = Decimal("0.0")

        for limit, price in self.tramos:
            if limit is None:
                qty = remaining
            else:
                qty = max(Decimal("0.0"), min(remaining, max(Decimal("0.0"), limit - last_limit)))
            subtotal += qty * price
            remaining -= qty
            last_limit = limit if limit is not None else last_limit
            if remaining <= 0:
                break

        base = subtotal + self.cargo_fijo
        impuesto_monto = (base * self.impuesto).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        total = (base + impuesto_monto).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        return {
            "consumo": consumo,
            "subtotal_energia": subtotal,
            "cargo_fijo": self.cargo_fijo,
            "impuesto": impuesto_monto,
            "total": total,
        }