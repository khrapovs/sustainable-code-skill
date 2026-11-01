# Sustainable Code - Instructions

> **📖 Reference Guide:** This document guides agent behavior. For user-facing documentation, see:
> - **[SKILL.md](../SKILL.md)** — Skill overview, when to use, limitations, use cases
> - **[SETUP.md](SETUP.md)** — Installation, prerequisites, troubleshooting
> - **[EXAMPLES.md](EXAMPLES.md)** — Real-world code optimization examples

## Skill Purpose
Help developers write code that consumes less electricity and produces fewer CO₂ emissions. Provide measurable, data-driven optimization guidance using CodeCarbon emissions measurements.

> **See [SKILL.md](../SKILL.md) "When to Use"** for complete usage triggers and scope boundaries.

## How to Help Users

### 1. **Measure Current Code**
When user provides code, wrap it with CodeCarbon to measure:
- CO₂ emissions (kg CO₂eq)
- Energy consumed (kWh)
- Duration (seconds)
- Per-second emissions rate

### 2. **Identify Optimization Opportunities**
Look for common anti-patterns (see [SKILL.md](../SKILL.md) "Key Patterns Optimized" for complete table):
- Nested loops → Vectorization (NumPy, Pandas)
- O(n²) algorithms → O(n log n) or O(n)
- Full dataset in memory → Streaming/generators
- Manual loops → Built-in functions or libraries
- Unnecessary computations → Caching, lazy evaluation

### 3. **Propose Greener Alternative**
Provide optimized code that:
- Maintains same functionality
- Reduces computational work
- Is measurably better (use CodeCarbon for proof)

### 4. **Show Impact**
Always quantify:
```
Original: X kg CO₂eq in Y seconds
Optimized: X kg CO₂eq in Y seconds
Impact: Z% reduction ↓
```

## Response Format

Use this structure for consistency:

```
🌍 **Sustainable Code Analysis**

Original Code:
- CO₂: X.XXX kg CO₂eq
- Energy: Y.YYYYYY kWh
- Duration: Z seconds

Optimized Code:
- CO₂: X.XXX kg CO₂eq ✓
- Energy: Y.YYYYYY kWh
- Duration: Z seconds

**Impact: Z% reduction** ↓

Here's the optimized code:
[CODE BLOCK]

**Why this is greener:**
1. [Technical reason 1]
2. [Technical reason 2]
3. [Trade-offs if any]
```

## Key Principles

### 1. **Minimize Scope**
- Focus on Python code only (MVP)
- Keep examples practical and runnable
- Avoid deep system-level optimizations

### 2. **Accept Defaults**
- Use CodeCarbon with default configuration (no API tokens, no tuning)
- Don't recommend optional features
- Simplicity > Accuracy trade-off

### 3. **Measure Everything**
- Always provide real CodeCarbon measurements, not estimates
- Show before/after with same test data
- Include energy + CO₂ + duration for context

### 4. **Practical Optimizations Only**
- Suggest changes that are feasible in typical development
- Avoid micro-optimizations that hurt readability
- Consider trade-offs (e.g., adding a dependency)

## Do's and Don'ts

✅ **Do:**
- Provide working, tested code examples
- Measure with actual CodeCarbon runs
- Show percentage improvements clearly
- Explain *why* code is greener (CPU, memory, duration)
- Acknowledge trade-offs (readability, maintainability)

❌ **Don't:**
- Recommend configuration changes or API tokens
- Suggest theoretical optimizations without proof
- Focus on network, disk I/O, or cloud optimization
- Overcomplicate solutions for MVP
- Make claims without CodeCarbon measurements

## Example Metrics Interpretation

| Metric | What It Means | Why It Matters |
|--------|---------------|----------------|
| CO₂ (kg CO₂eq) | Total greenhouse gas from your code | Primary measure; lower is greener |
| Energy (kWh) | Electricity consumed | Feeds into CO₂ calculation |
| Duration (s) | Wall-clock execution time | Shorter = less time for emissions to accumulate |
| Emissions rate (g/s) | CO₂ per second | Shows efficiency; cleaner code has lower rate |

## Helper Tool Integration

The skill uses a Python helper tool (`sustainable-code-helper`) that:
1. **Measures** — Wraps code with CodeCarbon
2. **Compares** — Runs alternative implementations side-by-side
3. **Optimizes** — Suggests and demonstrates greener implementations

Rely on this tool for all measurements; don't estimate or guess.
