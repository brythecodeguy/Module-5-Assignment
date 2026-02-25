import pytest
from decimal import Decimal

from app.operations import OperationFactory
from app.exceptions import ValidationError


@pytest.mark.parametrize(
    "op,a,b,expected",
    [
        ("add", "2", "3", "5"),
        ("add", "-2", "-3", "-5"),
        ("add", "0", "0", "0"),
        ("add", "2.5", "3.5", "6.0"),
        ("subtract", "5", "2", "3"),
        ("subtract", "2", "5", "-3"),
        ("subtract", "-5", "-2", "-3"),
        ("multiply", "4", "5", "20"),
        ("multiply", "-4", "5", "-20"),
        ("multiply", "0", "99", "0"),
        ("divide", "10", "2", "5"),
        ("divide", "-10", "2", "-5"),
        ("divide", "0", "5", "0"),
    ],
    ids=[
        "add_pos",
        "add_neg",
        "add_zeros",
        "add_floats",
        "sub_pos",
        "sub_neg_result",
        "sub_neg_inputs",
        "mul_pos",
        "mul_neg",
        "mul_zero",
        "div_pos",
        "div_neg",
        "div_zero_num",
    ],
)
def test_factory_operations(op, a, b, expected):
    operation = OperationFactory.create_operation(op)
    result = operation.execute(Decimal(a), Decimal(b))
    assert str(result) == str(Decimal(expected))


@pytest.mark.parametrize("a", ["1", "-1", "0"], ids=["pos", "neg", "zero"])
def test_divide_by_zero_raises_validation_error(a):
    operation = OperationFactory.create_operation("divide")
    with pytest.raises(ValidationError):
        operation.execute(Decimal(a), Decimal("0"))


def test_root_zero_exponent_raises_validation_error():
    operation = OperationFactory.create_operation("root")
    with pytest.raises(ValidationError):
        operation.execute(Decimal("9"), Decimal("0"))

def test_factory_returns_same_instance_when_given_operation_instance():
    op = OperationFactory.create_operation("add")   
    out = OperationFactory.create_operation(op)     
    assert out is op