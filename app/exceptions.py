class CalculatorError(Exception):
    """Base exception for the calculator application."""


class ConfigurationError(CalculatorError):
    """Raised when configuration settings are invalid."""


class InvalidOperationError(CalculatorError):
    """Raised when an operation command is not supported."""


class InvalidNumberError(CalculatorError):
    """Raised when input cannot be parsed into a number."""


class DivisionByZeroError(CalculatorError):
    """Raised when dividing by zero."""


class HistoryError(CalculatorError):
    """Raised for history load/save issues."""