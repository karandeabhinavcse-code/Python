class Vehicle:
    def start(self):
        print("Vehicle Started")

class Car(Vehicle):
    def drive(self):
        print("Driving Car")
        
c=Car()
c.start()
c.drive()

