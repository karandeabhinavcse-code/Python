# Dunder/Magic Methods


# _init_()- Constructor


    # class Student:
    #     def __init__(self,name):
    #         self.name = name

    # student  = Student("Rahul")

    # print(student.name)


# _str_()- String Representation

    # class Student:

    #     def __str__(self,name,age):
    #         self.name = name
    #         self.age = age

    #     def __str__(self):
    #         return f"(self.name) is {self.age} years old"

    # student = Student("Rahul",30)

    # print(student)


# _repr_()

class Student:


    def __init__(self, name, age):
        self.name = name
        self.age = age


    def __repr__(self):
        return f"Student('{self.name}', {self.age})"



student = Student("Rahul", 20)


print(repr(student))



# _len_() — len()

class ShoppingCart:

    def __init__(self,items):
        self.items = items

    def __len__(self):
        return len(self.items)


cart = cart = ShoppingCart(["Laptop", "Mouse", "Keyboard"])

print(len(cart))


# _add_+-

# class Number:

#     def __init__(self,value):
#         self.value=value


#     def __add__(self, other):
#         return Number(self.value + other.value)

#     def __str__(self):
#         return str(self.value)


# a = Number(10)
# b = Number(20)

# c = a + b

# print(c)


# __s__(-)

# class Number:


#     def __init__(self, value):
#         self.value = value

#     def __sub__(self, other):
#         return str(self.value - other.value)

#     def __str__(self):
#         return str(self.value)

# a = Number(20)
# b = Number(10)

# c = a - b

# print(c)


#  Multiplaction 

class Number:


    def __init__(self, value):
        self.value = value

    def __mul__(self, other):
        return Number(self.value * other.value)
    
    def __str__(self):
        return str(self.value)

a = Number(4)
b = Number(2)

c = a *b

print(c)



class Numbers:


    def __init__(self, value):
        self.value = value

    def __truediv__(self, other):
        return Numbers(self.value / other.value)
    
    def __str__(self):
        return str(self.value)

a = Numbers(4)
b = Numbers(2)

c = a / b

print(c)

