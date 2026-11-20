# *Banking Example*
class SBI:

    def interest(self):
        print("7% Interest")
class HDFC:

    def interest(self):
        print("6.5% Interest")
class ICICI:

    def interest(self):
        print("6.75% Interest") 

# Loop

banks = [SBI(), HDFC(), ICICI()]

for bank in banks:
    bank.interest()


    