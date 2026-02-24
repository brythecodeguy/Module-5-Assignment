import sys
import readline  # enables terminal history/editing
from typing import List

from app.calculation import Calculation, CalculationFactory


SHORTCUTS = {
    "sub": "subtract",
    "mul": "multiply",
    "div": "divide",
}

ERROR_FORMAT = "Invalid input. Use: <operation> <num1> <num2>"


def display_help() -> None:
    print(
        """
Calculator REPL Help
--------------------
Usage:
  <operation> <number1> <number2>

Supported operations:
  add, subtract, multiply, divide

Shortcuts:
  sub -> subtract
  mul -> multiply
  div -> divide

Special commands:
  help      show this message
  history   show calculation history
  exit      quit the program

Examples:
  add 10 5
  sub 15 3
  mul 7 8
  div 20 4
"""
    )


def display_history(history: List[Calculation]) -> None:
    if not history:
        print("No calculations performed yet.\n")
        return

    print("Calculation History:")
    for idx, calc in enumerate(history, start=1):
        print(f"{idx}. {calc}")
    print()


def calculator() -> None:
    history: List[Calculation] = []

    print("Welcome to the Professional Calculator REPL!")
    print("Type 'help' for instructions, 'history' to view past results, or 'exit' to quit.\n")

    while True:
        try:
            user_input = input(">> ").strip()

            # LBYL: quick check before doing any work
            if not user_input:
                continue

            command = user_input.lower()

            # Special commands
            if command == "help":
                display_help()
                continue
            if command == "history":
                display_history(history)
                continue
            if command in ("exit", "quit"):
                print("Goodbye!\n")
                sys.exit(0)

            # EAFP: parse + convert
            try:
                operation, num1_str, num2_str = user_input.split()
                operation = SHORTCUTS.get(operation.lower(), operation.lower())
                num1 = float(num1_str)
                num2 = float(num2_str)
            except ValueError:
                print(f"{ERROR_FORMAT}\n")
                continue

            # Create calculation via factory
            try:
                calc = CalculationFactory.create_calculation(operation, num1, num2)
            except ValueError as ve:
                print(f"{ve}\n")
                continue

            # Execute + print + store
            try:
                print(f"Result: {calc}\n")
                history.append(calc)
            except ValueError as e:
                print(f"{e}\n")
                continue

            except Exception as e:
                print(f"Error during calculation: {e}\n")
                continue

        except KeyboardInterrupt:
            print("\nKeyboard interrupt detected. Goodbye!\n")
            sys.exit(0)
        except EOFError:
            print("\nEOF detected. Goodbye!\n")
            sys.exit(0)