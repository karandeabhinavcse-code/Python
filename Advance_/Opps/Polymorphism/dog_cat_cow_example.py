class Dog:
    def soud(self):
        print("Woof Woof")

class Cat:
    def sound(self):
        print("Meow Meow")

class Cow:
    def sound(self):
        print("moo moo")

animals = [Dog(),Cat(),Cow()]

for animal in animals:
    animal.sound()