from abc import ABC,abstractclassmethod

class Payment(ABC):
    @abstractclassmethod
    def pay(self,amount):
        pass



class UPI(Payment):
    def pay(self,amount):
        
