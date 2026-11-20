class Animal:

    def sound(self):
        print("Animal Sound")


class Dog(Animal):

    def sound(self):
        print("Dog says Woof")


animal = Animal()
dog = Dog()

animal.sound()
dog.sound()