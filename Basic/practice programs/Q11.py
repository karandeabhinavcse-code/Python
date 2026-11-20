# find smallest number in 3 

a = int(input("Enter First Number:- "))
b = int(input("Enter Secound Number:- "))
c = int(input("Enter Thired Number:- "))

if a<b and a<c:
    print(a)
elif b<c:
    print(b)
else:
    print(c)