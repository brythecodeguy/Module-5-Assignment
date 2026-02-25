from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import List, Optional

import pandas as pd

from pathlib import Path
from types import SimpleNamespace
from app.calculator_config import CalculatorConfig
from app.exceptions import HistoryError, OperationError, ValidationError
from app.history import HistoryObserver
from app.input_validators import InputValidator
from app.operations import Operation


@dataclass
class CalculatorMemento:
    history_snapshot: list[dict]


class Calculator:
    def __init__(self, config: Optional[CalculatorConfig] = None):
        self.config = config or CalculatorConfig()
        self.config.ensure_directories()

        self.history: list[dict] = []
        self.observers: List[HistoryObserver] = []

        self.operation_strategy: Optional[Operation] = None

        self.undo_stack: list[CalculatorMemento] = []
        self.redo_stack: list[CalculatorMemento] = []

    def add_observer(self, observer: HistoryObserver) -> None:
        self.observers.append(observer)

    def remove_observer(self, observer: HistoryObserver) -> None:
        self.observers.remove(observer)

    def notify_observers(self, calculation_obj) -> None:
        for obs in self.observers:
            obs.update(calculation_obj)

    def set_operation(self, operation: Operation) -> None:
        self.operation_strategy = operation

    def perform_operation(self, a, b) -> Decimal:
        if not self.operation_strategy:
            raise OperationError("No operation set")

        validated_a = InputValidator.validate_number(a, self.config)
        validated_b = InputValidator.validate_number(b, self.config)

        # memento
        self.undo_stack.append(CalculatorMemento(self.history.copy()))
        self.redo_stack.clear()

        result = self.operation_strategy.execute(validated_a, validated_b)

        row = {
            "operation": str(self.operation_strategy),
            "operand1": str(validated_a),
            "operand2": str(validated_b),
            "result": str(result),
        }
        self.history.append(row)

        # notify observers with a lightweight object that has the attributes observers expect
        calc_obj = SimpleNamespace(
            operation=row["operation"],
            operand1=validated_a,
            operand2=validated_b,
            result=result,
)
        self.notify_observers(calc_obj)
        return result

    def show_history(self) -> list[str]:
        return [
            f"{r['operation']}({r['operand1']}, {r['operand2']}) = {r['result']}"
            for r in self.history
        ]

    def clear_history(self) -> None:
        self.undo_stack.append(CalculatorMemento(self.history.copy()))
        self.redo_stack.clear()
        self.history.clear()

    def undo(self) -> bool:
        if not self.undo_stack:
            return False
        self.redo_stack.append(CalculatorMemento(self.history.copy()))
        self.history = self.undo_stack.pop().history_snapshot
        return True

    def redo(self) -> bool:
        if not self.redo_stack:
            return False
        self.undo_stack.append(CalculatorMemento(self.history.copy()))
        self.history = self.redo_stack.pop().history_snapshot
        return True

    def save_history(self) -> None:
        try:
            df = pd.DataFrame(self.history)
            df.to_csv(self.config.history_file, index=False, encoding=self.config.default_encoding)
        except Exception as e:
            raise HistoryError(f"Failed to save history: {e}") from e

    def load_history(self) -> None:
        if not self.config.history_file.exists():
            return
        try:
            df = pd.read_csv(self.config.history_file, encoding=self.config.default_encoding)
            self.history = df.to_dict(orient="records") if not df.empty else []
        except Exception as e:
            raise HistoryError(f"Failed to load history: {e}") from e