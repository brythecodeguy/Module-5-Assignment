from __future__ import annotations
from abc import ABC, abstractmethod
import logging
from typing import Any
from app.calculation import Calculation


class HistoryObserver(ABC):
    """
    Abstract base class for observers that react to calculation events.
    """

    @abstractmethod
    def update(self, calculation: Calculation) -> None:
        """Handle a new calculation event."""
        raise NotImplementedError  # pragma: no cover


class LoggingObserver(HistoryObserver):
    """Observer that logs calculations."""

    def update(self, calculation: Calculation) -> None:
        if calculation is None:
            raise AttributeError("Calculation cannot be None")

        logging.info(
            f"Calculation performed: {calculation.operation} "
            f"({calculation.operand1}, {calculation.operand2}) = "
            f"{calculation.result}"
        )


class AutoSaveObserver(HistoryObserver):
    """
    Observer that triggers calculator.save_history() when autosave is enabled.
    Calculator must have config.auto_save and save_history()
    """

    def __init__(self, calculator: Any):
        if calculator is None:
            raise TypeError("Calculator must have 'config' and 'save_history' attributes")

        if not hasattr(calculator, "config") or not hasattr(calculator, "save_history"):
            raise TypeError("Calculator must have 'config' and 'save_history' attributes")

        self.calculator = calculator

    def update(self, calculation: Calculation) -> None:
        if calculation is None:
            raise AttributeError("Calculation cannot be None")

        if self.calculator.config.auto_save:
            self.calculator.save_history()
            logging.info("History auto-saved")