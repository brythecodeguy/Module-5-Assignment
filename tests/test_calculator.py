import pytest
from app.calculator import calculator

import builtins
import app.calculator as calc_mod

ERROR_MSG = "Invalid input. Please follow the format: <operation> <num1> <num2>"


def run_calculator_with_inputs(inputs, monkeypatch, capsys):
    it = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(it))

    with pytest.raises(SystemExit):
        calculator()

    return capsys.readouterr().out


# positive test cases
def test_add(monkeypatch, capsys):
    out = run_calculator_with_inputs(["add 2 3", "exit"], monkeypatch, capsys)
    assert "Result:" in out
    assert "AddCalculation" in out
    assert "= 5.0" in out


def test_subtract(monkeypatch, capsys):
    out = run_calculator_with_inputs(["subtract 9 4", "exit"], monkeypatch, capsys)
    assert "Result:" in out
    assert "SubtractCalculation" in out
    assert "= 5.0" in out


def test_multiply(monkeypatch, capsys):
    out = run_calculator_with_inputs(["multiply 4 5", "exit"], monkeypatch, capsys)
    assert "Result:" in out
    assert "MultiplyCalculation" in out
    assert "= 20.0" in out


def test_divide(monkeypatch, capsys):
    out = run_calculator_with_inputs(["divide 10 2", "exit"], monkeypatch, capsys)
    assert "Result:" in out
    assert "DivideCalculation" in out
    assert "= 5.0" in out


# negative test cases
def test_divide_by_zero(monkeypatch, capsys):
    out = run_calculator_with_inputs(["divide 5 0", "exit"], monkeypatch, capsys)
    assert "Cannot divide by zero" in out or "Division by zero" in out


def test_invalid_input(monkeypatch, capsys):
    out = run_calculator_with_inputs(["add two three", "exit"], monkeypatch, capsys)
    assert "Invalid input" in out


def test_invalid_arg_count(monkeypatch, capsys):
    out = run_calculator_with_inputs(["add 5", "exit"], monkeypatch, capsys)
    assert "Invalid input" in out


def test_calculator_invalid_operation(monkeypatch, capsys):
    out = run_calculator_with_inputs(["modulus 5 3", "exit"], monkeypatch, capsys)
    assert "Unsupported" in out or "Invalid operation" in out


def test_calculator_blank_input(monkeypatch, capsys):
    out = run_calculator_with_inputs(["", "exit"], monkeypatch, capsys)
    assert "Welcome" in out


def test_calculator_help_command(monkeypatch, capsys):
    out = run_calculator_with_inputs(["help", "exit"], monkeypatch, capsys)
    assert "Help" in out or "Usage" in out or "Commands" in out

def test_display_help_function_body(capsys):
    #display_help() print block
    calc_mod.display_help()
    out = capsys.readouterr().out
    assert "Calculator REPL Help" in out
    assert "Supported operations" in out
    assert "Special commands" in out


def test_display_history_empty_branch(capsys):
    #if not history -> print + return
    calc_mod.display_history([])
    out = capsys.readouterr().out
    assert "No calculations performed yet." in out


def test_history_command_path(monkeypatch, capsys):
    #if command == "history": display_history(history); continue
    out = run_calculator_with_inputs(["history", "exit"], monkeypatch, capsys)
    assert "No calculations performed yet." in out


def test_generic_exception_handler(monkeypatch, capsys):
    #except Exception as e: print(f"Error during calculation: {e}")
    # Trigger by making __str__ raise a non-ValueError exception.
    from app.calculation import AddCalculation

    def boom_str(self):
        raise RuntimeError("boom")

    monkeypatch.setattr(AddCalculation, "__str__", boom_str)

    out = run_calculator_with_inputs(["add 1 2", "exit"], monkeypatch, capsys)
    assert "Error during calculation:" in out
    assert "boom" in out


def test_keyboard_interrupt_branch(monkeypatch, capsys):
    def raise_keyboard_interrupt(_):
        raise KeyboardInterrupt

    monkeypatch.setattr(builtins, "input", raise_keyboard_interrupt)

    with pytest.raises(SystemExit):
        calc_mod.calculator()

    out = capsys.readouterr().out
    assert "Keyboard interrupt detected. Goodbye!" in out


def test_eof_branch(monkeypatch, capsys):
    def raise_eof(_):
        raise EOFError

    monkeypatch.setattr(builtins, "input", raise_eof)

    with pytest.raises(SystemExit):
        calc_mod.calculator()

    out = capsys.readouterr().out
    assert "EOF detected. Goodbye!" in out

def test_display_history_with_items(monkeypatch, capsys):
    # First perform a calculation so history has something in it
    out = run_calculator_with_inputs(["add 2 3", "history", "exit"], monkeypatch, capsys)

    assert "Calculation History:" in out
    assert "1." in out
    assert "AddCalculation" in out
