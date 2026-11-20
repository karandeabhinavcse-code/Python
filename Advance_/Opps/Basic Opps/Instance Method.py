class Student:
    def __init__(self, name):
        self.name = name

    def display(self):
        print("Student:", self.name)

s1 = Student("Amit")
s1.display()