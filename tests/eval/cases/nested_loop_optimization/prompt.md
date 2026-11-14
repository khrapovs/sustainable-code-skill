Can you measure the emissions of this function and suggest a greener approach?

```python
def find_common_elements(first: list[int], second: list[int]) -> list[int]:
    common = []
    for item in first:
        if item in second:
            common.append(item)
    return common
```
