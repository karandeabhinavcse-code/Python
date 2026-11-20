# Public Menber 
# A Public member can be accessed directly from outside the class 


# Syntax 

class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age


student = Student("Super", 21)

print(student.name)
print(student.age)


# Protected Members 

class Student:
    def __init__(self,name):
        self._name = name

    def display(self):
        print(self._name)

student = Student ("Rhaul")

student.display()

print(student._name)

# Private Menbers 

class Student:
    def __init__(self,name):
        self.__name = name

    def display(self):
        print(self.__name)


student = Student("Chota Bhim")

student.display()


