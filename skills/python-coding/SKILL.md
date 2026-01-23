---
name: python-coding
description: Use this skill when writing, editing, or reviewing Python code or scripts, including refactors, bug fixes, formatting, or adding type hints; enforce PEP 8/PEP 257 conventions and common Python best practices.
---

# Python Coding Guidelines

## Code Style

Follow [PEP 8](https://peps.python.org/pep-0008/) standards for all Python code:

- **Indentation**: Use 4 spaces per indentation level
- **Line length**: Maximum 79 characters for code, 72 for docstrings/comments
- **Imports**: Group in order: standard library, third-party, local; one import per line
- **Import Statements**: All import statements should be placed at the top of the file, not inside functions, unless absolutely necessary (e.g., circular import issues)
- **Whitespace**: No trailing whitespace; blank lines to separate functions/classes
- **Naming conventions**:
  - `snake_case` for functions, variables, and modules
  - `PascalCase` for classes
  - `UPPER_SNAKE_CASE` for constants

## Documentation

- Use English for all docstrings
- Follow [PEP 257](https://peps.python.org/pep-0257/) for docstring conventions
- Use triple double quotes `"""` for docstrings

## Type Hints

- Use type hints for function signatures when appropriate
- Follow [PEP 484](https://peps.python.org/pep-0484/) conventions

## Comments

- Write all comments in English
- Use comments sparingly; prefer self-documenting code
