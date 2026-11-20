# A double underscore (__) triggers name mangling.

class Student:
    def __init__(self):
        self._password ="Super"

s = Student()

print(s._password)

