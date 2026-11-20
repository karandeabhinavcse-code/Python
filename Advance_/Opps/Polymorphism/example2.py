class Dog:
    def sound(self):
        print("Dog say Woof")

class Cat:
    def sounf(self):
        print("Cow say Meow")

class Cow:
    def sound(self):
        print("Cow says Mooo")

animals = [Dog(),Cat(),Cow()]

for animal in animals:
    animal.sound()