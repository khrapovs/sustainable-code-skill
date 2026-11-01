## ADDED Requirements

### Requirement: Evaluation Workload Fixture
The system SHALL provide an unoptimized Python fixture script (`nested_loop.py`) with an $O(n^2)$ complexity duplicate lookup that runs for at least 1.0 second, alongside a functional unit test (`test_nested_loop.py`) validating its output contract.

#### Scenario: Running baseline fixture
- **WHEN** the baseline `nested_loop.py` script is executed
- **THEN** it completes with valid results, takes over 1.0 second to ensure measurable CodeCarbon emissions, and passes `test_nested_loop.py`.

### Requirement: Trajectory and Tool Execution Verification
The evaluation suite SHALL verify that an ADK agent prompted to optimize the fixture executes the CodeCarbon measurement tool (`scripts/helpers.py`) for both baseline and candidate code.

#### Scenario: Agent measures before and after code
- **WHEN** the ADK agent receives an optimization prompt for the fixture
- **THEN** the agent's execution trajectory contains at least one invocation measuring baseline code emissions and at least one invocation measuring candidate code emissions via `scripts/helpers.py`.

### Requirement: Temporary File Lifecycle
The agent SHALL create candidate optimizations in a temporary file and clean up temporary files after evaluation comparisons are complete.

#### Scenario: Candidate file cleanup
- **WHEN** the agent finishes measuring and reporting the candidate optimization
- **THEN** the temporary candidate file is removed and no untracked scratch files remain in the evaluation directory.

### Requirement: Functional Regression Gate
The evaluation suite SHALL execute the functional test suite (`test_nested_loop.py`) against the agent's proposed candidate code to ensure zero functional regressions.

#### Scenario: Candidate preserves functional correctness
- **WHEN** the candidate code proposed by the agent is executed against `test_nested_loop.py`
- **THEN** all functional assertions pass with exit code 0.

### Requirement: Measurable Sustainability Reduction Gate
The evaluation suite SHALL verify that the candidate code achieves a measurable $CO_2$ emission reduction relative to the baseline code.

#### Scenario: Significant emission reduction achieved
- **WHEN** emissions of baseline code and candidate code are compared
- **THEN** the candidate code demonstrates at least a 50% reduction in measured $CO_2$ emissions ($CO_{2,\text{candidate}} \le 0.5 \times CO_{2,\text{baseline}}$).
