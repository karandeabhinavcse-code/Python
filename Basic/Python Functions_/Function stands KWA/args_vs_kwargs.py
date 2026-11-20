# *args vs **kwargs
# *args → Multiple Positional 

# Arguments

def add(*args):
    print(args)

add(10, 20, 30)

# **kwargs → Multiple Keyword Arguments


def info(**kwargs):
    print(kwargs)

info(name="Rahul", age=20)



# Interview Question
# What is **kwargs?

# **kwargs allows a function to receive any number of keyword arguments and stores them in a dictionary.

# def details(**kwargs):
#     for key, value in kwargs.items():
#         print(key, value)

# details(name="Rahul", city="Pune")

