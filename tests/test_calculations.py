import pytest

from app.calculation import (
    CalculationFactory,
    AddCalculation,
    SubtractCalculation,
    MultiplyCalculation,
    DivideCalculation,
)


@pytest.mark.parametrize(
    "calc_type, a, b, expected, expected_class",
    [
        ("add", 10.0, 5.0, 15.0, AddCalculation),
        ("subtract", 10.0, 5.0, 5.0, SubtractCalculation),
        ("multiply", 10.0, 5.0, 50.0, MultiplyCalculation),
        ("divide", 10.0, 5.0, 2.0, DivideCalculation),
    ],
)
def test_factory_creates_and_executes(calc_type, a, b, expected, expected_class):
    # Arrange / Act
    calc = CalculationFactory.create_calculation(calc_type, a, b)
    result = calc.execute()

    # Assert
    assert isinstance(calc, expected_class)
    assert result == expected


def test_factory_unsupported_type_raises():
    with pytest.raises(ValueError):
        CalculationFactory.create_calculation("modulus", 10.0, 5.0)


def test_factory_duplicate_registration_raises():
    # Hits the branch you showed in your coverage snippet:
    # if calculation_type_lower in cls._calculations: raise ValueError(...)
    with pytest.raises(ValueError):
        CalculationFactory.register_calculation("add")(AddCalculation)


def test_repr_is_covered():
    calc = DivideCalculation(10.0, 2.0)
    r = repr(calc)
    assert "DivideCalculation" in r
    assert "a=" in r and "b=" in r


def test_str_is_covered():
    calc = AddCalculation(2.0, 3.0)
    s = str(calc)
    # Don’t be overly strict on formatting, just prove the path runs
    assert "AddCalculation" in s or "Add" in s
    assert "2.0" in s and "3.0" in s