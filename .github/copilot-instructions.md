# GitHub Copilot Instructions for CLI Tools Repository

This document provides context and guidelines for GitHub Copilot agents working on this repository.

## Project Overview

This is a collection of command-line utilities for developers. Each tool is self-contained with its own documentation, dependencies, and tests.

## Repository Structure

```
cli-tools/
├── .github/
│   ├── workflows/          # GitHub Actions workflows
│   └── copilot-instructions.md
├── tools/                  # CLI tools collection
│   └── {toolname}/        # Each tool in its own directory
│       ├── {toolname}.py  # Main tool script
│       ├── requirements.txt # Tool-specific dependencies
│       └── README.md      # Tool documentation
├── tests/                 # Test suite
│   ├── conftest.py       # pytest configuration and fixtures
│   └── test_*.py         # Test files
├── scripts/              # Installation and utility scripts
│   └── install.sh        # Installation script
├── requirements-dev.txt  # Development dependencies
└── README.md            # Main repository documentation
```

## Coding Standards

### Python Style
- Follow PEP 8 style guide
- Use type hints for function signatures
- Follow PEP 257 docstring conventions
- Use single quotes for strings unless double quotes are needed
- Format code with `black` (line length: 88)
- Lint with `flake8`
- Type check with `mypy`

### Error Handling
- Use specific exception types (e.g., `ValueError`, `FileNotFoundError`) instead of broad `Exception` catching
- Log errors to stderr using appropriate logging levels
- Provide helpful error messages that guide users to resolution

### Testing
- Write tests using `pytest`
- Test files follow naming convention: `test_*.py`
- Place tests in the `tests/` directory
- Include both unit tests and integration tests where appropriate
- Aim for good code coverage (use `pytest-cov`)

## Development Workflow

### Setting Up Development Environment
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install tool-specific dependencies
pip install -r tools/{toolname}/requirements.txt
```

### Running Tests
```bash
# Run all tests with coverage
pytest tests/ -v --cov=tools --cov-report=term

# Run specific test file
pytest tests/test_cleanshare.py -v
```

### Code Quality Checks
```bash
# Format code
black tools/ tests/

# Lint code
flake8 tools/ tests/

# Type check
mypy tools/
```

## Tool Development Guidelines

### Creating a New Tool
1. Create a new directory under `tools/` with the tool name
2. Create the main script as `{toolname}.py`
3. Add a `requirements.txt` file for dependencies
4. Write a comprehensive `README.md` with:
   - Tool description and purpose
   - Installation instructions
   - Usage examples
   - Command-line options
5. Add tests in `tests/test_{toolname}.py`

### Tool Structure Pattern
Each tool should:
- Be executable as a standalone script
- Use argparse for command-line arguments
- Include proper error handling and validation
- Have clear, helpful output messages
- Be installable via symlink to `/usr/local/bin/`

### Installation Pattern
Tools are installed as symlinks:
```bash
ln -s $(pwd)/tools/{toolname}/{toolname}.py /usr/local/bin/{toolname}
```

## Dependencies

### Core Development Tools
- `pytest>=7.4.0` - Testing framework
- `pytest-cov>=4.1.0` - Coverage reporting
- `black>=23.0.0` - Code formatting
- `flake8>=6.0.0` - Linting
- `mypy>=1.4.0` - Type checking
- `coverage>=7.2.0` - Coverage analysis

### Adding New Dependencies
- Add tool-specific dependencies to `tools/{toolname}/requirements.txt`
- Add development dependencies to `requirements-dev.txt`
- Keep dependencies minimal and well-justified
- Pin major versions for stability

## CI/CD

### GitHub Actions
- Tests run automatically on push to `main` and on pull requests
- Test workflow uses Python 3.11
- Coverage reports are generated for all test runs
- Workflow file: `.github/workflows/test.yml`

## Best Practices for Issues and PRs

### Good Task Types for Copilot
- Bug fixes in existing tools
- Adding new command-line tools
- Improving test coverage
- Updating documentation
- Refactoring for code quality
- Adding new features to existing tools

### Writing Clear Issues
- Provide specific, actionable requirements
- Include acceptance criteria
- Reference affected files or components
- Include example inputs/outputs when relevant

### Code Review Expectations
- All tests must pass
- Code must be formatted with `black`
- No linting errors from `flake8`
- Type hints required for new functions
- Documentation updated for user-facing changes

## Common Patterns

### Argument Parsing
```python
import argparse

def main():
    parser = argparse.ArgumentParser(description="Tool description")
    parser.add_argument("input", help="Input description")
    parser.add_argument("--option", help="Optional parameter")
    args = parser.parse_args()
```

### Error Handling
```python
import sys

try:
    # operation
    pass
except ValueError as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
```

### Testing Pattern
```python
import pytest
from tools.toolname.toolname import main_function

def test_function_success():
    result = main_function("input")
    assert result == expected

def test_function_error():
    with pytest.raises(ValueError):
        main_function("invalid")
```

## Security Considerations
- Validate all user inputs
- Use appropriate sanitization for file paths and shell commands
- Avoid exposing sensitive information in error messages
- Be cautious with file system operations

## Additional Resources
- [Python Style Guide (PEP 8)](https://www.python.org/dev/peps/pep-0008/)
- [Docstring Conventions (PEP 257)](https://www.python.org/dev/peps/pep-0257/)
- [pytest Documentation](https://docs.pytest.org/)
- [Black Code Formatter](https://black.readthedocs.io/)

## Questions or Clarifications
If you encounter ambiguity or need clarification on requirements, ask for guidance rather than making assumptions that could lead to incorrect implementations.
