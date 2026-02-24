# Module 4: Assignment - Professional Calculator Command-Line Application with 100% Test Coverage

## Overview

This is a command-line calculator written in Python that uses object-oriented programming principles, the Factory design pattern, input validation, and comprehensive error handling.  
It supports addition, subtraction, multiplication, and division using a REPL (Read–Eval–Print Loop) interface.

The project includes automated unit and parameterized tests using pytest, 100% test coverage enforcement using pytest-cov, and continuous integration using GitHub Actions.

Module 4 expands upon Module 3 by introducing a CalculationFactory, decorator based registration of calculation types, history tracking, and more robust error handling.

---

## Features

- Add, subtract, multiply, divide  
- REPL command-line interface  
- Shortcut commands (sub, mul, div)  
- Help command for user guidance  
- History command to display previous calculations  
- Input validation for incorrect formats and non-numeric values  
- Error handling (invalid input, divide by zero, unsupported    operations)  
- LBYL and EAFP error handling strategies  
- Graceful handling of KeyboardInterrupt and EOFError  
- Automated unit and parameterized tests with pytest  
- Continuous integration with GitHub Actions enforcing 100% test coverage  

---

## Setup Instructions

Clone the repository:

```bash
git clone https://github.com/brythecodeguy/Module-4-Assignment.git
cd Module-4-Assignment
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
