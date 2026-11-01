#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "codecarbon>=2.4.1",
# ]
# requires-python = ">=3.8"
# ///
"""
Sustainable Code Helper — Measure and optimize Python code for CO2 emissions.

This tool uses CodeCarbon to measure code emissions, compare alternatives,
and suggest greener implementations.

Run with uv (recommended):
    uv run scripts/helpers.py measure <file.py>
    uv run scripts/helpers.py compare <before.py> <after.py>
    uv run scripts/helpers.py --help

Usage as library:
    from sustainable_code_helper import CodeMetrics
    metrics = CodeMetrics.measure_code(code_string)
    print(metrics.to_dict())
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

from codecarbon import EmissionsTracker


class CodeMetrics:
    """Wrapper around CodeCarbon for measuring code emissions."""

    def __init__(self, *, emissions_kg: float, energy_kwh: float, duration_s: float) -> None:
        """Initialize metrics from CodeCarbon output.

        Args:
            emissions_kg: CO2 emissions in kg CO2eq
            energy_kwh: Energy consumed in kWh
            duration_s: Execution duration in seconds
        """
        self.emissions_kg = emissions_kg
        self.energy_kwh = energy_kwh
        self.duration_s = duration_s

    @property
    def emissions_g(self) -> float:
        """Emissions in grams."""
        return self.emissions_kg * 1000

    @property
    def emissions_rate_g_per_s(self) -> float:
        """Emissions rate in g CO2/second."""
        if self.duration_s == 0:
            return 0
        return self.emissions_g / self.duration_s

    def to_dict(self) -> dict[str, float]:
        """Convert metrics to dictionary."""
        return {
            "emissions_kg": round(self.emissions_kg, 6),
            "emissions_g": round(self.emissions_g, 4),
            "energy_kwh": round(self.energy_kwh, 8),
            "duration_s": round(self.duration_s, 2),
            "emissions_rate_g_per_s": round(self.emissions_rate_g_per_s, 4),
        }

    def to_string(self) -> str:
        """Format metrics as readable string."""
        return (
            f"CO₂: {self.emissions_kg:.6f} kg CO₂eq\n"
            f"Energy: {self.energy_kwh:.8f} kWh\n"
            f"Duration: {self.duration_s:.2f} seconds\n"
            f"Rate: {self.emissions_rate_g_per_s:.4f} g CO₂/s"
        )

    def compare(self, other: CodeMetrics) -> dict[str, Any]:
        """Compare with another CodeMetrics object.

        Args:
            other: Another CodeMetrics instance

        Returns
        -------
            Dictionary with comparison results (reduction %, etc.)
        """
        reduction_kg = self.emissions_kg - other.emissions_kg
        reduction_pct = (reduction_kg / self.emissions_kg * 100) if self.emissions_kg > 0 else 0

        return {
            "baseline_kg": round(self.emissions_kg, 6),
            "optimized_kg": round(other.emissions_kg, 6),
            "reduction_kg": round(reduction_kg, 6),
            "reduction_pct": round(reduction_pct, 2),
            "direction": "reduction" if reduction_kg > 0 else "increase",
        }


class SustainableCodeAnalyzer:
    """Main analyzer for measuring and comparing code implementations."""

    @staticmethod
    def measure_code(code: str, *, project_name: str = "sustainable-code", setup_code: str = "") -> CodeMetrics:
        """Measure emissions of a code snippet.

        Args:
            code: Python code as string (the main code to measure)
            project_name: Name for tracking (default: sustainable-code)
            setup_code: Optional setup code (imports, initialization) that runs but isn't tracked

        Returns
        -------
            CodeMetrics object with measurements
        """
        # Create a temporary file with the code
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            if setup_code:
                f.write(setup_code + "\n")
            f.write(code)
            temp_file = f.name

        try:
            tracker = EmissionsTracker(project_name=project_name)
            tracker.start()

            # Execute the code
            namespace = {}
            if setup_code:
                exec(setup_code, namespace)
            exec(code, namespace)

            emissions = tracker.stop()

            # Get detailed emissions data
            final_data = tracker.final_emissions_data
            return CodeMetrics(
                emissions_kg=emissions,
                energy_kwh=final_data.energy_consumed,
                duration_s=final_data.duration,
            )
        finally:
            os.unlink(temp_file)

    @staticmethod
    def compare_implementations(
        *,
        original: str,
        optimized: str,
        setup_code: str = "",
        project_name: str = "sustainable-code",
    ) -> dict[str, Any]:
        """Compare emissions between two code implementations.

        Args:
            original: Original code as string
            optimized: Optimized code as string
            setup_code: Optional setup code (imports, data) run before both
            project_name: Name for tracking

        Returns
        -------
            Dictionary with comparison results
        """
        original_metrics = SustainableCodeAnalyzer.measure_code(
            original, project_name=f"{project_name}-original", setup_code=setup_code
        )
        optimized_metrics = SustainableCodeAnalyzer.measure_code(
            optimized, project_name=f"{project_name}-optimized", setup_code=setup_code
        )

        comparison = original_metrics.compare(optimized_metrics)

        return {
            "original": original_metrics.to_dict(),
            "optimized": optimized_metrics.to_dict(),
            "comparison": comparison,
        }


def cli_measure(args: argparse.Namespace) -> None:
    """CLI: Measure emissions from a file."""
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"ERROR: File not found: {file_path}")
        sys.exit(1)

    code = file_path.read_text()
    print(f"Measuring {file_path}...\n")

    metrics = SustainableCodeAnalyzer.measure_code(code, project_name=file_path.stem)
    print("Results:")
    print(metrics.to_string())

    if args.json:
        print("\nJSON:")
        print(json.dumps(metrics.to_dict(), indent=2))


def cli_compare(args: argparse.Namespace) -> None:
    """CLI: Compare two implementations."""
    before_path = Path(args.before)
    after_path = Path(args.after)

    if not before_path.exists():
        print(f"ERROR: File not found: {before_path}")
        sys.exit(1)
    if not after_path.exists():
        print(f"ERROR: File not found: {after_path}")
        sys.exit(1)

    before_code = before_path.read_text()
    after_code = after_path.read_text()

    print(f"Comparing {before_path} vs {after_path}...\n")

    result = SustainableCodeAnalyzer.compare_implementations(before_code, after_code, project_name=before_path.stem)

    print("Original Code:")
    print("  CO₂: {:.6f} kg CO₂eq".format(result["original"]["emissions_kg"]))
    print("  Energy: {:.8f} kWh".format(result["original"]["energy_kwh"]))
    print("  Duration: {:.2f} seconds".format(result["original"]["duration_s"]))

    print("\nOptimized Code:")
    print("  CO₂: {:.6f} kg CO₂eq".format(result["optimized"]["emissions_kg"]))
    print("  Energy: {:.8f} kWh".format(result["optimized"]["energy_kwh"]))
    print("  Duration: {:.2f} seconds".format(result["optimized"]["duration_s"]))

    comp = result["comparison"]
    reduction_pct = comp["reduction_pct"]
    print("\nComparison:")
    print(f"  Reduction: {reduction_pct:.2f}%")
    print(f"  CO₂ saved: {comp['reduction_kg']:.6f} kg CO₂eq")

    if args.json:
        print("\nJSON:")
        print(json.dumps(result, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Measure and optimize Python code for CO2 emissions.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Measure a single file (with uv):
    uv run scripts/helpers.py measure my_code.py

  Compare two implementations (with uv):
    uv run scripts/helpers.py compare before.py after.py

  Get JSON output (with uv):
    uv run scripts/helpers.py measure my_code.py --json

  Without installing (with uvx):
    uvx --python 3.8+ --with codecarbon python scripts/helpers.py measure my_code.py
    uvx --python 3.8+ --with codecarbon python scripts/helpers.py compare before.py after.py
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Measure command
    measure_parser = subparsers.add_parser("measure", help="Measure emissions of a Python file")
    measure_parser.add_argument("file", help="Python file to measure")
    measure_parser.add_argument("--json", action="store_true", help="Output as JSON")
    measure_parser.set_defaults(func=cli_measure)

    # Compare command
    compare_parser = subparsers.add_parser("compare", help="Compare two Python implementations")
    compare_parser.add_argument("before", help="Original Python file")
    compare_parser.add_argument("after", help="Optimized Python file")
    compare_parser.add_argument("--json", action="store_true", help="Output as JSON")
    compare_parser.set_defaults(func=cli_compare)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    args.func(args)


if __name__ == "__main__":
    main()
