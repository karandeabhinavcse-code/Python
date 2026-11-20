# In Python, a single underscore (_) is a convention that says:

# "Please don't access this directly unless you're inside the class or a subclass.

class Student:

    def _init_(self):
        self._marks = 95

s = Student()

print(s._marks)