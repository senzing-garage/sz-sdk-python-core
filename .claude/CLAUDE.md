# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is `sz-sdk-python-core`, a Python SDK that wraps the Senzing C libraries for entity resolution. It implements the abstract interfaces defined in the `senzing` package (`sz-sdk-python`) using ctypes to call the native Senzing C binaries.

The SDK provides five main components:
- **SzConfig** - Configuration management for the Senzing engine
- **SzConfigManager** - Manages configuration storage and retrieval
- **SzDiagnostic** - Diagnostics and repository maintenance
- **SzEngine** - Core entity resolution operations (add/delete records, search, entity analysis)
- **SzProduct** - Product version and license information

## Prerequisites

The Senzing C library must be installed before using this SDK:
- Linux: `/opt/senzing/er/lib` (set `LD_LIBRARY_PATH`)
- macOS: `$SENZING_PATH/er`
- Requires Senzing version >= 4.0.0 and < 5.0.0

## Common Commands

### Setup
```bash
make dependencies-for-development  # Install all dev dependencies
make dependencies                  # Install runtime dependencies only
make setup                         # Set up test database (copies SQLite to /tmp/sqlite)
```

### Testing
```bash
make clean setup test              # Full test run (unit tests + examples)
pytest tests/                      # Run unit tests only
pytest tests/szengine_test.py     # Run single test file
pytest tests/szengine_test.py::test_add_record -v  # Run single test
make coverage                      # Run tests with coverage report
```

### Linting
```bash
make lint                          # Run all linters (pylint, mypy, bandit, black, flake8, isort)
make black                         # Format code
make pylint                        # Run pylint
make mypy                          # Run type checking
make isort                         # Sort imports
```

### Building
```bash
make package                       # Build wheel distribution
make publish-test                  # Publish to test PyPI
```

## Architecture

### Source Structure
All SDK code is in `src/senzing_core/`:
- `szabstractfactory.py` - Factory pattern entry point (recommended usage)
- `szengine.py`, `szconfig.py`, etc. - Individual SDK component implementations
- `_helpers.py` - Shared utilities for C library interaction

### C Library Binding Pattern

Each SDK class follows this pattern:
1. Load the Senzing shared library via `load_sz_library()` in `_helpers.py`
2. Define C function signatures using ctypes (argtypes/restype)
3. Create ctypes Structure classes for complex return types (e.g., `SzResponseReturnCodeResult`)
4. Use `FreeCResources` context manager to properly free C memory
5. Use `check_result_rc()` to convert C error codes to Python exceptions

### Factory Pattern Usage

The recommended way to use the SDK:
```python
from senzing_core import SzAbstractFactoryCore

sz_factory = SzAbstractFactoryCore(instance_name, settings)
sz_engine = sz_factory.create_engine()
# Use sz_engine...
sz_factory.destroy()  # Clean up all created objects
```

The factory manages initialization/destruction of all Senzing components and prevents conflicting configurations.

### Settings Dictionary Structure
```python
settings = {
    "PIPELINE": {
        "CONFIGPATH": "/etc/opt/senzing",
        "RESOURCEPATH": "/opt/senzing/er/resources",
        "SUPPORTPATH": "/opt/senzing/data",
    },
    "SQL": {"CONNECTION": "sqlite3://na:na@/tmp/sqlite/G2C.db"},
}
```

## Code Style

- Line length: 120 characters
- Uses black for formatting, isort with "black" profile
- Type hints required (mypy strict)
- Pylint disabled rules include: `line-too-long`, `too-many-arguments`, `duplicate-code`
- B101 (assert usage) skipped in bandit for test assertions

## Testing Notes

- Tests require the Senzing library and a test database (created by `make setup`)
- Test fixtures are in `tests/conftest.py` (provides `engine_vars` with platform-specific settings)
- Uses `senzing_truthset` package for test data
- Examples in `examples/` are also run as tests via pytest
