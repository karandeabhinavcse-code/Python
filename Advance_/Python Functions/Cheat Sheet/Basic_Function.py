# 1. Define a Function

def name():
    print("superuser")

name()

# 2. Call a Function

def come():
    print("Come!!!!")
come()

# 3. Function with a Parameter

def treat(name):
    print("Hello", name)

treat("Superuser")

# 4. Return a Value
def add (a, b):
    return a + b

print(add(44, 96))

# 5. Function with Two Parameters

def multiply(a, b):
    return a * b

print(multiply(10,95))

# 6. Default Parameter

def greet(name = "Superuser"):
    print("Hello", name)

# 7. Multiple Parameters

def total(*numbers):
    print(sum(numbers))
total(10,20,30)

# 8. Keyword Arguments

def details(**data):
    print(data)
details(name="Abhinav", age=20, course="BCA")

# 