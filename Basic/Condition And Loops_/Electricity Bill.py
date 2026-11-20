units = int(input("Enter units: "))

if units > 100:
    bill = units * 5 + 50
else:
    bill = units * 5

print("Bill:", bill)


