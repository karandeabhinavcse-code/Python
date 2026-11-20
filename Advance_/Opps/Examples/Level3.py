# Inheritance

class Parent:
    def show(self):
        print("Parent Class")

class Child(Parent):
    pass

child = Child()
child.show()


# Parent Class

class Parent:
    def display(self):
        print("This is Parent Class")

parent = Parent()
parent.display()


# Child Class

class Parent:
    def display(self):
        print("Parent Class")

class Child(Parent):
    def show(self):
        print("Child Class")

child = Child()
child.display()
child.show()


# Single Inheritance

class Parent:
    def show(self):
        print("Parent Class")

class Child(Parent):
    def display(self):
        print("Child Class")

child = Child()
child.show()
child.display()


# Multiple Inheritance

class Father:
    def house(self):
        print("House")

class Mother:
    def car(self):
        print("Car")

class Child(Father, Mother):
    pass

child = Child()
child.house()
child.car()


# Multilevel Inheritance

class Grandfather:
    def land(self):
        print("Land")

class Father(Grandfather):
    def house(self):
        print("House")

class Son(Father):
    def bike(self):
        print("Bike")

son = Son()
son.land()
son.house()
son.bike()


# Hierarchical Inheritance

class Parent:
    def show(self):
        print("Parent Class")

class Son(Parent):
    pass

class Daughter(Parent):
    pass

son = Son()
daughter = Daughter()

son.show()
daughter.show()


# Hybrid Inheritance

class A:
    def show1(self):
        print("Class A")

class B(A):
    def show2(self):
        print("Class B")

class C:
    def show3(self):
        print("Class C")

class D(B, C):
    pass

d = D()
d.show1()
d.show2()
d.show3()


# super()

class Parent:
    def show(self):
        print("Parent Class")

class Child(Parent):
    def show(self):
        super().show()
        print("Child Class")

child = Child()
child.show()


# Constructor Inheritance

class Parent:
    def __init__(self):
        print("Parent Constructor")

class Child(Parent):
    def __init__(self):
        super().__init__()
        print("Child Constructor")

child = Child()