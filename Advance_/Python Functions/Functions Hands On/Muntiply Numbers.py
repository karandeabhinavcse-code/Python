
def calculate_sum(n):

    total = n

    for i in range(1, n + 1):
        total = total * i

    return total


print(calculate_sum(10))