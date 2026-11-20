class Car:

    def __init__(self, brand, model, price):
        self.brand = brand
        self.model = model
        self.price = price

    def display_details(self):
        print("Car Details")
        print("-" * 30)
        print("Brand :",self.brand)
        print("Model :",self.model)
        print("Price :",self.price)

car1 = Car ("Toyota","Fortuner",450000)

car1.display_details()