# Setup & Installation

## Prerequisites

This skill requires:
- **Python 3.8+**
- **uv** (recommended) or `uvx` for running scripts with automatic dependency resolution
- **CodeCarbon** (auto-installed via `uv run`)

**System Requirements for Hardware Metrics:**
- **Linux**: RAPL (Intel/AMD) or TDP fallback
- **macOS**: Native power API
- **Windows 11**: Energy Meter Interface (EMI)

## Quick Start with uv

[uv](https://docs.astral.sh/uv/) automatically handles dependencies declared in the script. No separate installation step needed.

```bash
# Measure a file's emissions
uv run scripts/helpers.py measure my_code.py

# Compare two implementations
uv run scripts/helpers.py compare before.py after.py
```

If you don't have `uv` installed:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Using the Helper Tool

The skill includes a Python helper tool: `scripts/helpers.py`

Run it with `uv run`. Dependencies are automatically installed.

### Measure a single file's emissions:

```bash
uv run scripts/helpers.py measure my_code.py
```

Output:
```
Measuring my_code.py...

Results:
CO₂: 0.000123 kg CO₂eq
Energy: 0.000004 kWh
Duration: 0.45 seconds
Rate: 0.2733 g CO₂/s
```

### Compare two implementations:

```bash
uv run scripts/helpers.py compare before.py after.py
```

Output:
```
Comparing before.py vs after.py...

Original Code:
  CO₂: 0.000156 kg CO₂eq
  Energy: 0.000005 kWh
  Duration: 1.25 seconds

Optimized Code:
  CO₂: 0.000031 kg CO₂eq
  Energy: 0.000001 kWh
  Duration: 0.25 seconds

Comparison:
  Reduction: 80.13%
  CO₂ saved: 0.000125 kg CO₂eq
```

### Get JSON output for automation:

```bash
uv run scripts/helpers.py measure my_code.py --json
```

## Using as a Python Library

You can also use the helper tool programmatically in your own code:

```python
from sustainable_code_helper import CodeMetrics

# Measure a code snippet
code = """
for i in range(1000000):
    x = i * 2
"""

metrics = CodeMetrics.measure_code(code, project_name="my-test")
print(metrics.to_dict())

# Compare two implementations
result = CodeMetrics.compare_implementations(
    original=original_code,
    optimized=optimized_code
)
print(result["comparison"]["reduction_pct"], "% reduction")
```

## Troubleshooting

### "uv: command not found"

Install uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Measurements seem too small or zero

- Make sure your code runs for at least 1+ seconds
- CodeCarbon measures local CPU/GPU/RAM; short scripts may be below measurement threshold

### "Unable to read hardware metrics"

- On Linux: Ensure RAPL is available (`ls /sys/class/powercap/intel-rapl/`)
- On Windows: Windows 11+ with Energy Meter Interface is required
- Fallback: CodeCarbon estimates from CPU/RAM specs if hardware counters unavailable

### Extremely high or low numbers

- Results vary by hardware, grid carbon intensity, and system load
- Run multiple times for consistency
- Use `--no-api` mode for stable defaults (already default in MVP)

## Resources

- **CodeCarbon GitHub**: https://github.com/mlco2/codecarbon
- **CodeCarbon Docs**: https://docs.codecarbon.io/
- **Installation Guide**: https://docs.codecarbon.io/latest/how-to/installation/
- **Methodology**: https://docs.codecarbon.io/latest/explanation/methodology/
- **uv Documentation**: https://docs.astral.sh/uv/
