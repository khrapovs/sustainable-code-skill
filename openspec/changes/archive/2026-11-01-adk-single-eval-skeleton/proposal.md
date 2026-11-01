## Why

The sustainable-code skill optimizes Python code for lower CO₂ emissions using CodeCarbon, but currently lacks an automated evaluation framework to verify that CodeCarbon is actually invoked and that refactored code yields genuine emission reductions without breaking functional behavior. We need a single Google ADK-based evaluation test as a repeatable skeleton to anchor automated testing for this skill.

## What Changes

- Introduce a single evaluation fixture (`tests/evals/fixtures/nested_loop.py`) featuring an O(n²) loop search with measurable execution duration (~1.5s).
- Add a companion functional unit test (`tests/evals/fixtures/test_nested_loop.py`) verifying functional correctness of the fixture.
- Implement an ADK-based evaluation test (`tests/evals/test_sustainable_eval.py`) that loads the sustainable-code skill, provides an execution environment, prompts the agent to optimize the fixture, and enforces three evaluation gates:
  - **Trajectory gate**: Verifies that CodeCarbon was executed (via `scripts/helpers.py`) for both baseline and candidate code.
  - **Functional gate**: Verifies that the candidate code passes the original functional unit test.
  - **Sustainability gate**: Verifies that the candidate code achieves a measurable CO₂ reduction ($\ge 50\%$).
- Ensure the candidate code lifecycle handles creating a temporary file and cleaning it up after measurement.

## Capabilities

### New Capabilities
- `skill-evaluation`: Defines requirements and evaluation gates for automated testing of the sustainable-code skill using Google ADK and CodeCarbon.

### Modified Capabilities
<!-- None: no existing specs exist in openspec/specs/ -->

## Impact

- **New files**: `tests/evals/fixtures/nested_loop.py`, `tests/evals/fixtures/test_nested_loop.py`, `tests/evals/test_sustainable_eval.py`.
- **Dependencies**: Uses `google-adk`, `codecarbon`, and `pytest`.
- **APIs & Production Code**: No breaking changes to existing production code or skill instructions.
