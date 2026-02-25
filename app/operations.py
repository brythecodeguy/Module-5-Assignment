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
    _operations: Dict[str, type] = {
        # REPL command names
        "add": Addition,
        "subtract": Subtraction,
        "multiply": Multiplication,
        "divide": Division,
        "power": Power,
        "root": Root,

        # Calculation operation names
        "addition": Addition,
        "subtraction": Subtraction,
        "multiplication": Multiplication,
        "division": Division,
    }

    @classmethod
    def create_operation(cls, operation_type) -> Operation:
        # If accidentally passed an instance, just return it
        if isinstance(operation_type, Operation):
            return operation_type

        # otherwise, look up by name
        name = str(operation_type).strip().lower()
        operation_class = cls._operations.get(name)
        if not operation_class:
            raise ValueError(f"Unknown operation: {operation_type}")
        return operation_class()

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