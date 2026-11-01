## Context

The `sustainable-code` skill instructs agents on diagnosing and optimizing Python code for reduced carbon footprint using CodeCarbon via `scripts/helpers.py`. To automate quality assurance, we need an evaluation skeleton that tests both agent behavior (tool-use trajectory) and empirical software performance (functional correctness and verified $CO_2$ reduction).

## Goals / Non-Goals

**Goals:**
- Provide a reproducible, deterministic workload fixture (`nested_loop.py`) taking ~1.0–2.0 seconds to run, giving CodeCarbon sufficient sample duration above hardware noise.
- Provide a functional unit test (`test_nested_loop.py`) establishing the input/output contract of the fixture.
- Implement an evaluation runner in `tests/evals/test_sustainable_eval.py` runnable via `uv run pytest tests/evals/`.
- Validate trajectory (verifying `scripts/helpers.py` is invoked before and after).
- Enforce clean temporary file lifecycle for generated candidate scripts.
- Enforce automated gates: 100% test pass on candidate code, and $\ge 50\%$ $CO_2$ reduction.

**Non-Goals:**
- Testing cloud or GPU-specific emissions.
- Building a full matrix of dozens of test cases (this change focuses strictly on the single test skeleton).
- Modifying production skill behavior or `scripts/helpers.py` implementation.

## Decisions

- **Decision 1: Use synthetic nested loop duplicate lookup for initial fixture**
  - *Rationale:* Completely dependency-free (standard library only), deterministic execution duration, and easily optimized from $O(n^2)$ nested iteration to $O(n)$ hash set lookup ($>80\%$ emission reduction).
  - *Alternatives considered:* Pandas/NumPy dataframe vectorization (rejected for initial skeleton due to heavier dependencies and cold-start import overhead).

- **Decision 2: Integrate ADK eval as a standard `pytest` suite**
  - *Rationale:* Integrates directly into existing developer workflows (`uv run pytest tests/evals/`) and CI/CD pipelines without requiring a standalone separate eval server.
  - *Alternatives considered:* ADK CLI declarative runner (`agents-cli eval`) standalone. Wrapping in `pytest` gives greater flexibility to run custom post-run functional checks and assertions on artifacts.

- **Decision 3: Isolated temporary file strategy for candidate code**
  - *Rationale:* Prompting the agent to write candidate code to a temporary path (or using Python `tempfile`) keeps the evaluation directory clean and prevents git workspace pollution during automated runs.

## Risks / Trade-offs

- **[Risk] CodeCarbon hardware emission noise on fast execution** → *Mitigation:* Calibrate `nested_loop.py` dataset size to ensure runtime is at least 1.0–1.5 seconds.
- **[Risk] LLM non-determinism during optimization** → *Mitigation:* The prompt explicitly requests optimizing for $CO_2$ and following the `sustainable-code` skill workflow. The three-gate assertion verifies output quality regardless of subtle formatting differences.
- **[Risk] Temporary file left behind if agent fails mid-run** → *Mitigation:* Pytest fixture uses `try...finally` to ensure all temporary candidate files are purged even on failure.
