# Sustainable Code Helper

This directory contains the Sustainable Code helper module and its unit tests.

## Files

- **`helpers.py`** - Main module with `CodeMetrics` and `SustainableCodeAnalyzer` classes
- **`test_helpers.py`** - Pytest unit tests for the helpers module

## Running Tests with uv

### Prerequisites

Ensure you have `uv` installed. If not, install it from https://docs.astral.sh/uv/.

### Initial Setup

On first use, sync the dependencies:

```bash
uv sync
```

This creates a `.venv` directory and installs pytest and codecarbon.

### Run All Tests

From this directory, run:

```bash
uv run pytest test_helpers.py -v
```

> **Note:** The `emissions.csv` file created by CodeCarbon during testing is automatically cleaned up after the test session completes.

### Run Specific Test Class

```bash
uv run pytest test_helpers.py::TestCodeMetrics -v
```

Or:

```bash
uv run pytest test_helpers.py::TestSustainableCodeAnalyzer -v
```

## Test Coverage

The test suite includes:

- **CodeMetrics class tests**: Initialization, unit conversions, rate calculations, dictionary/string formatting, and comparisons
- **SustainableCodeAnalyzer class tests**: Code measurement with and without setup code, custom project names, and implementation comparisons

## Using as a Library

Import the helpers in your Python scripts:

```python
from helpers import CodeMetrics, SustainableCodeAnalyzer

# Measure code emissions
metrics = SustainableCodeAnalyzer.measure_code("x = 1 + 1")
print(metrics.to_string())

# Compare two implementations
result = SustainableCodeAnalyzer.compare_implementations(
    "result = sum(range(10))",
    "result = 45"
)
print(f"Reduction: {result['comparison']['reduction_pct']}%")
```

## Sample Scripts

Three sample scripts are provided to demonstrate the helpers:

- **`my_code.py`** - General sample code with various operations (loops, comprehensions, string operations)
- **`before.py`** - Unoptimized version with inefficient algorithms (nested loops, string concatenation, redundant checks)
- **`after.py`** - Optimized version of the same logic (list comprehensions, `join()`, `set()` for uniqueness)

## CLI Usage

Measure a file:
```bash
uv run helpers.py measure my_code.py
```

Compare two implementations:
```bash
uv run helpers.py compare before.py after.py
```

Get JSON output:
```bash
uv run helpers.py measure my_code.py --json
```

Compare with JSON output:
```bash
uv run helpers.py compare before.py after.py --json
```

See full help:
```bash
uv run helpers.py --help
```

**Note:** The emissions.csv file created by CodeCarbon during CLI usage will be tracked in the directory. Since it's excluded by .gitignore, it won't be committed to the repository.
