# AGENTS Instructions

## Commands

- Run a single test: `uv run pytest tests/path/to/test.py::TestClass::test_method -xvs`.
- Run all tests in package: `uv run pytest -xvs`.
- Run pre-commit hooks on all files before finishing off with a change:
  `uv run prek run -v --show-diff-on-failure --all-files`.
- Run Python scripts with `uv run path/to/script.py`.

## Coding Standards

- Each change in `.py` files should be formatted and linted with `ruff`, and type checked with `ty`. These checks can be
  done in one command using pre-commit hooks (`prek`).
- No `assert` in production code.
- Comment sparingly — code says what, comments say why. Add a comment only when the reasoning is non-obvious and cannot
  be carried by a clear name or the code itself. Do not write narrating comments that restate the next line, do not pad
  logic with multi-line prose, and do not repeat the same rationale at several sites — put one concise note at the
  source of truth and let the others stand on their own. Tests whose names already describe intent need no explanatory
  comment. Reserve longer explanation for genuinely complex or non-obvious logic, and keep even that as tight as it can
  be. Over-commenting is noise that ages badly and obscures the code it wraps.
- Name functions and methods with action verbs: `get_`, `extract_`, `find_`, `compute_`, `build_`, etc. Avoid noun-only
  names like `_serialize_keys` or `_base_names` — they read as attributes, not callables. Predicates (`is_`, `has_`) are
  the one exception.

## Testing Standards

- Target exactly 100% coverage of what the PR changes — no more, no less. Every changed or added behavior must have a
  test; every test must fail without the PR's change.
- Do not add tests for pre-existing logic that was already present before the PR, and do not test standard-library or
  third-party functions. The exception is deliberate behavior or integration tests, which may cross those boundaries by
  design.
- Use `pytest` patterns, not `unittest.TestCase`.
- Use `@pytest.mark.parametrize` for multiple similar inputs — consolidate tests that only differ in input/expected
  values into a single parametrized test.
- Unit tests are not allowed to access private attribute/methods of classes.

## Scope Discipline

- Do not commit anything. Only add to the staging area. Committing is the responsibility of the user.
- Only read files I explicitly name or point to.
- Do not read additional files to "get context," "understand the project," or "see how things connect" unless I ask you
  to.
- If you think reading more files would help, ask first. One sentence: "Want me to also read X?" Wait for my answer.
- This applies to every task in this project. No exceptions for "just checking" or "quick look."
- Each class should expose only those methods and attributes that are used in the other classes/functions. All other
  attributes and methods should be private (_method). Example:

    ```python
    class A:
        def __init__(self):
            self._x = 1 # should be private
            self.y = 2 # should be public

        def _private_method(self):
            pass # should be private

        def public_method(self):
            pass # should be public
    ```
