# Missing Number 
numbers = [1, 2, 3, 5, 6]

n = len(numbers) + 1  
array_sum  = 0

for num in numbers:
    array_sum += num

total = n * (n + 1) // 2
missing = total - array_sum
print("Missing number is:", missing)