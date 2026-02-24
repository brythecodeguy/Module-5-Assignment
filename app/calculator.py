from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List

import pandas as pd

from app.calculation import Calculation, CalculationFactory
from app.calculator_config import CalculatorConfig
from app.exceptions import HistoryError
from app.history import HistoryObserver


@dataclass
class Calculator:
    """
    Facade for calculator subsystems:
    - config
    - history list
    - observers (logging/autosave)
    - persistence (pandas CSV)
    """
    config: CalculatorConfig
    history: List[Calculation]

    def __init__(self, config: CalculatorConfig | None = None):
        self.config = config or CalculatorConfig()
        self.history = []
        self._observers: List[HistoryObserver] = []
        self.config.ensure_directories()

    def add_observer(self, observer: HistoryObserver) -> None:
        self._observers.append(observer)

    def _notify(self, calc: Calculation) -> None:
        for obs in self._observers:
            obs.update(calc)

    def calculate(self, operation: str, a: float, b: float) -> Calculation:
        calc = CalculationFactory.create_calculation(operation, a, b)
        # store
        self.history.append(calc)
        # notify observers
        self._notify(calc)
        return calc

    def clear_history(self) -> None:
        self.history.clear()

    def save_history(self) -> None:
        """Persist history to CSV using pandas."""
        try:
            rows = []
            for c in self.history:
                rows.append(
                    {
                        "operation": c.operation,
                        "operand1": c.operand1,
                        "operand2": c.operand2,
                        "result": c.result,
                        "timestamp": datetime.utcnow().isoformat(),
                    }
                )
            df = pd.DataFrame(rows)
            df.to_csv(self.config.history_file, index=False, encoding=self.config.default_encoding)
        except Exception as e:  # pragma: no cover
            raise HistoryError(f"Failed to save history: {e}") from e

    def load_history(self) -> None:
        """Load history from CSV using pandas."""
        if not self.config.history_file.exists():
            return
        try:
            df = pd.read_csv(self.config.history_file, encoding=self.config.default_encoding)
            self.history.clear()
            for row in df.to_dict(orient="records"):
                # rebuild Calculation objects via factory
                op = str(row.get("operation"))
                a = float(row.get("operand1"))
                b = float(row.get("operand2"))
                self.history.append(CalculationFactory.create_calculation(op, a, b))
        except Exception as e:  # pragma: no cover
            raise HistoryError(f"Failed to load history: {e}") from e