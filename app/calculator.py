from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
from typing import List, Optional
import logging
import pandas as pd
from pathlib import Path

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.calculator_memento import CalculatorMemento
from app.exceptions import HistoryError, OperationError, ValidationError
from app.history import HistoryObserver
from app.input_validators import InputValidator
from app.operations import Operation


class Calculator:
    def __init__(self, config: Optional[CalculatorConfig] = None):
        self.config = config or CalculatorConfig()
        self.config.ensure_directories()

        self.history: List[Calculation] = []
        self.observers: List[HistoryObserver] = []

        self.undo_stack: List[CalculatorMemento] = []
        self.redo_stack: List[CalculatorMemento] = []

        self.operation_strategy: Optional[Operation] = None 

        logging.info("Calculator initialized with configuration")

    def set_operation(self, operation: Operation) -> None:  
        self.operation_strategy = operation

    def add_observer(self, observer: HistoryObserver) -> None:
        self.observers.append(observer)

    def remove_observer(self, observer: HistoryObserver) -> None:
        self.observers.remove(observer)

    def _notify(self, calc: Calculation) -> None:
        for obs in self.observers:
            obs.update(calc)

    def perform_operation(self, a, b) -> Decimal:
        if self.operation_strategy is None:
            raise OperationError("No operation set")

        # validate -> Decimal
        x = InputValidator.validate_number(a, self.config)
        y = InputValidator.validate_number(b, self.config)

        # run strategy FIRST
        result = self.operation_strategy.execute(x, y) 

        # snapshot for undo
        self.undo_stack.append(CalculatorMemento(history=deepcopy(self.history)))
        self.redo_stack.clear()

        # store history as Calculation (but don't re-execute)
        op_label = str(self.operation_strategy)  # "Addition", "Division", etc.
        calc = Calculation(operation=op_label, operand1=x, operand2=y, result=result)
        self.history.append(calc)
        self._notify(calc)
        return result

    def clear_history(self) -> None:
        self.history.clear()
        self.undo_stack.clear()
        self.redo_stack.clear()

    def undo(self) -> bool:
        if not self.undo_stack:
            return False
        self.redo_stack.append(CalculatorMemento(history=deepcopy(self.history)))
        self.history = self.undo_stack.pop().history
        return True

    def redo(self) -> bool:
        if not self.redo_stack:
            return False
        self.undo_stack.append(CalculatorMemento(history=deepcopy(self.history)))
        self.history = self.redo_stack.pop().history
        return True

    def show_history(self) -> List[str]:
        return [str(c) for c in self.history]

    def save_history(self) -> None:
        try:
            df = pd.DataFrame([c.to_dict() for c in self.history])
            df.to_csv(self.config.history_file, index=False, encoding=self.config.default_encoding)
        except Exception as e:
            raise HistoryError(f"Failed to save history: {e}") from e

    def load_history(self) -> None:
        if not Path(self.config.history_file).exists():
            return
        try:
            df = pd.read_csv(self.config.history_file, encoding=self.config.default_encoding)
            rows = df.to_dict(orient="records") if not df.empty else []
            self.history = [Calculation.from_dict(r) for r in rows]
        except Exception as e:
            raise HistoryError(f"Failed to load history: {e}") from e