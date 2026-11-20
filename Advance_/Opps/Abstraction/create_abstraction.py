
# class Payment(ABC):

#     @abstractmethod
#     def pay(self, amount):
#         pass


# class UPI(Payment):

#     def pay(self, amount):
#         print(f"₹{amount} paid using UPI")


# # Credit Card:

# class CreditCard(Payment):

#     def pay(self, amount):
#         print(f"₹{amount} paid using Credit Card")


        
# # Net Banking:

# class NetBanking(Payment):

#     def pay(self, amount):
#         print(f"₹{amount} paid using Net Banking")

# Use them:

# payments = [
#     UPI(),
#     CreditCard(),
#     NetBanking()
# ]

# for payment in payments:
#     payment.pay(5000)



