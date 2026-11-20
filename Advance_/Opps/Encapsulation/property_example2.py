class Student:
    def __init__(self):
        self.__marks = 90

    @property
    def marks(self):
        return self.__marks

    @marks.setter
    def marks(self, value):
        if 0 <= value <= 100:
            self.__marks = value
        else:
            print("Invalid Marks")

s = Student()

print(s.marks)
s.marks = 95

print(s.marks)
s.marks = 150