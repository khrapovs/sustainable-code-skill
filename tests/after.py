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
