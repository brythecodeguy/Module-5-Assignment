from decimal import Decimal
from app.calculation import Calculation
from app.calculator_memento import CalculatorMemento

def test_memento_to_dict_and_from_dict():
    c = Calculation("Addition", Decimal("2"), Decimal("3"))
    m = CalculatorMemento(history=[c])

    d = m.to_dict()
    m2 = CalculatorMemento.from_dict(d)

    assert len(m2.history) == 1
    assert m2.history[0].result == Decimal("5")