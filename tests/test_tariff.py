from app.application.services.tariff_service import TariffCalculator


def test_tariff_basic() -> None:  # ← Añadido
    calc = TariffCalculator()
    res = calc.calculate(50)
    assert res["consumo"] == 50.0
    assert abs(res["subtotal_energia"] - 5.0) < 1e-6
    assert res["cargo_fijo"] == 0.0
    assert res["impuesto"] == 0.0
    assert abs(res["total"] - 5.0) < 1e-6


def test_tariff_multi_tramos() -> None:  # ← Añadido
    calc = TariffCalculator()
    res = calc.calculate(150)
    assert abs(res["subtotal_energia"] - 17.5) < 1e-6
    assert abs(res["total"] - 17.5) < 1e-6


def test_tariff_with_cargo_e_impuesto() -> None:  # ← Añadido
    calc = TariffCalculator(cargo_fijo=2.0, impuesto=0.1)
    res = calc.calculate(100)
    assert abs(res["subtotal_energia"] - 10.0) < 1e-6
    assert abs(res["cargo_fijo"] - 2.0) < 1e-6
    assert abs(res["impuesto"] - 1.2) < 1e-6
    assert abs(res["total"] - 13.2) < 1e-6