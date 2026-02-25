import pytest
from app.operations import Operations


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (2.0, 3.0, 5.0),
        (-2.0, -3.0, -5.0),
        (0.0, 0.0, 0.0),
        (2.5, 3.5, 6.0),
    ],
    ids=["add_pos", "add_neg", "add_zeros", "add_floats"],
)
def test_add(a, b, expected):
    assert Operations.add(a, b) == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (5.0, 2.0, 3.0),
        (2.0, 5.0, -3.0),
        (-5.0, -2.0, -3.0),
    ],
    ids=["sub_pos", "sub_neg_result", "sub_neg_inputs"],
)
def test_subtract(a, b, expected):
    assert Operations.subtract(a, b) == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (4.0, 5.0, 20.0),
        (-4.0, 5.0, -20.0),
        (0.0, 99.0, 0.0),
    ],
    ids=["mul_pos", "mul_neg", "mul_zero"],
)
def test_multiply(a, b, expected):
    assert Operations.multiply(a, b) == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (10.0, 2.0, 5.0),
        (-10.0, 2.0, -5.0),
        (0.0, 5.0, 0.0),
    ],
    ids=["div_pos", "div_neg", "div_zero_num"],
)
def test_divide(a, b, expected):
    assert Operations.divide(a, b) == expected


@pytest.mark.parametrize("a", [1.0, -1.0, 0.0], ids=["pos", "neg", "zero"])
def test_divide_by_zero_raises(a):
    with pytest.raises(ValueError):
        Operations.divide(a, 0.0)
