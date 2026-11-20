class BankAccount:

    def __init__(self, account_no, holder_name, balance):
        self.account_no = account_no 
        self.holder_name = holder_name
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"${amount} deposited successfully.")

    def withdraw(self, amount):
        if amount<= self.balance:
            self.balance -= amount
            print(f"${amount} withdrawn Successfully.")
        else:
            print("Insufficient Balance!")

    def display_balance(self):
        print("\nAccount Details")
        print("-"*30)
        print("Account No  :",self.account_no)
        print("Holder Name :",self.holder_name)
        print("Balance     :$" ,self.balance)

acc1 = BankAccount(1001,"Superuser",500000)
acc1.display_balance()
acc1.deposit(150000)
acc1.withdraw(12000)
acc1.display_balance()
