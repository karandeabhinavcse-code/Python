# Object

class Student:
    def study(self):
        print("Student is studying")

student1=Student()

student1.study()

# Class

class Car:
    pass

car1 = Car()
car2 = Car()

print(car1)
print(car2)

# Object 

class mobile:
    def call(self):
        print("Calling.............")

phone1 = mobile()
phone2 = mobile()

phone1.call()
phone2.call()


# Attributes

class Student:
    name = "Rahul"
    age = "88"
    course = "Super"

student1 = Student()

print(student1.name)
print(student1.age)
print(student1.course)


# Method

class Calculator:

    def add(self):
        print(10 +20 )

    def subtract(self):
        print(20-10)

calculator = Calculator()

calculator.add()
calculator.subtract()

# Self 

class Person:
    def introduce(self):
        print("My name is Rhaul")

person1 = Person()
person1.introduce()

# Self 2

class Person:
    def set_name(self):
        self.name = "Rhaul"

    def show_name(self):
        print(self.name)

person1 = Person()


person1.set_name()
person1.show_name()


# __init__() Constructor

class Employee:

    def __init__(self):
        print("Employee object created")

employee1 = Employee()


# Creating Object 

class Laptop:
    def start(self):
        print("Laptop started")

laptop1 = Laptop()
laptop2 = Laptop()

laptop1.start()
laptop2.start()

# Instance Variables

class Student:

    def __init__(self, name, age):
        self.name = name
        self.age = age


student1 = Student("Rahul", 20)
student2 = Student("Priya", 22)

print(student1.name)
print(student1.age)

print(student2.name)
print(student2.age)

# Instance Methods

class BankAccount:

    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def show_balance(self):
        print("Owner:", self.owner)
        print("Balance:", self.balance)


account1 = BankAccount("Rahul", 5000)

account1.show_balance()

