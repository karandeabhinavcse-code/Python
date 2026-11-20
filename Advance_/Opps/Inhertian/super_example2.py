class Employee:

    def __init__(self,name,salary):
        self.name=name
        self.salary=salary

    def show(self):
        print(self.name,self.salary)

# Child

class Manager(Employee):

    def __init__(self,name,salary,department):

        super().__init__(name,salary)

        self.department=department

    def details(self):
        print(self.department)

# Object

m=Manager("Rahul",70000,"IT")

m.show()

m.details()