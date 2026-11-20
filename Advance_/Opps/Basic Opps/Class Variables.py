class Student:
    college = "Super Uni"

    def __init__(self , name):
        self.name = name

s1 = Student("Super")
s2 = Student("User")

print(s1.college)
print(s2.college)