# AGENTS.md

This file provides guidelines for AI agents working in this repository.

## Project Overview

This is an AI agent patterns repository demonstrating various agent architectures including Plan-and-Solve, ReAct, and Reflection patterns. The project uses Python 3.14+ with litellm for LLM integration and includes implementations from the "Hello Agents" book.

**Key Directories:**
- `datawhale/` - Main agent implementations (ReAct, Plan-and-Solve, Reflection)
- `examples/` - Demo scripts for various agent frameworks
- `patterns/` - Pattern implementations
- `src/ulib/` - Utility library
- `bin/` - Command-line tools

## Build, Lint, and Test Commands

### Installation
```bash
pip install -e .
```

### Development Dependencies
```bash
pip install -e ".[dev]"
```

### Linting
```bash
ruff check .                    # Run linter on all files
ruff check --fix .              # Auto-fix linting issues
ruff check <file>               # Lint specific file
```

### Formatting
```bash
ruff format .                   # Format all files
ruff format <file>              # Format specific file
```

### Testing
```bash
pytest                          # Run all tests
pytest <file>                   # Run specific test file
pytest -v                       # Run with verbose output
pytest -k "test_name"           # Run tests matching pattern
pytest --collect-only           # List all tests without running
```

**Note:** This project currently doesn't have a test suite. When adding tests, follow these patterns:
- Create `tests/` directory at project root
- Test files should be named `test_*.py` or `*_test.py`
- Use pytest fixtures and assertions

### Building
```bash
pip install build
python -m build                 # Build wheel and tarball
```

**VERY IMPORTANT:** When you have completed a task, you MUST run the lint and typecheck commands (e.g., `ruff check .`, `ruff format .`) to ensure your code is correct. If you are unable to find the correct command, ask the user for the command to run and if they supply it, proactively suggest writing it to AGENTS.md so that you will know to run it next time.

## Code Style Guidelines

### General Principles
- Write self-documenting code with descriptive names
- Keep functions focused and modular
- Use docstrings for complex functions and classes
- Follow existing patterns in agent implementations

## Code Style Guidelines

### General Principles
- Write self-documenting code with descriptive names
- Keep functions focused and modular
- Use docstrings for complex functions and classes
- Follow existing patterns in agent implementations

### Imports
Organize imports in three sections separated by blank lines:
1. Standard library imports
2. Third-party imports
3. Local application imports

```python
import os
import re
from collections.abc import Callable
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

from ulib.utils.env_reader import read_deepseek_api_key
```

### Formatting
- **Line length**: Maximum 120 characters
- **Quotes**: Use double quotes (`"`) for all strings
- **Indentation**: 4 spaces (PEP 8)
- **Line breaks**: Use trailing commas for multi-line structures

### Type Hints
Use modern Python 3.14+ union syntax:
```python
def __init__(
    self,
    model: str | None = None,
    apiKey: str | None = None,
):
    ...
```

Avoid `Optional[]` - use `| None` instead.

### Naming Conventions
- **Classes**: PascalCase (e.g., `HelloAgentsLLM`, `ReActAgent`)
- **Functions/methods**: snake_case (e.g., `get_tool`, `think`)
- **Variables**: snake_case (e.g., `response_text`, `llm_client`)
- **Constants**: SCREAMING_SNAKE_CASE (e.g., `PLANNER_PROMPT_TEMPLATE`)
- **Private methods**: Leading underscore (e.g., `_parse_output`)

### Error Handling
- Use specific exception types when possible
- Return `None` or error messages for recoverable errors
- Print user-friendly error messages with emojis
- Handle `None` returns from functions with `or` defaults

```python
try:
    response = self.client.chat.completions.create(...)
except Exception as e:
    print(f"❌ 调用LLM API时发生错误: {e}")
    return None

if not all([self.model, apiKey, baseUrl]):
    raise ValueError("模型ID、API密钥和服务地址必须被提供或在.env文件中定义。")
```

### Class Structure
Follow this pattern for classes:
```python
class ClassName:
    """Docstring describing the class."""

    def __init__(self, param: str | None = None):
        """Initialize the class."""
        self.param = param

    def public_method(self) -> ReturnType:
        """Public method description."""
        ...

    def _private_method(self) -> ReturnType:
        """Private method description."""
        ...
```

### File Structure
- Put `if __name__ == "__main__":` at the bottom of files
- Include usage examples in main blocks
- Load environment variables at module level with error handling

### Comments
- Avoid comments that state the obvious
- Use Chinese comments when documenting Chinese-specific behavior
- Prefer descriptive naming over comments for simple logic

### Agent Implementation Patterns
See actual implementations in `datawhale/` directory:
- `ReAct.py`: ReAct pattern with tool execution loop
- `Plan_and_solve.py`: Plan-and-Solve pattern with planner/executor
- `Reflection.py`: Reflection pattern with self-critique

## Ruff Configuration
- `fix = true`: Auto-resolve issues
- `unsafe-fixes = true`: Allow aggressive auto-correction
- Selects: E4, E7, E9, F, B, A, I, UP rules
- `line-length = 120`: Maximum line length
- `quote-style = "double"`: Use double quotes for all strings
