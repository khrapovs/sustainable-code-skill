# Sustainable Code Optimization Examples

⚠️ **Before using these examples, you must install CodeCarbon.**
See [SETUP.md](../SETUP.md) for complete installation instructions.

---

## Use Case 1: Loop vs Vectorization (NumPy)

**Scenario:** Developer asks to optimize a data processing function for sustainability.

**User Input:**
```python
# Original: inefficient loop over array
def process_data(arr):
    result = []
    for i in range(len(arr)):
        result.append(arr[i] * 2 + 1)
    return result
```

**Skill Response:**
```
🌍 **Sustainable Code Analysis**

I'll measure the carbon emissions of your code and suggest optimizations.

Original Code Emissions:
- CO₂: 0.0042 kg CO₂eq
- Energy: 0.00012 kWh
- Duration: 3.2 seconds

Optimized Code (using NumPy vectorization):
- CO₂: 0.0008 kg CO₂eq ✓
- Energy: 0.000024 kWh
- Duration: 0.8 seconds

**Impact: 81% CO₂ reduction** ↓

Here's the optimized code:
```python
import numpy as np

def process_data(arr):
    return np.array(arr) * 2 + 1
```

**Why this is greener:**
- Vectorized operations use optimized C code (faster, less CPU time)
- Fewer CPU cycles = less electricity consumed
- Reduced duration also contributes to lower emissions
```

---

## Use Case 2: Algorithm Complexity (O(n²) → O(n log n))

**Scenario:** Developer has duplicate-detection code and wants to reduce carbon footprint.

**User Input:**
```python
# Original: O(n²) nested loop
def remove_duplicates(items):
    result = []
    for i in range(len(items)):
        is_dup = False
        for j in range(len(items)):
            if i != j and items[i] == items[j]:
                is_dup = True
                break
        if not is_dup:
            result.append(items[i])
    return result
```

**Skill Response:**
```
🌍 **Sustainable Code Analysis**

Original Code (nested loop, O(n²)):
- CO₂: 0.0156 kg CO₂eq
- Energy: 0.00045 kWh
- Duration: 12.5 seconds

Optimized Code (set-based, O(n)):
- CO₂: 0.0002 kg CO₂eq ✓
- Energy: 0.000006 kWh
- Duration: 0.2 seconds

**Impact: 99% CO₂ reduction** ↓

Here's the optimized code:
```python
def remove_duplicates(items):
    return list(dict.fromkeys(items))  # O(n) with preserved order
```

**Why this is greener:**
- O(n) algorithm vs O(n²) dramatically reduces iterations
- Fewer CPU operations = exponentially less electricity
- Especially important for large datasets
```

---

## Use Case 3: Memory Efficiency (Large Datasets)

**Scenario:** Processing large files; developer wants to optimize for emissions.

**User Input:**
```python
# Original: loads entire file into memory
def process_large_file(filepath):
    with open(filepath) as f:
        lines = f.readlines()  # ← loads all into RAM
    return [line.strip().upper() for line in lines]
```

**Skill Response:**
```
🌍 **Sustainable Code Analysis**

Original Code (full load into memory):
- CO₂: 0.0089 kg CO₂eq
- Energy: 0.00026 kWh
- Duration: 8.1 seconds

Optimized Code (streaming, line-by-line):
- CO₂: 0.0012 kg CO₂eq ✓
- Energy: 0.000035 kWh
- Duration: 1.2 seconds

**Impact: 87% CO₂ reduction** ↓

Here's the optimized code:
```python
def process_large_file(filepath):
    with open(filepath) as f:
        for line in f:  # ← streams, doesn't load all at once
            yield line.strip().upper()
```

**Why this is greener:**
- Reduced RAM usage = lower memory power consumption
- Generators process one item at a time (smaller working set)
- Better for both sustainability and system stability
```

---

## Use Case 4: Library Choices (Pandas vs Native Python)

**Scenario:** Data aggregation task; questioning if Pandas is worth it.

**User Input:**
```python
# Original: native Python
def aggregate_scores(data):
    result = {}
    for record in data:
        key = record['category']
        if key not in result:
            result[key] = []
        result[key].append(record['score'])
    return {k: sum(v)/len(v) for k, v in result.items()}
```

**Skill Response:**
```
🌍 **Sustainable Code Analysis**

Original Code (native loops):
- CO₂: 0.0031 kg CO₂eq
- Energy: 0.000089 kWh
- Duration: 4.2 seconds

Pandas Solution (groupby aggregation):
- CO₂: 0.0018 kg CO₂eq ✓
- Energy: 0.000052 kWh
- Duration: 2.1 seconds

**Impact: 42% CO₂ reduction** ↓

Here's the optimized code:
```python
import pandas as pd

def aggregate_scores(data):
    df = pd.DataFrame(data)
    return df.groupby('category')['score'].mean().to_dict()
```

**Why this is greener:**
- Pandas groupby uses optimized C/Cython backend
- Better memory layout for data operations
- Proven efficient for this use case
- Trade-off: dependency worth the 42% savings for large datasets
```
