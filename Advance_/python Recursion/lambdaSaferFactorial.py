def factorial(number):

    if number < 0:
        raise ValueError("Number cannot be negative")

    if number in (0, 1):
        return 1

    return number * factorial(number - 1)


print(factorial(5))
print(factorial(0))