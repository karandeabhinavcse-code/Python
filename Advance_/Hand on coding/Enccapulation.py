class Bank:
    def __init__(self):
        self.__balance = 1000

    def check_balance(self):
        print(self.__balance)

account = Bank()
account.check_balance()  