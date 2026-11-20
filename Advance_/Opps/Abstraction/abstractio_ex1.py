# Practice Question

# Create an abstract class:

# Vehicle

# Create an abstract method:

# start()

# Create three child classes:

# Car
# Bike
# Bus

# Implement start() differently:

# Car  → "Car Started"
# Bike → "Bike Started"
# Bus  → "Bus Started"

# Then create objects and call:

# car.start()
# bike.start()
# bus.start()



from abc import ABC, abstractclassmethod
# Abstract class
class Vehicle(ABC):
    @abstractclassmethod
    def start(self):
        pass

# Child Class 1
class Car(Vehicle):
    def start(self):
        print("Car Started")

# Child class 2
class Bike(Vehicle):

    def start(self):
        print("Bike Started")

# Child Class 3

class Bus(Vehicle):
    def start(self):
        print("Bus Started")

# Creating Object 

car = Car()
bike = Bike()
bus = Bus()

# Calling Methods

car.start()
bike.start()
bus.start()
