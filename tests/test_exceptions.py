import pytest
from app.exceptions import (
    CalculatorError,
    ValidationError,
    OperationError,
    ConfigurationError,
    HistoryError,
)


def test_calculator_error_base():
    with pytest.raises(CalculatorError) as exc:
        raise CalculatorError("base")
    assert str(exc.value) == "base"


def test_validation_error_is_calculator_error():
    with pytest.raises(CalculatorError):
        raise ValidationError("bad input")


def test_operation_error_is_calculator_error():
    with pytest.raises(CalculatorError):
        raise OperationError("bad operation")


def test_configuration_error_is_calculator_error():
    with pytest.raises(CalculatorError):
        raise ConfigurationError("bad config")


def test_history_error_is_calculator_error():
    with pytest.raises(CalculatorError):
        raise HistoryError("bad history")