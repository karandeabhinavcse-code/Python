# *6. Employee Example*
class Employee:

    def work(self):
        print("Employee is working")


class Developer(Employee):

    def work(self):
        print("Developer writes Python code")


class Tester(Employee):

    def work(self):
        print("Tester tests software")


class Manager(Employee):

    def work(self):
        print("Manager manages the team")