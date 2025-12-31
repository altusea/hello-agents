# Agents

This directory contains various AI agent implementations and examples.

## Overview

This project demonstrates different agent patterns and architectures for AI systems, including reasoning strategies and tool usage patterns.

## Components

### DataWhale Agents

Located in the `datawhale/` directory, containing core agent implementations:

- **Plan_and_solve.py**: Implements the Plan-and-Solve reasoning pattern
- **ReAct.py**: Implements the ReAct (Reasoning and Acting) pattern
- **Reflection.py**: Implements self-reflection capabilities
- **llm_client.py**: LLM client utilities for agent communication
- **tools.py**: Tool definitions and utilities for agent operations

### Examples

Located in the `examples/` directory, containing demonstration scripts:

- **litellm_test.py**: Example usage of LiteLLM integration
- **smolagent_demo.py**: Small-scale agent demonstration

### Utilities

Located in the `src/ulib/utils/` directory:

- **env_reader.py**: Environment variable reading utilities
- **__init__.py**: Package initialization

## Getting Started

1. Install dependencies: `pip install -e .`
2. Explore the agent implementations in the `datawhale/` directory
3. Run examples in the `examples/` directory
4. Check out the utility functions in `src/ulib/utils/`

## Agent Patterns

This project implements several key agent reasoning patterns:

- **Plan-and-Solve**: Two-stage reasoning with planning followed by execution
- **ReAct**: Alternating between reasoning and acting
- **Reflection**: Self-evaluation and improvement capabilities

Each pattern demonstrates different approaches to AI agent reasoning and decision-making.

## Code Style Guidelines

This project follows specific coding standards to maintain consistency and readability across all agent implementations.

### Code Formatting Rules

- **Line Length**: Maximum 120 characters per line
- **Quote Style**: Use double quotes (`"`) for all strings
- **Indentation**: Use consistent indentation (follow PEP 8 standards)
- **File Extensions**: Python files should use `.py` extension

### Linting Standards

### Code Quality Tools

- **Auto-formatting**: Ruff is configured with `fix = true` to automatically resolve issues
- **Unsafe fixes**: Enabled with `unsafe-fixes = true` for aggressive auto-correction
- **File coverage**: Applies to `pyproject.toml`, `src/**/*.py`, `bin/**/*.py`, `examples/**/*.py`, and `datawhale/**/*.py`

### Development Workflow

1. Run linting: `ruff check .`
2. Auto-fix issues: `ruff check --fix .`
3. Format code: `ruff format .`
4. Verify changes: `ruff check .` (after formatting)

### Best Practices

- Write self-documenting code with descriptive variable and function names
- Include type hints where appropriate
- Keep functions focused and modular
- Use docstrings for complex functions and classes
- Follow the existing patterns in agent implementations
