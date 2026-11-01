"""Sample code for measuring emissions."""

# Calculate sum using a loop
total = 0
for i in range(1000):
    total += i

# Process a list
numbers = [1, 2, 3, 4, 5, 10, 20, 50, 100]
squared = [n**2 for n in numbers]
filtered = [n for n in squared if n > 100]

# String operations
text = "Sustainable code is about measuring and optimizing" * 10
words = text.split()
unique_words = set(words)

# Simple calculations
result = sum(filtered) / len(filtered) if filtered else 0

print(f"Total: {total}")
print(f"Filtered squares: {filtered}")
print(f"Average: {result:.2f}")
print(f"Unique words: {len(unique_words)}")
