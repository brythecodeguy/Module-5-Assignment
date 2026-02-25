from __future__ import annotations

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict
from app.exceptions import ValidationError


class Operation(ABC):
    """Base class for all operations."""

    @abstractmethod
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        raise NotImplementedError  # pragma: no cover

    def validate(self, a: Decimal, b: Decimal) -> None:
        """Optional validation hook for subclasses."""
        return


class Addition(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate(a, b)
        return a + b


class Subtraction(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate(a, b)
        return a - b


class Multiplication(Operation):
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate(a, b)
        return a * b


class Division(Operation):
    def validate(self, a: Decimal, b: Decimal) -> None:
        if b == 0:
            raise ValidationError("Division by zero is not allowed")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate(a, b)
        return a / b


class Power(Operation):
    def validate(self, a: Decimal, b: Decimal) -> None:
        if b < 0:
            raise ValidationError("Negative exponents not supported")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate(a, b)
        return Decimal(pow(float(a), float(b)))


class Root(Operation):
    def validate(self, a: Decimal, b: Decimal) -> None:
        if a < 0:
            raise ValidationError("Cannot calculate root of negative number")
        if b == 0:
            raise ValidationError("Zero root is undefined")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate(a, b)
        return Decimal(pow(float(a), 1 / float(b)))


class OperationFactory:
    """Creates an Operation instance from a command string."""

    _ops: Dict[str, type[Operation]] = {
        "add": Addition,
        "subtract": Subtraction,
        "multiply": Multiplication,
        "divide": Division,
        "power": Power,
        "root": Root,
    }

    @classmethod
    def create_operation(cls, name: str) -> Operation:
        op_cls = cls._ops.get(name.lower())
        if not op_cls:
            raise ValueError(f"Unknown operation: {name}")
        return op_cls()

class Operations:
    @staticmethod
    def add(a: float, b: float) -> float:
        return float(a) + float(b)

    @staticmethod
    def subtract(a: float, b: float) -> float:
        return float(a) - float(b)

    @staticmethod
    def multiply(a: float, b: float) -> float:
        return float(a) * float(b)

    @staticmethod
    def divide(a: float, b: float) -> float:
        if float(b) == 0.0:
            raise ValueError("Division by zero is not allowed")
        return float(a) / float(b)