balance  = 10000

try:
    amount = int(input("Enter the amount to withdraw: "))

    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    if amount > balance:
        raise ValueError("Insufficient balance.")

    balance  = balance - amount

    print("withdrawal successful")
    print("Remaining balance:", balance)

except ValueError:
    print("Please enter a valid amount")

except Exception as e:
    print("transaction failed:", e)
    