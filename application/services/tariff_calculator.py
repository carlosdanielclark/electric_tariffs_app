from decimal import Decimal
from typing import List, Tuple


class TariffCalculator:
    """
    Calcula el costo total y desglose por tramos según la tarifa eléctrica cubana.
    Usa Decimal para precisión financiera.
    """

    TRAMOS: List[Tuple[Decimal, Decimal, Decimal]] = [
        (Decimal('0'), Decimal('100'), Decimal('0.40')),
        (Decimal('101'), Decimal('150'), Decimal('1.30')),
        (Decimal('151'), Decimal('200'), Decimal('1.75')),
        (Decimal('201'), Decimal('250'), Decimal('3.00')),
        (Decimal('251'), Decimal('300'), Decimal('4.00')),
        (Decimal('301'), Decimal('350'), Decimal('7.50')),
        (Decimal('351'), Decimal('400'), Decimal('9.00')),
        (Decimal('401'), Decimal('450'), Decimal('10.00')),
        (Decimal('451'), Decimal('500'), Decimal('15.00')),
        (Decimal('501'), Decimal('Infinity'), Decimal('25.00')),
    ]

    @staticmethod
    def calcular_costo(consumo_kwh: Decimal) -> Decimal:
        """
        Calcula el costo total aplicando tarifas por tramos.

        Args:
            consumo_kwh (Decimal): Consumo total en kWh.

        Returns:
            Decimal: Costo total en CUP, redondeado a 2 decimales.
        """
        if consumo_kwh <= 0:
            return Decimal('0.00')

        costo_total = Decimal('0.00')
        consumo_restante = consumo_kwh

        for tramo_min, tramo_max, tarifa in TariffCalculator.TRAMOS:
            if consumo_restante <= 0:
                break

            if tramo_max == Decimal('Infinity'):
                consumo_en_tramo = consumo_restante
            else:
                max_en_tramo = tramo_max - tramo_min + 1
                consumo_en_tramo = min(consumo_restante, max_en_tramo)

            costo_total += consumo_en_tramo * tarifa
            consumo_restante -= consumo_en_tramo

        return costo_total.quantize(Decimal('0.01'))