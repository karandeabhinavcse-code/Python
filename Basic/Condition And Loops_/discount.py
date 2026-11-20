amount = float(input("Enter Amout Of Shoping:- "))

if amount > 1000:
    discount = amount * 0.10
    print("Final price",amount-discount)
else:
    print("No discount. Final price:", amount)

