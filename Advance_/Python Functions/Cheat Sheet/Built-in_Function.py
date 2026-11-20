# 1 Display Output
print("Abhinav")

# 2. input() — Accept User Input
# name = input("Enter our fav car: ")
# print("Your favorite car is:", name)

# 3. type() — Check Data Type

a = 20
b = 4.94
c = "Superuser"
d = False

print("Data type of a:", type(a))
print("Data type of b:", type(b))
print("Data type of c:", type(c))
print("Data type of d:", type(d))

# 4. int() — Convert to Integer

a = int("85")
b = int(18.8)

print(a)
print(b)

# 5. float() — Convert to Float

a = float(85) 
b = float("55.4")
  
print(a)
print(b)

# 6. str() — Convert to String

a = str(95)
print(a)

# 7. bool() — Convert to Boolean

print(bool(1))
print(bool(0))

# 8. len() — Count Items 

print(len("Abhinav"))

# 9. range() — Generate a Sequence of Integers

for i in range (1,96):
    print(i)

# 10. sum() — Calculate the Total

numbers = [10, 20, 30]
print(sum(numbers))

# 11. min() — Find the Minimum 

numbers = [12,34,45,56,67]
print(min(numbers))

# 12. max() — Find the Maximum
numbers = [12,34,45,56,67]
print(max(numbers))

# 13. abs() — Find Absolute 
print(abs(-5))

# 14. round() — Round a Number
print(round(5.678, 2))

# 15. pow() — Calculate Power
print(pow(2, 4))  

# 16. divmod() —  Quotient and Remainder
print(divmod(10, 5))