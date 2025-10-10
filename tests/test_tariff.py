from decimal import Decimal
from application.services.tariff_calculator import TariffCalculator

def test_tariff_basic() -> None:
    calc = TariffCalculator()
    res = calc.calculate(Decimal("50"))
    assert res["consumo"] == Decimal("50")
    assert res["subtotal_energia"] == Decimal("5.0")
    assert res["cargo_fijo"] == Decimal("0.0")
    assert res["impuesto"] == Decimal("0.0")
    assert res["total"] == Decimal("5.0")

def test_tariff_multi_tramos() -> None:
    calc = TariffCalculator()
    res = calc.calculate(Decimal("150"))
    assert res["subtotal_energia"] == Decimal("17.5")
    assert res["total"] == Decimal("17.5")

def test_tariff_with_cargo_e_impuesto() -> None:
    calc = TariffCalculator(cargo_fijo=Decimal("2.0"), impuesto=Decimal("0.1"))
    res = calc.calculate(Decimal("100"))
    assert res["subtotal_energia"] == Decimal("10.0")
    assert res["cargo_fijo"] == Decimal("2.0")
    assert res["impuesto"] == Decimal("1.2")
    assert res["total"] == Decimal("13.2")