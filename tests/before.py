"""Unoptimized version - inefficient code for comparison."""

# Inefficient: Creating list and then filtering
numbers = list(range(100))
squared_list = []
for num in numbers:
    squared_list.append(num**2)

# Inefficient: Checking membership multiple times
filtered = []
for val in squared_list:
    if val in squared_list:  # Redundant check
        if val > 100:
            filtered.append(val)

# Inefficient: String manipulation with repeated concatenation
text = ""
words = ["sustainable", "code", "is", "about", "measuring", "and", "optimizing"]
for word in words:
    text = text + " " + word  # String concatenation is O(n)

# Inefficient: Nested loop to find duplicates
data = [1, 2, 3, 4, 5, 1, 2, 3]
unique = []
for item in data:
    found = False
    for unique_item in unique:
        if item == unique_item:
            found = True
            break
    if not found:
        unique.append(item)

# Inefficient: Multiple passes over data
total = 0
for num in filtered:
    total += num

average = total / len(filtered) if len(filtered) > 0 else 0

# Inefficient: Redundant calculations
result = average * 2
result = result + 10
result = result - 5

print(f"Total: {total}")
print(f"Average: {average:.2f}")
print(f"Result: {result:.2f}")
print(f"Unique items: {len(unique)}")
print(f"Text: {text.strip()}")
