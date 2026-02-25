import pytest
from decimal import Decimal
from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError
from app.input_validators import InputValidator


@pytest.fixture
def config():
    return CalculatorConfig(max_input_value=Decimal("1000000"))


def test_validate_number_positive_integer(config):
    assert InputValidator.validate_number(123, config) == Decimal("123")


def test_validate_number_positive_decimal(config):
    assert InputValidator.validate_number(123.456, config) == Decimal("123.456").normalize()


def test_validate_number_positive_string_integer(config):
    assert InputValidator.validate_number("123", config) == Decimal("123")


def test_validate_number_positive_string_decimal(config):
    assert InputValidator.validate_number("123.456", config) == Decimal("123.456").normalize()


def test_validate_number_negative_integer(config):
    assert InputValidator.validate_number(-789, config) == Decimal("-789")


def test_validate_number_negative_decimal(config):
    assert InputValidator.validate_number(-789.123, config) == Decimal("-789.123").normalize()


def test_validate_number_trimmed_string(config):
    assert InputValidator.validate_number("  456  ", config) == Decimal("456")


def test_validate_number_invalid_string(config):
    with pytest.raises(ValidationError, match=r"Invalid number format: abc"):
        InputValidator.validate_number("abc", config)


def test_validate_number_exceeds_max_value(config):
    with pytest.raises(ValidationError, match=r"Value exceeds maximum allowed"):
        InputValidator.validate_number(Decimal("1000001"), config)


def test_validate_number_exceeds_negative_max_value(config):
    with pytest.raises(ValidationError, match=r"Value exceeds maximum allowed"):
        InputValidator.validate_number(-Decimal("1000001"), config)


def test_validate_number_empty_string(config):
    with pytest.raises(ValidationError, match=r"Invalid number format:"):
        InputValidator.validate_number("", config)


def test_validate_number_whitespace_string(config):
    with pytest.raises(ValidationError, match=r"Invalid number format:"):
        InputValidator.validate_number("   ", config)


def test_validate_number_none(config):
    with pytest.raises(ValidationError, match=r"Invalid number format: None"):
        InputValidator.validate_number(None, config)


def test_validate_number_non_numeric_type(config):
    with pytest.raises(ValidationError, match=r"Invalid number format:"):
        InputValidator.validate_number([], config)