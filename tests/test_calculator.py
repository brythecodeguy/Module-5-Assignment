import pytest
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch, PropertyMock

import builtins
import pandas as pd
from datetime import datetime

from app.calculator import Calculator
from app.calculator_repl import calculator_repl
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError, ValidationError, HistoryError
from app.history import LoggingObserver, AutoSaveObserver
from app.operations import OperationFactory


@pytest.fixture
def calculator():
    """
    Build a Calculator using a temp base_dir so file paths never touch real disk locations.
    We patch the config properties to point into the temp directory.
    """
    with TemporaryDirectory() as td:
        temp = Path(td)
        cfg = CalculatorConfig(base_dir=temp)

        with (
            patch.object(CalculatorConfig, "log_dir", new_callable=PropertyMock) as p_log_dir,
            patch.object(CalculatorConfig, "log_file", new_callable=PropertyMock) as p_log_file,
            patch.object(CalculatorConfig, "history_dir", new_callable=PropertyMock) as p_hist_dir,
            patch.object(CalculatorConfig, "history_file", new_callable=PropertyMock) as p_hist_file,
        ):
            p_log_dir.return_value = temp / "logs"
            p_log_file.return_value = temp / "logs" / "calculator.log"
            p_hist_dir.return_value = temp / "history"
            p_hist_file.return_value = temp / "history" / "calculator_history.csv"

            yield Calculator(config=cfg)

# Calculator initialization
def test_calculator_starts_empty(calculator):
    assert calculator.history == []
    assert calculator.undo_stack == []
    assert calculator.redo_stack == []
    assert calculator.operation_strategy is None

# Observers

def test_add_and_remove_observer(calculator):
    obs = LoggingObserver()
    calculator.add_observer(obs)
    assert obs in calculator.observers

    calculator.remove_observer(obs)
    assert obs not in calculator.observers


def test_autosave_observer_can_be_added(calculator):
    obs = AutoSaveObserver(calculator)
    calculator.add_observer(obs)
    assert obs in calculator.observers

# Setting operations + performing

def test_set_operation_sets_strategy(calculator):
    op = OperationFactory.create_operation("add")
    calculator.set_operation(op)
    assert calculator.operation_strategy is op


def test_perform_operation_addition(calculator):
    calculator.set_operation(OperationFactory.create_operation("add"))
    result = calculator.perform_operation("2", "3")
    assert result == Decimal("5")


def test_perform_operation_requires_strategy(calculator):
    with pytest.raises(OperationError, match="No operation set"):
        calculator.perform_operation("2", "3")


def test_perform_operation_invalid_number_raises_validation(calculator):
    calculator.set_operation(OperationFactory.create_operation("add"))
    with pytest.raises(ValidationError):
        calculator.perform_operation("not-a-number", "3")


def test_division_by_zero_raises_validation(calculator):
    calculator.set_operation(OperationFactory.create_operation("divide"))
    with pytest.raises(ValidationError):
        calculator.perform_operation("5", "0")


# Undo / Redo

def test_undo_restores_previous_state(calculator):
    calculator.set_operation(OperationFactory.create_operation("add"))
    calculator.perform_operation("2", "3")
    assert len(calculator.history) == 1

    ok = calculator.undo()
    assert ok is True
    assert calculator.history == []


def test_redo_restores_undone_state(calculator):
    calculator.set_operation(OperationFactory.create_operation("add"))
    calculator.perform_operation("2", "3")
    calculator.undo()

    ok = calculator.redo()
    assert ok is True
    assert len(calculator.history) == 1

# Persistence: save / load

@patch("app.calculator.pd.DataFrame.to_csv")
def test_save_history_calls_to_csv(mock_to_csv, calculator):
    calculator.set_operation(OperationFactory.create_operation("add"))
    calculator.perform_operation("2", "3")
    calculator.save_history()
    mock_to_csv.assert_called_once()


@patch("app.calculator.pd.read_csv")
@patch("app.calculator.Path.exists", return_value=True)
def test_load_history_reads_csv(mock_exists, mock_read_csv, calculator):
    mock_read_csv.return_value = pd.DataFrame(
        [
            {
                "operation": "Addition",
                "operand1": "2",
                "operand2": "3",
                "result": "5",
                "timestamp": datetime.now().isoformat(),
            }
        ]
    )

    calculator.load_history()
    assert len(calculator.history) == 1
    row = calculator.history[0]
    assert row.operation == "Addition"
    assert row.operand1 == Decimal("2")
    assert row.operand2 == Decimal("3")
    assert row.result == Decimal("5")


def test_save_history_raises_history_error_on_failure(calculator, monkeypatch):
    def boom(*args, **kwargs):
        raise RuntimeError("disk full")

    monkeypatch.setattr(pd.DataFrame, "to_csv", boom)

    with pytest.raises(HistoryError):
        calculator.save_history()


# REPL tests

@patch("builtins.input", side_effect=["exit"])
@patch("builtins.print")
def test_repl_exit_saves_and_quits(mock_print, mock_input):
    with patch("app.calculator.Calculator.save_history") as save_mock:
        calculator_repl()
        save_mock.assert_called_once()
        mock_print.assert_any_call("History saved successfully.")
        mock_print.assert_any_call("Goodbye!")


@patch("builtins.input", side_effect=["help", "exit"])
@patch("builtins.print")
def test_repl_help_then_exit(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("\nAvailable commands:")


@patch("builtins.input", side_effect=["add", "2", "3", "exit"])
@patch("builtins.print")
def test_repl_addition_flow(mock_print, mock_input):
    calculator_repl()
    # accept "5" or "5.0"
    printed = " ".join(str(c.args[0]) for c in mock_print.call_args_list if c.args)
    assert "Result:" in printed
    assert "5" in printed

@patch("builtins.input", side_effect=["history", "exit"])
@patch("builtins.print")
def test_repl_history_empty_then_exit(mock_print, mock_input):
    calculator_repl()
    printed = " ".join(str(c.args[0]) for c in mock_print.call_args_list if c.args)
    assert "No calculations in history" in printed
    assert "Goodbye!" in printed


@patch("builtins.input", side_effect=["bogus", "exit"])
@patch("builtins.print")
def test_repl_unknown_command(mock_print, mock_input):
    calculator_repl()
    printed = " ".join(str(c.args[0]) for c in mock_print.call_args_list if c.args)
    assert "Unknown command" in printed


@patch("builtins.input", side_effect=["add", "cancel", "exit"])
@patch("builtins.print")
def test_repl_cancel_first_number(mock_print, mock_input):
    calculator_repl()
    printed = " ".join(str(c.args[0]) for c in mock_print.call_args_list if c.args)
    assert "Operation cancelled" in printed


@patch("builtins.input", side_effect=["add", "2", "cancel", "exit"])
@patch("builtins.print")
def test_repl_cancel_second_number(mock_print, mock_input):
    calculator_repl()
    printed = " ".join(str(c.args[0]) for c in mock_print.call_args_list if c.args)
    assert "Operation cancelled" in printed


@patch("builtins.input", side_effect=["clear", "exit"])
@patch("builtins.print")
def test_repl_clear(mock_print, mock_input):
    calculator_repl()
    printed = " ".join(str(c.args[0]) for c in mock_print.call_args_list if c.args)
    assert "History cleared" in printed


@patch("builtins.input", side_effect=["undo", "redo", "exit"])
@patch("builtins.print")
def test_repl_undo_redo_when_empty(mock_print, mock_input):
    calculator_repl()
    printed = " ".join(str(c.args[0]) for c in mock_print.call_args_list if c.args)
    assert "Nothing to undo" in printed
    assert "Nothing to redo" in printed


@patch("builtins.input", side_effect=["save", "load", "exit"])
@patch("builtins.print")
def test_repl_save_and_load(mock_print, mock_input):
    # Patch where Calculator is USED (inside calculator_repl module)
    with (
        patch("app.calculator_repl.Calculator.save_history") as save_mock,
        patch("app.calculator_repl.Calculator.load_history") as load_mock,
    ):
        calculator_repl()

        save_mock.assert_called()
        load_mock.assert_called_once()

    printed = " ".join(str(c.args[0]) for c in mock_print.call_args_list if c.args)
    assert "History saved successfully" in printed
    assert "History loaded successfully" in printed

@patch("builtins.print")
def test_repl_keyboard_interrupt_then_exit(mock_print):
    # input() raises KeyboardInterrupt once, then returns "exit"
    with patch.object(builtins, "input", side_effect=[KeyboardInterrupt, "exit"]):
        calculator_repl()
    printed = " ".join(str(c.args[0]) for c in mock_print.call_args_list if c.args)
    assert "Operation cancelled" in printed

@patch("builtins.print")
def test_repl_eof_exits(mock_print):
    with patch.object(builtins, "input", side_effect=[EOFError]):
        calculator_repl()
    printed = " ".join(str(c.args[0]) for c in mock_print.call_args_list if c.args)
    assert "Input terminated" in printed or "Exiting" in printed