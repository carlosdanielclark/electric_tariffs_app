from __future__ import annotations
from typing import Dict, List, Tuple


class TariffCalculator:
    """
    Calculadora de tarifa simple por tramos.
    Configuración por defecto:
      - cargo_fijo: monto fijo por periodo
      - tramos: lista de (limite_kwh, precio_por_kwh)
        El último tramo puede tener limite None (infinito)
      - impuesto: porcentaje (ej. 0.13 para 13% IVA)
    """

    def __init__(
        self,
        tramos: List[Tuple[float | None, float]] | None = None,
        cargo_fijo: float = 0.0,
        impuesto: float = 0.0,
    ):
        self.tramos = tramos or [(100.0, 0.10), (200.0, 0.15), (None, 0.20)]
        self.cargo_fijo = float(cargo_fijo)
        self.impuesto = float(impuesto)

    def calculate(self, consumo_kwh: float) -> Dict[str, float]:
        """
        Retorna desglose:
          - consumo: consumo_kwh
          - subtotal_energia: costo sin cargo fijo ni impuesto
          - cargo_fijo
          - impuesto
          - total
        """
        if consumo_kwh < 0:
            raise ValueError("Consumo no puede ser negativo")

        remaining = consumo_kwh
        last_limit = 0.0
        subtotal = 0.0

        for limit, price in self.tramos:
            if limit is None:
                qty = remaining
            else:
                qty = max(0.0, min(remaining, max(0.0, limit - last_limit)))
            subtotal += qty * price
            remaining -= qty
            last_limit = limit if limit is not None else last_limit
            if remaining <= 0:
                break

        subtotal = round(subtotal, 6)
        cargo_fijo = round(self.cargo_fijo, 6)
        base = subtotal + cargo_fijo
        impuesto_monto = round(base * float(self.impuesto), 6)
        total = round(base + impuesto_monto, 6)

        return {
            "consumo": float(consumo_kwh),
            "subtotal_energia": subtotal,
            "cargo_fijo": cargo_fijo,
            "impuesto": impuesto_monto,
            "total": total,
        }
