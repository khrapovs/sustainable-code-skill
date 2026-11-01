#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "pytest>=7.0",
#   "codecarbon>=2.4.1",
# ]
# requires-python = ">=3.8"
# ///
"""Unit tests for sustainable code helpers."""

from pathlib import Path

import pytest
from helpers import CodeMetrics, SustainableCodeAnalyzer


@pytest.fixture(scope="session", autouse=True)
def cleanup_emissions_csv() -> None:
    """Clean up emissions.csv file created by CodeCarbon after tests complete."""
    yield
    csv_file = Path("emissions.csv")
    if csv_file.exists():
        csv_file.unlink()
        print(f"\nCleaned up {csv_file.name}")


class TestCodeMetrics:
    """Tests for CodeMetrics class."""

    def test_initialization(self) -> None:
        """Test CodeMetrics initialization with valid values."""
        metrics = CodeMetrics(emissions_kg=0.001, energy_kwh=0.00001, duration_s=5.0)
        assert metrics.emissions_kg == 0.001
        assert metrics.energy_kwh == 0.00001
        assert metrics.duration_s == 5.0

    def test_emissions_g_conversion(self) -> None:
        """Test conversion from kg to grams."""
        metrics = CodeMetrics(emissions_kg=0.001, energy_kwh=0.00001, duration_s=1.0)
        assert metrics.emissions_g == 1.0

    def test_emissions_rate_g_per_s(self) -> None:
        """Test emissions rate calculation."""
        metrics = CodeMetrics(emissions_kg=0.001, energy_kwh=0.00001, duration_s=5.0)
        assert metrics.emissions_rate_g_per_s == pytest.approx(0.2, abs=0.001)

    def test_emissions_rate_with_zero_duration(self) -> None:
        """Test emissions rate returns 0 when duration is 0."""
        metrics = CodeMetrics(emissions_kg=0.001, energy_kwh=0.00001, duration_s=0)
        assert metrics.emissions_rate_g_per_s == 0

    def test_to_dict(self) -> None:
        """Test conversion to dictionary."""
        metrics = CodeMetrics(emissions_kg=0.001, energy_kwh=0.00001, duration_s=5.0)
        result = metrics.to_dict()

        assert isinstance(result, dict)
        assert "emissions_kg" in result
        assert "emissions_g" in result
        assert "energy_kwh" in result
        assert "duration_s" in result
        assert "emissions_rate_g_per_s" in result
        assert result["emissions_kg"] == 0.001
        assert result["emissions_g"] == 1.0

    def test_to_string(self) -> None:
        """Test string formatting."""
        metrics = CodeMetrics(emissions_kg=0.001, energy_kwh=0.00001, duration_s=5.0)
        result = metrics.to_string()

        assert isinstance(result, str)
        assert "CO₂" in result
        assert "0.001000" in result
        assert "kg CO₂eq" in result
        assert "kWh" in result
        assert "seconds" in result

    def test_compare_reduction(self) -> None:
        """Test comparison showing reduction."""
        baseline = CodeMetrics(emissions_kg=0.002, energy_kwh=0.00002, duration_s=10.0)
        optimized = CodeMetrics(emissions_kg=0.001, energy_kwh=0.00001, duration_s=5.0)

        result = baseline.compare(optimized)

        assert result["baseline_kg"] == 0.002
        assert result["optimized_kg"] == 0.001
        assert result["reduction_kg"] == 0.001
        assert result["reduction_pct"] == 50.0
        assert result["direction"] == "reduction"

    def test_compare_increase(self) -> None:
        """Test comparison showing increase."""
        baseline = CodeMetrics(emissions_kg=0.001, energy_kwh=0.00001, duration_s=5.0)
        worse = CodeMetrics(emissions_kg=0.002, energy_kwh=0.00002, duration_s=10.0)

        result = baseline.compare(worse)

        assert result["reduction_kg"] == -0.001
        assert result["direction"] == "increase"

    def test_compare_zero_baseline(self) -> None:
        """Test comparison with zero baseline."""
        baseline = CodeMetrics(emissions_kg=0.0, energy_kwh=0.0, duration_s=0.0)
        other = CodeMetrics(emissions_kg=0.001, energy_kwh=0.00001, duration_s=5.0)

        result = baseline.compare(other)

        assert result["reduction_pct"] == 0


class TestSustainableCodeAnalyzer:
    """Tests for SustainableCodeAnalyzer class."""

    def test_measure_simple_code(self) -> None:
        """Test measuring a simple code snippet."""
        code = "x = 1 + 1"
        metrics = SustainableCodeAnalyzer.measure_code(code)

        assert isinstance(metrics, CodeMetrics)
        assert metrics.emissions_kg >= 0
        assert metrics.energy_kwh >= 0
        assert metrics.duration_s > 0

    def test_measure_code_with_setup(self) -> None:
        """Test measuring code with setup code."""
        setup = "data = [1, 2, 3, 4, 5]"
        code = "result = sum(data)"

        metrics = SustainableCodeAnalyzer.measure_code(code, setup_code=setup)

        assert isinstance(metrics, CodeMetrics)
        assert metrics.emissions_kg >= 0

    def test_measure_code_custom_project_name(self) -> None:
        """Test measuring with custom project name."""
        code = "x = 42"
        metrics = SustainableCodeAnalyzer.measure_code(code, project_name="test-project")

        assert isinstance(metrics, CodeMetrics)

    def test_compare_implementations(self) -> None:
        """Test comparing two implementations."""
        original = "result = sum(range(10))"
        optimized = "result = 45"

        result = SustainableCodeAnalyzer.compare_implementations(original, optimized)

        assert isinstance(result, dict)
        assert "original" in result
        assert "optimized" in result
        assert "comparison" in result
        assert isinstance(result["original"], dict)
        assert isinstance(result["optimized"], dict)
        assert isinstance(result["comparison"], dict)

    def test_compare_with_setup_code(self) -> None:
        """Test comparison with setup code."""
        setup = "data = range(100)"
        original = "result = sum(data)"
        optimized = "result = sum(range(100))"

        result = SustainableCodeAnalyzer.compare_implementations(original, optimized, setup_code=setup)

        assert "original" in result
        assert "optimized" in result
        assert "comparison" in result

    def test_compare_returns_correct_structure(self) -> None:
        """Test comparison result has expected structure."""
        original = "x = 1"
        optimized = "y = 1"

        result = SustainableCodeAnalyzer.compare_implementations(original, optimized)
        comp = result["comparison"]

        assert "baseline_kg" in comp
        assert "optimized_kg" in comp
        assert "reduction_kg" in comp
        assert "reduction_pct" in comp
        assert "direction" in comp


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
