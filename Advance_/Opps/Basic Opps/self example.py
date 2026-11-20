# Understanding self

# self refers to the current object (instance) on which a method is being called.

class Student:
    def __init__(self,name):
        self.name = name

    def display(self):
        print("Name",self.name)

s1 = Student("Abhi")
s1.display()