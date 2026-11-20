# Instead of calling methods like get_balance(), Python provides a cleaner approach.

class Bank:

    def _init_(self):
        self.__balance = 10000

    @property
    def balance(self):
        return self.__balance

account = Bank()

print(account.balance)