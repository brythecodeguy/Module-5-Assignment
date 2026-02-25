# Module 5: Assignment - Enhanced Professional Calculator Application with Advanced Design Patterns and pandas

## Overview

This project is an advanced, modular calculator application built in Python.
It demonstrates object-oriented programming principles, multiple design patterns, persistent data management using pandas, configuration management via environment variables, and full automated testing with enforced 100% test coverage.

Module 5 significantly expands upon Module 4 by introducing:

- Strategy Pattern for interchangeable arithmetic operations
- Factory Pattern for dynamic operation instantiation
- Observer Pattern for logging and auto-saving history
- Memento Pattern for undo/redo functionality
- Facade Pattern through the Calculator interface
- Persistent history storage using pandas and CSV files
- Environment-based configuration using python-dotenv

All functionality is verified through comprehensive pytest test suites with CI enforcement.

---

## Features

- Add, subtract, multiply, divide, power, root
- REPL command-line interface
- Help command for user guidance
- History command to display previous calculations
- Clear command to reset history
- Undo and redo functionality using the Memento pattern
- Save and load history to/from CSV files
- Persistent history storage using pandas
- Input validation for incorrect formats and non-numeric values
- Custom exception handling (invalid input, divide by zero, unsupported operations, history errors)
- LBYL and EAFP error handling strategies
- Good handling of KeyboardInterrupt and EOFError
- Automated unit and parameterized tests with pytest
- Continuous integration with GitHub Actions enforcing 100% test coverage

---

## Setup Instructions

Clone the repository:

```bash
git clone https://github.com/brythecodeguy/Module-5-Assignment.git
cd Module-5-Assignment
```

Create and activate a virtual environment, then install the required dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Run Calculator

```bash
python main.py
```

---

## Run Tests

```bash
pytest --cov=app --cov-report=term-missing
coverage report --fail-under=100
```

---

## Continuous Integration

All tests must pass with full coverage. Tests automatically run on every push using GitHub Actions.
If coverage drops below 100%, the build fails.
