# Sustainable Code Skill

> Measure and optimize Python code to reduce CO₂ emissions — a skill for LLM agents.

[![Version](https://img.shields.io/badge/version-0.3.0-blue)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/python-%3E%3D3.14-blue)](pyproject.toml)
[![License](https://img.shields.io/badge/license-MIT-green)](#license)

## Overview

The **Sustainable Code** skill helps developers write Python code that consumes less electricity and produces fewer CO₂ emissions. Using the [CodeCarbon](https://github.com/mlco2/codecarbon) library, it measures the carbon footprint of code and recommends greener alternatives with quantified impact.

This skill bridges software engineering and environmental responsibility by making code sustainability measurable and actionable.

**Perfect for:**
- Optimizing computationally intensive Python functions
- Comparing performance vs. sustainability trade-offs
- Refactoring algorithms with carbon footprint in mind
- Benchmarking before/after implementations

**Out of scope:**
- Cloud/infrastructure sustainability (use cloud provider tools)
- GenAI API emissions (use [EcoLogits](https://github.com/genai-impact/ecologits) instead)
- Non-Python languages (Python only, MVP)
- Production monitoring (one-time analysis only)

## Requirements

- Python ≥ 3.14
- [uv](https://docs.astral.sh/uv/) package manager
- Linux, macOS, or Windows 11+ (for hardware energy metrics)

## Installation

TBA

### For local development

```bash
# Clone the repository
git clone https://github.com/your-org/sustainable-code-skill.git
cd sustainable-code-skill

# Install dependencies (uv manages the virtualenv automatically)
uv sync
```

### Running tests

```bash
# Run all tests
uv run pytest -xvs
```

### Linting and type checking

```bash
# Format, lint (ruff), and type-check (ty) in one pass
uv run prek run -v --show-diff-on-failure --all-files
```

### Project structure

```
sustainable-code-skill/
├── skills/
│   └── sustainable-code/
│       ├── SKILL.md        # Skill definition and instructions
│       ├── scripts/        # CodeCarbon measurement utilities
│       └── references/     # Supporting documentation
├── tests/                  # pytest test suite
└── pyproject.toml
```
