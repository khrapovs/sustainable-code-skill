from pathlib import Path

import pytest
from tests.evals.eval_harness import (
    CandidateLifecycleManager,
    EvaluationGates,
    TrajectoryTracker,
    build_sustainable_agent,
)

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
SKILL_DIR = Path(__file__).resolve().parents[2] / "skills" / "sustainable-code"

OPTIMIZED_CODE = """
def find_common_elements(first: list[int], second: list[int]) -> list[int]:
    common: list[int] = []
    set_second = set(second)
    for a in first:
        if a in set_second and a not in common:
            common.append(a)
    return common

def run_benchmark() -> list[int]:
    first = list(range(25000))
    second = list(range(12500, 37500))
    return find_common_elements(first, second)

if __name__ == '__main__':
    result = run_benchmark()
"""

BUGGY_CODE = """
def find_common_elements(first: list[int], second: list[int]) -> list[int]:
    return []

def run_benchmark() -> list[int]:
    return []
"""


def test_build_sustainable_agent() -> None:
    tracker = TrajectoryTracker()
    agent = build_sustainable_agent(tracker, skill_dir=SKILL_DIR)
    assert agent.name == "sustainable_code_optimizer"
    assert len(agent.tools) == 2
    assert isinstance(agent.instruction, str)
    assert "Sustainable Code" in agent.instruction


def test_trajectory_tracker() -> None:
    tracker = TrajectoryTracker()
    tracker.record_call("measure_code_file", arguments={"file_path": "baseline.py"}, result={"duration_s": 1.0})
    assert tracker.has_measured_files("baseline.py", candidate_name="candidate.py") is False

    tracker.record_call("measure_code_file", arguments={"file_path": "candidate.py"}, result={"duration_s": 0.1})
    assert tracker.has_measured_files("baseline.py", candidate_name="candidate.py") is True
    assert len(tracker.get_tool_calls()) == 2


def test_candidate_lifecycle_cleanup() -> None:
    candidate_path_holder: list[Path] = []
    with CandidateLifecycleManager.create_candidate_file("x = 1") as candidate_path:
        candidate_path_holder.append(candidate_path)
        assert candidate_path.exists()

    assert not candidate_path_holder[0].exists()


def test_functional_correctness_gate() -> None:
    test_path = FIXTURES_DIR / "test_nested_loop.py"

    with CandidateLifecycleManager.create_candidate_file(OPTIMIZED_CODE) as candidate_path:
        is_valid = EvaluationGates.verify_functional_correctness(candidate_path, test_file_path=test_path)
        assert is_valid is True

    with CandidateLifecycleManager.create_candidate_file(BUGGY_CODE) as candidate_path:
        is_invalid = EvaluationGates.verify_functional_correctness(candidate_path, test_file_path=test_path)
        assert is_invalid is False


@pytest.mark.parametrize(
    ("original", "optimized", "expected_passed"),
    [
        ({"duration_s": 2.0, "emissions_kg": 0.0}, {"duration_s": 0.1, "emissions_kg": 0.0}, True),
        ({"duration_s": 2.0, "emissions_kg": 0.002}, {"duration_s": 1.5, "emissions_kg": 0.0005}, True),
        ({"duration_s": 2.0, "emissions_kg": 0.0}, {"duration_s": 1.8, "emissions_kg": 0.0}, False),
        ({"duration_s": 0.0, "emissions_kg": 0.0}, {"duration_s": 0.0, "emissions_kg": 0.0}, False),
    ],
)
def test_sustainability_reduction_gate(
    *, original: dict[str, float], optimized: dict[str, float], expected_passed: bool
) -> None:
    passed = EvaluationGates.verify_sustainability_reduction(
        original=original, optimized=optimized, min_reduction_pct=50.0
    )
    assert passed is expected_passed


def test_single_eval_full_flow() -> None:
    tracker = TrajectoryTracker()
    agent = build_sustainable_agent(tracker, skill_dir=SKILL_DIR)
    baseline_path = FIXTURES_DIR / "nested_loop.py"
    test_path = FIXTURES_DIR / "test_nested_loop.py"

    # 1. Execute baseline measurement via agent tool
    measure_tool = agent.tools[0]
    compare_tool = agent.tools[1]
    assert callable(measure_tool)
    assert callable(compare_tool)
    baseline_metrics = measure_tool(file_path=str(baseline_path))
    assert isinstance(baseline_metrics, dict)
    assert "duration_s" in baseline_metrics

    # 2. Agent generates candidate in temporary file
    with CandidateLifecycleManager.create_candidate_file(OPTIMIZED_CODE) as candidate_path:
        # 3. Candidate measurement and comparison via agent tool
        comparison = compare_tool(before_file=str(baseline_path), after_file=str(candidate_path))
        assert isinstance(comparison, dict)
        assert "original" in comparison
        assert "optimized" in comparison

        # 4. Trajectory Gate
        assert tracker.has_measured_files(str(baseline_path), candidate_name=str(candidate_path)) is True

        # 5. Functional Gate
        assert EvaluationGates.verify_functional_correctness(candidate_path, test_file_path=test_path) is True

        # 6. Sustainability Gate
        assert isinstance(comparison["original"], dict)
        assert isinstance(comparison["optimized"], dict)
        sustainability_passed = EvaluationGates.verify_sustainability_reduction(
            comparison["original"], optimized=comparison["optimized"], min_reduction_pct=50.0
        )
        assert sustainability_passed is True

    # 7. Verification that candidate file was cleaned up
    assert not candidate_path.exists()
