def square(number):
    return number * number


def process_number(function, number):

    return function(number)


result = process_number(square, 5)

print(result)