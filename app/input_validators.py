from __future__ import annotations

from decimal import Decimal, InvalidOperation

from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError


class InputValidator:
    @staticmethod
    def validate_number(value: str | int | float | Decimal, config: CalculatorConfig) -> Decimal:
        try:
            d = Decimal(str(value).strip())
        except (InvalidOperation, ValueError, TypeError):
            raise ValidationError("Invalid number input")

        # optional max range rule
        if abs(d) > Decimal(str(config.max_input_value)):
            raise ValidationError("Input exceeds maximum allowed value")

        return d