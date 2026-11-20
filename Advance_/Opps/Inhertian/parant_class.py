#  parant class
class Animal:
    def eat(self):
        print("Eating")

    def sleep(self):
        print("Sleeping")


# Clild class
class Dog(Animal):
     pass

dog = Dog()

dog.eat()

dog.sleep()