transactions = [500, 1500, 3000, 4500, 800, 6000]

high_value = list(
    filter(lambda amount: amount > 2000, transactions)
)

print(high_value)


