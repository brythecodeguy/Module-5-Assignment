from __future__ import annotations

from decimal import Decimal, InvalidOperation

from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError

class InputValidator:
    @staticmethod
    def validate_number(value, config) -> Decimal:
        raw = str(value).strip()

        try:
            d = Decimal(raw)
        except (InvalidOperation, ValueError, TypeError):
            raise ValidationError(f"Invalid number format: {value}")

        if abs(d) > Decimal(str(config.max_input_value)):
            raise ValidationError("Value exceeds maximum allowed")

        return d.normalize()