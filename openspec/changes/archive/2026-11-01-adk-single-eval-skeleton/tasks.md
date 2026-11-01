## 1. Test Fixtures Setup

- [x] 1.1 Create `tests/evals/fixtures/nested_loop.py` with an unoptimized O(n²) duplicate search running >= 1.0s
- [x] 1.2 Create `tests/evals/fixtures/test_nested_loop.py` to assert functional correctness of the duplicate search

## 2. Evaluation Harness Implementation

- [x] 2.1 Implement ADK agent wrapper loading `skills/sustainable-code/SKILL.md` and configuring execution tools
- [x] 2.2 Implement trajectory verification ensuring `scripts/helpers.py` is executed for baseline and candidate code
- [x] 2.3 Implement temporary candidate file lifecycle and cleanup management
- [x] 2.4 Implement functional regression gate asserting candidate code passes `test_nested_loop.py`
- [x] 2.5 Implement sustainability gate asserting >= 50% measured CO₂ emission reduction
- [x] 2.6 Assemble test runner in `tests/evals/test_sustainable_eval.py`

## 3. Verification & Pre-commit Quality Checks

- [x] 3.1 Run `uv run pytest tests/evals/fixtures/test_nested_loop.py -xvs` to verify baseline fixture tests
- [x] 3.2 Run `uv run pytest tests/evals/test_sustainable_eval.py -xvs` to verify the single eval skeleton
- [x] 3.3 Run `uv run prek run -v --show-diff-on-failure --all-files` to format, lint, and type check all files
