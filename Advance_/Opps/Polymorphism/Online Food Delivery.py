class Zomato_order:
    def __init__(self, food_amount):
        self.food_amount = food_amount

    def delivery_charge(self):
        return 40

    def final_bill(self):
        delivery = self.delivery_charge()
        total = self.food_amount + delivery

        print("Food Amount:",self.food_amount)
        print("Delivery:",delivery)
        print("Total:",total)

class Swiggy_order:

    def __init__(self,food_amount):
        self.food_amount = food_amount

    def delivery_charges(self):
        return 50

    def final_bill(self):
        delivery = self.delivery_charges()
        total = self.food_amount + delivery

        print("Food Amount:",self.food_amount)
        print("Delivery:",delivery)
        print("Total:",total)

class Restaurant_order: 

    def __init__(self,food_amount):
        self.food_amount = food_amount

    def delivery_charges(self):
        return 50

    def final_bill(self):
        delivery = self.delivery_charges()
        total = self.food_amount + delivery

        print("Food Amount:",self.food_amount)
        print("Delivery:",delivery)
        print("Total:",total)

order = [
     
    Zomato_order(500),
    Swiggy_order(500),
    Restaurant_order(500)
]

for order in order:
    order.final_bill()
    print()

    