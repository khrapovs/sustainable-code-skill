---
name: sustainable-code
description: 'Measure and optimize Python code to reduce CO₂ emissions. Use when: writing computationally intensive code, refactoring for efficiency, or comparing algorithm choices. Provides real emissions measurements and actionable optimizations.'
compatibility: Requires Python 3.8+, CodeCarbon>=2.4.1, and Linux/macOS/Windows 11+ for hardware metrics
metadata:
  version: "0.1.0"
  tags: sustainability, optimization, carbon, green-tech, python
  scope: experimental
---

## Overview

The **Sustainable Code** skill helps developers write Python code that consumes less electricity and produces fewer CO₂ emissions. Using the CodeCarbon library, it measures the carbon footprint of code and recommends greener alternatives with quantified impact.

This skill bridges software engineering and environmental responsibility by making code sustainability measurable and actionable.

## When to Use

✅ **Perfect for:**
- Optimizing computationally intensive Python functions
- Comparing performance vs. sustainability trade-offs
- Refactoring algorithms with carbon footprint in mind
- Understanding which code patterns are "greener"
- Benchmarking before/after implementations

**Example requests:**
- "How can I make this data processing more sustainable?"
- "Compare the carbon footprint: loops vs NumPy vectorization"
- "Is this algorithm worth optimizing for emissions?"
- "Which is greener: streaming file processing or loading all at once?"
- "How much CO₂ would I save by vectorizing this code?"

❌ **Out of scope:**
- Cloud/infrastructure sustainability (use cloud provider tools)
- GenAI API emissions (use EcoLogits instead)
- Configuration tuning or advanced features
- Non-Python languages (Python only, MVP)
- Production monitoring (one-time analysis only)

## Capabilities

1. **Measure emissions** — Real CodeCarbon measurements (kg CO₂eq, kWh, duration)
2. **Identify optimizations** — Common patterns: loops→vectorization, O(n²)→O(n), memory efficiency
3. **Compare alternatives** — Before/after measurements with % impact
4. **Suggest implementations** — Working, tested code examples with explanations

## Output Example

```
🌍 Sustainable Code Analysis

Original Code (nested loop):
- CO₂: 0.0156 kg CO₂eq
- Energy: 0.00045 kWh
- Duration: 12.5 seconds

Optimized Code (set-based):
- CO₂: 0.0002 kg CO₂eq ✓
- Energy: 0.000006 kWh
- Duration: 0.2 seconds

Impact: 99% CO₂ reduction ↓

Why this is greener:
1. Set operations are O(1) vs O(n²) nested loops
2. Fewer iterations = less CPU time
3. Reduced CPU time = lower power consumption
```

## Key Patterns Optimized

| Pattern | Issue | Optimization | Typical Savings |
|---------|-------|--------------|-----------------|
| Nested loops | O(n²) complexity | Vectorization, sets, hashing | 80-99% |
| Full file load | High RAM usage | Streaming, generators | 70-90% |
| Manual iteration | CPU overhead | Built-ins, comprehensions, libraries | 50-80% |
| Algorithm choice | Wrong complexity class | Better algorithm selection | 60-95% |
| Redundant calls | Duplicate work | Caching, memoization | 40-75% |

## Limitations

⚠️ **Know the constraints:**

- **Python-only** — MVP focuses on Python; other languages need CLI wrapper
- **Hardware-dependent** — Results vary by CPU, GPU, RAM availability
- **Short-running code** — CodeCarbon overhead may dominate for sub-second scripts
- **Grid averages** — Uses country-level defaults (not real-time carbon intensity)
- **Local compute only** — Doesn't measure cloud/remote execution
- **Single-threaded** — Unpredictable results for parallel/async code

## How It Works

1. **You provide code** — Share Python snippet or file path
2. **Skill measures with CodeCarbon** — Tracks CPU/GPU/RAM power consumption
3. **Grid carbon intensity applied** — Converts power to CO₂ using your region's grid
4. **Optimization suggested** — Skill identifies greener alternative
5. **Comparison shown** — Before/after metrics with % reduction

**Example workflow:**

```
User: "Optimize this for CO₂: for i in data: result.append(i*2)"
↓
Skill: Measures original code with CodeCarbon → 0.042 kg CO₂eq
↓
Skill: Suggests NumPy vectorization → np.array(data) * 2
↓
Skill: Measures optimized code → 0.008 kg CO₂eq
↓
User: "81% reduction! 🌍 I'll use this."
```

## Getting Started

### Prerequisites & Installation

See [references/SETUP.md](references/SETUP.md) for complete setup instructions, including:
- Python 3.8+ installation
- uv setup
- CodeCarbon dependency installation
- Troubleshooting hardware metric issues

### First Use
Ask the skill to measure or optimize your code:

```
"Can you measure the emissions of this function and suggest a greener approach?
[paste your Python code]"
```

The skill will:
1. ✅ Run your code with CodeCarbon
2. ✅ Show emissions (CO₂, energy, duration)
3. ✅ Identify inefficiencies
4. ✅ Suggest optimized version
5. ✅ Measure optimized version
6. ✅ Show impact (% reduction)

## Helper Tool

The skill includes a standalone Python utility: `scripts/helpers.py` for measuring and comparing code emissions.

**Quick examples:**
- Measure a file: `uv run scripts/helpers.py measure my_code.py`
- Compare two versions: `uv run scripts/helpers.py compare before.py after.py`

See [references/SETUP.md](references/SETUP.md) for full usage guide, output formats, and programmatic API.

## Common Use Cases

### 1. Loop Vectorization
**Problem:** Iterating over arrays with Python loops
**Solution:** Use NumPy or built-in vectorized operations
**Savings:** 80%+

### 2. Algorithm Optimization
**Problem:** O(n²) nested loops or wrong data structures
**Solution:** Better algorithm or data structure choice
**Savings:** 60-99%

### 3. Memory Efficiency
**Problem:** Loading entire files into memory
**Solution:** Streaming with generators
**Savings:** 70-90%

### 4. Redundant Computation
**Problem:** Recalculating same values repeatedly
**Solution:** Caching or memoization
**Savings:** 40-75%

## Related Skills & Tools

- **EcoLogits** — For GenAI API call emissions (complementary tool)
- **Code Reviewer** — For general code quality (separate skill)
- **CodeCarbon** — The underlying library doing measurements (open-source)

## Resources

- **CodeCarbon Documentation** — https://docs.codecarbon.io/
- **Emissions Calculation Methodology** — https://docs.codecarbon.io/latest/explanation/methodology/
- **CodeCarbon GitHub** — https://github.com/mlco2/codecarbon
- **Setup Guide** — See [references/SETUP.md](references/SETUP.md) for installation and usage
- **Real-world Examples** — See [references/EXAMPLES.md](references/EXAMPLES.md) for common use cases
- **Behavior Guide** — See [references/INSTRUCTIONS.md](references/INSTRUCTIONS.md) for how the skill works
