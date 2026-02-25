class CalculatorError(Exception):
    """Base exception for the calculator application."""


class ConfigurationError(CalculatorError):
    """Raised when configuration settings are invalid."""


class ValidationError(CalculatorError):
    """Raised when user input/operands fail validation."""


class OperationError(CalculatorError):
    """Raised when an operation cannot be performed."""


class InvalidOperationError(CalculatorError):
    """Raised when an operation command is not supported."""


class InvalidNumberError(CalculatorError):
    """Raised when input cannot be parsed into a number."""


class DivisionByZeroError(CalculatorError):
    """Raised when dividing by zero."""


class HistoryError(CalculatorError):
    """Raised for history load/save issues."""