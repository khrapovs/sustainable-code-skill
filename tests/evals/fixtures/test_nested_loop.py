import pytest
from tests.evals.fixtures.nested_loop import find_common_elements, run_benchmark


@pytest.mark.parametrize(
    ("first", "second", "expected"),
    [
        ([], [], []),
        ([1, 2, 3], [4, 5, 6], []),
        ([1, 2, 3], [2, 3, 4], [2, 3]),
        ([1, 1, 2], [1, 2, 2], [1, 2]),
    ],
)
def test_find_common_elements(*, first: list[int], second: list[int], expected: list[int]) -> None:
    assert find_common_elements(first=first, second=second) == expected


def test_run_benchmark() -> None:
    result = run_benchmark()
    assert len(result) == 12500
    assert result[0] == 12500
    assert result[-1] == 24999
