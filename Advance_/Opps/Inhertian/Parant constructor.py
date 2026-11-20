class Animal:
    def __init__(self,name):
        self.name=name

# Child

class Dog(Animal):
    pass

d=Dog("Tommy")
print(d.name)

