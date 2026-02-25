import logging
from datetime import datetime
from decimal import Decimal

import pytest

from app.calculation import Calculation
from app.exceptions import OperationError
from app.operations import Addition


def test_addition():
    c = Calculation(operation="Addition", operand1=Decimal("2"), operand2=Decimal("3"))
    assert c.result == Decimal("5")


def test_subtraction():
    c = Calculation(operation="Subtraction", operand1=Decimal("5"), operand2=Decimal("3"))
    assert c.result == Decimal("2")


def test_multiplication():
    c = Calculation(operation="Multiplication", operand1=Decimal("4"), operand2=Decimal("2"))
    assert c.result == Decimal("8")


def test_division():
    c = Calculation(operation="Division", operand1=Decimal("8"), operand2=Decimal("2"))
    assert c.result == Decimal("4")


def test_division_by_zero_raises_operation_error():
    # Match whatever your validator says (common: "Division by zero")
    with pytest.raises(OperationError, match=r"Division by zero"):
        Calculation(operation="Division", operand1=Decimal("8"), operand2=Decimal("0"))


def test_power():
    c = Calculation(operation="Power", operand1=Decimal("2"), operand2=Decimal("3"))
    assert c.result == Decimal("8")


def test_negative_power_raises_operation_error():
    # Make the regex flexible in case the wording is "Negative exponent(s) not allowed"
    with pytest.raises(OperationError, match=r"Negative exponent"):
        Calculation(operation="Power", operand1=Decimal("2"), operand2=Decimal("-3"))


def test_root():
    c = Calculation(operation="Root", operand1=Decimal("16"), operand2=Decimal("2"))
    assert c.result == Decimal("4")


def test_invalid_root_raises_operation_error():
    # Flexible match (message might be "Cannot take root of negative number")
    with pytest.raises(OperationError, match=r"negative"):
        Calculation(operation="Root", operand1=Decimal("-16"), operand2=Decimal("2"))


def test_unknown_operation_raises():
    with pytest.raises(OperationError, match=r"Unknown operation"):
        Calculation(operation="Unknown", operand1=Decimal("5"), operand2=Decimal("3"))


def test_to_dict_includes_timestamp_and_result():
    c = Calculation(operation="Addition", operand1=Decimal("2"), operand2=Decimal("3"))
    d = c.to_dict()

    assert d["operation"] == "Addition"
    assert d["operand1"] == "2"
    assert d["operand2"] == "3"
    assert d["result"] == "5"
    # Use fromisoformat to avoid microsecond string mismatches
    assert datetime.fromisoformat(d["timestamp"]) == c.timestamp


def test_from_dict_round_trip():
    ts = datetime.now().isoformat()
    data = {
        "operation": "Addition",
        "operand1": "2",
        "operand2": "3",
        "result": "5",
        "timestamp": ts,
    }

    c = Calculation.from_dict(data)
    assert c.operation == "Addition"
    assert c.operand1 == Decimal("2")
    assert c.operand2 == Decimal("3")
    assert c.result == Decimal("5")
    assert c.timestamp == datetime.fromisoformat(ts)


def test_from_dict_missing_timestamp_uses_now():
    data = {
        "operation": "Addition",
        "operand1": "2",
        "operand2": "3",
        "result": "5",
        # no timestamp
    }
    c = Calculation.from_dict(data)
    assert c.result == Decimal("5")
    assert isinstance(c.timestamp, datetime)


def test_from_dict_invalid_data_raises():
    ts = datetime.now().isoformat()
    bad = {
        "operation": "Addition",
        "operand1": "not-a-number",
        "operand2": "3",
        "result": "5",
        "timestamp": ts,
    }
    with pytest.raises(OperationError, match=r"Invalid calculation data"):
        Calculation.from_dict(bad)


def test_from_dict_logs_warning_if_result_mismatch(caplog):
    ts = datetime.now().isoformat()
    data = {
        "operation": "Addition",
        "operand1": "2",
        "operand2": "3",
        "result": "999",
        "timestamp": ts,
    }

    with caplog.at_level(logging.WARNING):
        c = Calculation.from_dict(data)

    assert c.result == Decimal("5")
    assert "differs from computed result" in caplog.text


def test_format_result_precision():
    c = Calculation(operation="Division", operand1=Decimal("1"), operand2=Decimal("3"))
    assert c.format_result(precision=2) == "0.33"
    assert c.format_result(precision=10) == "0.3333333333"


def test_str_contains_operation_and_result():
    c = Calculation(operation="Addition", operand1=Decimal("2"), operand2=Decimal("3"))
    s = str(c)
    assert "Addition" in s
    assert "= 5" in s


def test_equality():
    # If __eq__ ignores timestamp, this passes.
    # If not, set a shared timestamp explicitly.
    ts = datetime.now()
    c1 = Calculation(operation="Addition", operand1=Decimal("2"), operand2=Decimal("3"), timestamp=ts)
    c2 = Calculation(operation="Addition", operand1=Decimal("2"), operand2=Decimal("3"), timestamp=ts)
    c3 = Calculation(operation="Subtraction", operand1=Decimal("5"), operand2=Decimal("3"), timestamp=ts)

    assert c1 == c2
    assert c1 != c3


def test_equality_notimplemented_path():
    c = Calculation(operation="Addition", operand1=Decimal("2"), operand2=Decimal("3"))
    assert (c == 123) is False

def test_normalize_op():
    assert Calculation._normalize_op("  ADD  ") == "add"

def test_to_dict_with_operation_instance():
    calc = Calculation(
        operation=Addition(),
        operand1=Decimal("2"),
        operand2=Decimal("3"),
        result=Decimal("5")
    )

    data = calc.to_dict()

    assert data["operation"] == "Addition"
