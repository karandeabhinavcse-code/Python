class Father:
    def house(self):
        print("Father owns a housef")


class Son(Father):
    def bike(self):
        print("Son owns a bike ")


s = Son() 
s.house()
s.bike()