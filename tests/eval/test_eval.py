"""Pytest integration tests that run agent evaluation with the ADK SDK.

These tests invoke the sustainable-code skill via a real LLM call and grade
the agent's response using AgentEvaluator. They require a valid
GOOGLE_API_KEY or Application Default Credentials (ADC) environment to run.

Run with:
    uv run pytest tests/eval/test_eval.py -xvs
"""

from pathlib import Path

import pytest
from google.adk.evaluation import AgentEvaluator
from google.adk.evaluation.eval_set import EvalSet


_AGENT_MODULE = "tests.eval.agent"
_EVAL_SET_FILE = "tests/eval/datasets/nested_loop_optimization.test.json"


def test_eval_set_loads_and_is_non_empty() -> None:
    """EvalSet dataset is valid and contains exactly one eval case."""
    eval_set = EvalSet.model_validate_json(Path(_EVAL_SET_FILE).read_text())

    assert eval_set.eval_set_id == "sustainable_code_eval"
    assert len(eval_set.eval_cases) == 1
    assert eval_set.eval_cases[0].eval_id == "nested_loop_optimization"
    assert eval_set.eval_cases[0].conversation is not None
    assert len(eval_set.eval_cases[0].conversation) == 1


@pytest.mark.asyncio
async def test_nested_loop_optimization_response_quality() -> None:
    """Agent correctly identifies the inefficiency and suggests a greener alternative."""
    await AgentEvaluator.evaluate(
        agent_module=_AGENT_MODULE,
        eval_dataset_file_path_or_dir=_EVAL_SET_FILE,
        num_runs=1,
        print_detailed_results=True,
    )
