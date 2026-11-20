# Credit Card

class CreditCard:
    def pay(self):
        print("Paid Using Credit Card")

        # UPI

class UPI:

    def pay(self):
        print("Paid Using UPI")

        # Cash

class Cash:

    def pay(self):
        print("Paid using cash")

        #now

payments = [CreditCard(),UPI(),Cash()]


for payment in payments:
    payment.pay()