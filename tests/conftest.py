import pytest
from app.calculation import CalculationFactory


@pytest.fixture(autouse=True)
def reset_calculation_factory_registry():
    """
    Prevent cross-test pollution of CalculationFactory._calculations.
    """
    original = dict(getattr(CalculationFactory, "_calculations", {}))
    yield
    CalculationFactory._calculations.clear()
    CalculationFactory._calculations.update(original)
