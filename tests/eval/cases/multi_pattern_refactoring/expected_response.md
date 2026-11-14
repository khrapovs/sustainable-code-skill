### 🌍 Sustainable Code Analysis

Here is the sustainable refactoring of your code, optimizing multiple computational and memory bottlenecks to reduce CPU cycles, power consumption, and carbon emissions.

---

### Inefficiencies Identified

1. **Manual Loop Appends vs List Comprehensions:** `for num in numbers: squared_list.append(...)` causes dynamic list resizing and Python bytecode overhead compared to list comprehensions.
2. **Redundant Membership Checks:** `if val in squared_list:` is redundant because `val` was just drawn from `squared_list`.
3. **Repeated String Concatenation ($O(N^2)$):** `text = text + " " + word` creates new string allocations on each iteration. Using `" ".join(words)` executes in $O(N)$ with single memory allocation.
4. **Nested Loop for Deduplication ($O(N^2)$):** Manual nested loops for duplicates scale quadratically. Using `list(set(data))` uses hash lookups in $O(N)$ time.
5. **Manual Accumulation vs Built-in `sum()`:** `for num in filtered: total += num` runs in interpreted Python loops instead of C-accelerated `sum(filtered)`.
6. **Redundant Arithmetic Steps:** Step-by-step reassignments collapsed into a single direct calculation.

---

### Optimized Code

```python
"""Optimized version - efficient code for comparison."""

# Optimized: Use list comprehension (single pass)
numbers = list(range(100))
squared_list = [num**2 for num in numbers]

# Optimized: Filter directly without redundant checks
filtered = [val for val in squared_list if val > 100]

# Optimized: Use join for string concatenation (O(n) instead of O(n²))
words = ["sustainable", "code", "is", "about", "measuring", "and", "optimizing"]
text = " ".join(words)

# Optimized: Use set for finding unique items (O(n) instead of O(n²))
data = [1, 2, 3, 4, 5, 1, 2, 3]
unique = list(set(data))

# Optimized: Single pass calculation
total = sum(filtered)
average = total / len(filtered) if filtered else 0

# Optimized: Direct calculation
result = average * 2 + 10 - 5

print(f"Total: {total}")
print(f"Average: {average:.2f}")
print(f"Result: {result:.2f}")
print(f"Unique items: {len(unique)}")
print(f"Text: {text}")
```

---

### Why This is Greener

1. **Reduced CPU Cycles:** Built-ins (`sum`, `join`, `set`) run in compiled C routines, avoiding Python interpreter loop overhead.
2. **Reduced Memory Allocations:** Eliminates intermediate string copies and redundant lists.
3. **Algorithmic Complexity Reduction:** Replaces $O(N^2)$ quadratic algorithms with $O(N)$ linear operations.

---

### Measure It Locally

Measure with CodeCarbon using `EmissionsTracker`:
```python
from codecarbon import EmissionsTracker

with EmissionsTracker() as tracker:
    # Benchmark execution
    pass
```
Check `emissions.csv` for electricity (kWh) and CO₂ emissions.
