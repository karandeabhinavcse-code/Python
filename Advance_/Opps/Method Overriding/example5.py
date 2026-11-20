# *5. Vehicle Example*

# Parent:

class Vehicle:

    def start(self):
        print("Vehicle Started")

# Children:

class Car(Vehicle):

    def start(self):
        print("Car Started")


class Bike(Vehicle):

    def start(self):
        print("Bike Started")


class Bus(Vehicle):

    def start(self):
        print("Bus Started")

# Objects:

vehicles = [
    Car(),
    Bike(),
    Bus()
]

for vehicle in vehicles:
    vehicle.start()