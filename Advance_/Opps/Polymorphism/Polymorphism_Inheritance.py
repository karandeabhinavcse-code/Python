# Parant

class Animal:
    def sound(Self):
        print("Animal Sount")

        # child

class Dog (Animal):
    def sound(Self):
        print ("Woof")

class Cat(Animal):
    def sound(self):
        print("Meow")

# object

animals = [Dog(),Cat()]

for animal in animals:
    animal.sound()