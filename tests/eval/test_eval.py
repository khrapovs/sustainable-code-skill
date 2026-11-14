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
from google.adk.evaluation.eval_case import EvalCase, Invocation
from google.adk.evaluation.eval_config import EvalConfig
from google.adk.evaluation.eval_set import EvalSet
from google.genai import types as genai_types

_AGENT_MODULE = "tests.eval.agent"
_CURRENT_DIR = Path(__file__).parent
_PROJECT_ROOT = _CURRENT_DIR.parent.parent
_CASE_DIR = _CURRENT_DIR / "cases" / "nested_loop_optimization"
_OUTPUT_FILE_PATH = _PROJECT_ROOT / "artifacts" / "eval_results.csv"


def build_eval_set() -> EvalSet:
    """Build an EvalSet from markdown files."""
    prompt_text = (_CASE_DIR / "prompt.md").read_text(encoding="utf-8")
    expected_text = (_CASE_DIR / "expected_response.md").read_text(encoding="utf-8")

    return EvalSet(
        eval_set_id="sustainable_code_eval",
        eval_cases=[
            EvalCase(
                eval_id="nested_loop_optimization",
                conversation=[
                    Invocation(
                        user_content=genai_types.Content(role="user", parts=[genai_types.Part(text=prompt_text)]),
                        final_response=genai_types.Content(role="model", parts=[genai_types.Part(text=expected_text)]),
                    )
                ],
            )
        ],
    )


def test_eval_set_loads_and_is_non_empty() -> None:
    """EvalSet dataset is valid and contains exactly one eval case."""
    eval_set = build_eval_set()

    assert eval_set.eval_set_id == "sustainable_code_eval"
    assert len(eval_set.eval_cases) == 1
    assert eval_set.eval_cases[0].eval_id == "nested_loop_optimization"
    assert eval_set.eval_cases[0].conversation is not None
    assert len(eval_set.eval_cases[0].conversation) == 1
    assert eval_set.eval_cases[0].conversation[0].final_response is not None


@pytest.mark.asyncio
async def test_nested_loop_optimization_response_quality() -> None:
    """Agent correctly identifies the inefficiency and suggests a greener alternative."""
    eval_set = build_eval_set()
    eval_config = EvalConfig(criteria={"tool_trajectory_avg_score": 1.0, "response_match_score": 0.5})

    await AgentEvaluator.evaluate_eval_set(
        agent_module=_AGENT_MODULE,
        eval_set=eval_set,
        eval_config=eval_config,
        num_runs=1,
        output_file=str(_OUTPUT_FILE_PATH),
        print_detailed_results=False,
    )
