"""Fixture script demonstrating an unoptimized O(n^2) search."""


def find_common_elements(*, first: list[int], second: list[int]) -> list[int]:
    """Find common elements between two lists using nested loops."""
    common: list[int] = []
    for a in first:
        for b in second:
            if a == b and a not in common:
                common.append(a)
    return common


def run_benchmark() -> list[int]:
    """Execute the workload with inputs calibrated to run for ~3.5s."""
    first = list(range(25000))
    second = list(range(12500, 37500))
    return find_common_elements(first=first, second=second)


if __name__ == "__main__":
    result = run_benchmark()
    print(f"Found {len(result)} common elements.")
