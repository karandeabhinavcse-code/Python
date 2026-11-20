# for i in range (1,11):
#     print(i)


# for j in range (1,21):
#     print(j)


# for e in range(1, 21):
#     if e % 2 == 0:
#         print(e)

# total = 0
# for p in range(1, 11):
#     total += p

# print("Sum:", total)


# # Print multiplication table of 5

# for g in range(1, 11):
#     print("5 x", g, "=", 5 * g)

#  =================================================================================================

text = "python programming"
count = 0

for ch in text:
    if ch in "aeiou":
        count += 1

print("Vowels:", count)



# Find largest number in list

nums = [10, 25, 5, 40, 15]
largest = nums[0]

for n in nums:
    if n > largest:
        largest = n

print("Largest:", largest)

# Reverse a string

text = "hello"
rev = ""

for ch in text:
    rev = ch + rev

print(rev)


# Factorial of number


num = 5
fact = 1

for i in range(1, num + 1):
    fact *= i

print("Factorial:", fact)


# Simple Login Attempts (3 tries)

for i in range(3):
    pwd = input("Enter password: ")
    if pwd == "1234":
        print("Login success")
        break
else:
    print("Account blocked")


