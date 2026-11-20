arr = [25, 10, 45, 5, 30]

maximum = arr[0]
minimum = arr[0]

for number in arr:
    if number > maximum:
        maximum = number 
    if number < minimum:
        minimum = number

print("Maximum =", maximum)
print("Minimum =", minimum)
