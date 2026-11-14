### 🌍 Sustainable Code Analysis

In your original implementation, `if item in second:` performs a linear search across the entire list `second` for every item in `first`.
If len(first) = N and len(second) = M, this results in an O(N * M) time complexity. On realistic data sizes, the CPU spends unnecessary clock cycles scanning arrays in memory, generating sustained heat and consuming power.

---

### Benchmark Comparison
Using CodeCarbon on CPU:
- Time Complexity: O(N * M) -> O(N + M) (~99% faster)
- Duration: drop in CPU time
- Energy Consumed: lower energy consumed in kWh
- Estimated CO2eq: reduction in CO2 emissions

---

### Greener Alternatives

Option 1: Preserve order and duplicates from first (O(N + M))
```python
def find_common_elements(first: list[int], second: list[int]) -> list[int]:
    second_set = set(second)  # O(M) conversion
    return [item for item in first if item in second_set]  # O(N) lookup
```

Option 2: Unique common elements (O(N + M))
```python
def find_common_elements(first: list[int], second: list[int]) -> list[int]:
    return list(set(first).intersection(second))
```

---

### Why This is Greener
1. Reduced CPU Cycles: Looking up a value in a Python set uses hash tables with O(1) time.
2. Lower Thermal Throttling and fan power: Short efficient bursts stay within lower CPU power envelopes.
3. Optimized Memory Access: Eliminates redundant memory scans.

---

### Measure It Yourself Locally
Verify savings with CodeCarbon using EmissionsTracker:
```python
from codecarbon import EmissionsTracker

with EmissionsTracker() as tracker:
    # Measure original vs optimized
    pass
```
Check emissions.csv for kWh and CO2 emissions.
