# With Validation
class Bank:

    def __init__(self):
        self.__balance = 5000

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print("Deposited:", amount)

    def withdraw(self, amount):
        if amount <= self.__balance:
            self.__balance -= amount
            print("Withdrawn:", amount)
        else:
            print("Insufficient Balance")

    def show_balance(self):
        print("Balance:", self.__balance)

account = Bank()

account.deposit(2000)
account.withdraw(1000)
account.show_balance()