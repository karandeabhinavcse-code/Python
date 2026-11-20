from abc import ABC, abstractclassmethod

class Vehicle(ABC):
    @abstractclassmethod
    def start(self):
        pass

class Car(Vehicle):
    def start(self):
        print("Car Started")


class Bike(Vehicle):
    def start(self):
        print("Bike Started")


class Bus(Vehicle):
    def start(self):
        print("Bus Started")


car = Car()
bike = Bike()
bus = Bus()

car.start() 
bike.start()
bus.start()