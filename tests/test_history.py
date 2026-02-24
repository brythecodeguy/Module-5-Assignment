import pytest
from unittest.mock import Mock, patch
from app.calculation import Calculation
from app.history import LoggingObserver, AutoSaveObserver


def _mock_calc():
    c = Mock(spec=Calculation)
    c.operation = "addition"
    c.operand1 = 5
    c.operand2 = 3
    c.result = 8
    return c


@patch("logging.info")
def test_logging_observer_logs_calculation(logging_info_mock):
    observer = LoggingObserver()
    observer.update(_mock_calc())

    logging_info_mock.assert_called_once_with(
        "Calculation performed: addition (5, 3) = 8"
    )


def test_logging_observer_no_calculation_raises():
    observer = LoggingObserver()
    with pytest.raises(AttributeError):
        observer.update(None)


def test_autosave_observer_triggers_save_when_enabled():
    calculator_mock = Mock()
    calculator_mock.config = Mock()
    calculator_mock.config.auto_save = True

    observer = AutoSaveObserver(calculator_mock)
    observer.update(_mock_calc())

    calculator_mock.save_history.assert_called_once()


@patch("logging.info")
def test_autosave_observer_logs_autosave(logging_info_mock):
    calculator_mock = Mock()
    calculator_mock.config = Mock()
    calculator_mock.config.auto_save = True

    observer = AutoSaveObserver(calculator_mock)
    observer.update(_mock_calc())

    logging_info_mock.assert_called_once_with("History auto-saved")


def test_autosave_observer_does_not_trigger_save_when_disabled():
    calculator_mock = Mock()
    calculator_mock.config = Mock()
    calculator_mock.config.auto_save = False

    observer = AutoSaveObserver(calculator_mock)
    observer.update(_mock_calc())

    calculator_mock.save_history.assert_not_called()


def test_autosave_observer_invalid_calculator_none_raises():
    with pytest.raises(TypeError):
        AutoSaveObserver(None)


def test_autosave_observer_missing_required_attributes_raises():
    class BadCalc:
        pass

    with pytest.raises(TypeError):
        AutoSaveObserver(BadCalc())


def test_autosave_observer_no_calculation_raises():
    calculator_mock = Mock()
    calculator_mock.config = Mock()
    calculator_mock.config.auto_save = True

    observer = AutoSaveObserver(calculator_mock)
    with pytest.raises(AttributeError):
        observer.update(None)