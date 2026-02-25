from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional, Union
import logging

from app.exceptions import OperationError, ValidationError
from app.operations import OperationFactory, Operation


@dataclass
class Calculation:
    operation: Union[str, Operation]
    operand1: Decimal
    operand2: Decimal
    timestamp: datetime = field(default_factory=datetime.now)

    # allow precomputed result (Calculator strategy computes it first)
    result: Optional[Decimal] = None

    def __post_init__(self) -> None:
        # If result already provided, do not recompute
        if self.result is not None:
            return

        try:
            op = OperationFactory.create_operation(self.operation)
            self.result = op.execute(self.operand1, self.operand2)
        except ValidationError as e:
            #Calculation raises OperationError for op-validation problems
            raise OperationError(str(e)) from e
        except ValueError as e:
            raise OperationError("Unknown operation") from e

    @staticmethod
    def _normalize_op(name: str) -> str:
        return name.strip().lower()

    def to_dict(self) -> dict[str, str]:
        # store operation name consistently as a string
        op_name = self.operation if isinstance(self.operation, str) else str(self.operation)
        return {
            "operation": op_name,
            "operand1": str(self.operand1),
            "operand2": str(self.operand2),
            "result": str(self.result),
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Calculation":
        try:
            op = data["operation"]
            a = Decimal(str(data["operand1"]))
            b = Decimal(str(data["operand2"]))
            saved_result = Decimal(str(data["result"]))

            ts_raw = data.get("timestamp")
            ts = datetime.fromisoformat(ts_raw) if ts_raw else datetime.now()
        except Exception as e:
            raise OperationError("Invalid calculation data") from e

        # Let Calculation compute result normally, then compare/log warning
        calc = cls(operation=op, operand1=a, operand2=b, timestamp=ts)

        if calc.result != saved_result:
            logging.warning(
                f"Loaded calculation result {saved_result} differs from computed result {calc.result}"
            )
        return calc

    def format_result(self, precision: int) -> str:
        q = Decimal("1").scaleb(-precision)  # 10^-precision
        return str(self.result.quantize(q))  # type: ignore[union-attr]

    def __str__(self) -> str:
        op_name = self.operation if isinstance(self.operation, str) else str(self.operation)
        return f"{op_name} ({self.operand1}, {self.operand2}) = {self.result}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Calculation):
            return NotImplemented

        # ignore timestamp
        self_op = self.operation if isinstance(self.operation, str) else str(self.operation)
        other_op = other.operation if isinstance(other.operation, str) else str(other.operation)

        return (
            self_op == other_op
            and self.operand1 == other.operand1
            and self.operand2 == other.operand2
            and self.result == other.result
        )
    @classmethod
    def from_dict(cls, data: dict) -> "Calculation":
        try:
            op = data["operation"]
            a = Decimal(str(data["operand1"]))
            b = Decimal(str(data["operand2"]))
            saved_result = Decimal(str(data["result"]))
            ts_raw = data.get("timestamp")
            ts = datetime.fromisoformat(ts_raw) if ts_raw else datetime.now()
        except Exception as e:
            raise OperationError("Invalid calculation data") from e

        calc = cls(operation=op, operand1=a, operand2=b, timestamp=ts)
        if calc.result != saved_result:
            logging.warning(
                f"Loaded calculation result {saved_result} differs from computed result {calc.result}"
            )
        return calc

    def format_result(self, precision: int) -> str:
        q = Decimal("1").scaleb(-precision)  # 10^-precision
        return str(self.result.quantize(q))

    def __str__(self) -> str:
        return f"{self.operation} ({self.operand1}, {self.operand2}) = {self.result}"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Calculation):
            return NotImplemented
        return (
            self.operation == other.operation
            and self.operand1 == other.operand1
            and self.operand2 == other.operand2
            and self.result == other.result
        )