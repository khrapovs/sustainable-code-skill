import json
import subprocess
import sys
import tempfile
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

from google.adk import Agent
from google.adk.skills import load_skill_from_dir


class TrajectoryTracker:
    def __init__(self) -> None:
        self._tool_calls: list[dict[str, object]] = []

    def record_call(self, tool_name: str, *, arguments: dict[str, object], result: object) -> None:
        self._tool_calls.append({"tool": tool_name, "args": arguments, "result": result})

    def get_tool_calls(self) -> list[dict[str, object]]:
        return list(self._tool_calls)

    def has_measured_files(self, baseline_name: str, *, candidate_name: str) -> bool:
        called_measure_baseline = False
        called_measure_candidate = False

        for call in self._tool_calls:
            args_str = json.dumps(call["args"])
            if baseline_name in args_str:
                called_measure_baseline = True
            if candidate_name in args_str:
                called_measure_candidate = True

        return called_measure_baseline and called_measure_candidate


class CandidateLifecycleManager:
    @staticmethod
    @contextmanager
    def create_candidate_file(code_content: str) -> Generator[Path, None, None]:
        temp_file = tempfile.NamedTemporaryFile(mode="w", suffix="_candidate.py", delete=False)
        candidate_path = Path(temp_file.name)
        try:
            temp_file.write(code_content)
            temp_file.flush()
            temp_file.close()
            yield candidate_path
        finally:
            if candidate_path.exists():
                candidate_path.unlink()


class EvaluationGates:
    @staticmethod
    def verify_functional_correctness(candidate_path: Path, *, test_file_path: Path) -> bool:
        # Run test suite dynamically against candidate implementation
        run_code = f"""
import sys
from pathlib import Path
import pytest

candidate_dir = str(Path('{candidate_path}').parent)
if candidate_dir not in sys.path:
    sys.path.insert(0, candidate_dir)

import importlib.util
spec = importlib.util.spec_from_file_location("nested_loop", "{candidate_path}")
module = importlib.util.module_from_spec(spec)
sys.modules["nested_loop"] = module
sys.modules["tests.evals.fixtures.nested_loop"] = module
spec.loader.exec_module(module)

exit_code = pytest.main(["{test_file_path}", "-xvs"])
sys.exit(exit_code)
"""
        result = subprocess.run([sys.executable, "-c", run_code], capture_output=True, text=True, check=False)
        return result.returncode == 0

    @staticmethod
    def compute_sustainability_reduction(original: dict[str, float], *, optimized: dict[str, float]) -> float:
        orig_kg = original.get("emissions_kg", 0.0)
        opt_kg = optimized.get("emissions_kg", 0.0)
        if orig_kg > 0:
            return round((orig_kg - opt_kg) / orig_kg * 100, 2)

        orig_dur = original.get("duration_s", 0.0)
        opt_dur = optimized.get("duration_s", 0.0)
        if orig_dur > 0:
            return round((orig_dur - opt_dur) / orig_dur * 100, 2)

        return 0.0

    @classmethod
    def verify_sustainability_reduction(
        cls, original: dict[str, float], *, optimized: dict[str, float], min_reduction_pct: float = 50.0
    ) -> bool:
        reduction_pct = cls.compute_sustainability_reduction(original, optimized=optimized)
        return reduction_pct >= min_reduction_pct


def build_sustainable_agent(tracker: TrajectoryTracker, *, skill_dir: Path) -> Agent:
    skill = load_skill_from_dir(str(skill_dir))

    def measure_code_file(file_path: str) -> dict[str, object]:
        """Measure the carbon and energy emissions of a Python file using helpers.py."""
        helpers_path = skill_dir / "scripts" / "helpers.py"
        cmd = [sys.executable, str(helpers_path), "measure", file_path, "--json"]
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        out = proc.stdout
        marker = '{\n  "emissions_kg":'
        idx = out.find(marker)
        data = json.loads(out[idx:]) if idx != -1 else {}
        tracker.record_call("measure_code_file", arguments={"file_path": file_path}, result=data)
        return data

    def compare_code_files(*, before_file: str, after_file: str) -> dict[str, object]:
        """Compare the carbon and energy emissions of two Python files using helpers.py."""
        helpers_path = skill_dir / "scripts" / "helpers.py"
        cmd = [sys.executable, str(helpers_path), "compare", before_file, after_file, "--json"]
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        out = proc.stdout
        marker = '{\n  "original":'
        idx = out.find(marker)
        data = json.loads(out[idx:]) if idx != -1 else {}
        tracker.record_call(
            "compare_code_files", arguments={"before_file": before_file, "after_file": after_file}, result=data
        )
        return data

    return Agent(
        name="sustainable_code_optimizer",
        description=skill.frontmatter.description if skill.frontmatter else "Optimizes code for CO2",
        instruction=skill.instructions,
        tools=[measure_code_file, compare_code_files],
    )
