# Make a function addhar card and voting id pan card and call them

def addhar_card():
    name = input("Enter your name: ")
    dob = input("Enter your date of birth (DD/MM/YYYY): ")
    gender = input("Enter your gender: ")
    address = input("Enter your address: ")
    addhar_number = input("Enter your Addhar number: ")

    print("Addhar Card Details:")
    print("Name:", name)
    print("Date of Birth:", dob)
    print("Gender:", gender)
    print("Address:", address)
    print("Addhar Number:", addhar_number)

    print("-----------------------------------------------------------------------------")


def voting_id():
    name = input("Enter your name: ")
    dob = input("Enter your date of birth (DD/MM/YYYY): ")
    gender = input("Enter your gender: ")
    address = input("Enter your address: ")
    voting_number = input("Enter your Voting number: ")

    print("Voting ID Details:")
    print("Name:", name)
    print("Date of Birth:", dob)
    print("Gender:", gender)
    print("Address:", address)
    print("Voting Number:", voting_number)

    print("-----------------------------------------------------------------------------")

def pan_card():
    name = input("Enter your name: ")
    dob = input("Enter your date of birth (DD/MM/YYYY): ")
    gender = input("Enter your gender: ")
    address = input("Enter your address: ")
    pan_number = input("Enter your PAN number: ")

    print("PAN Card Details:")
    print("Name:", name)
    print("Date of Birth:", dob)
    print("Gender:", gender)
    print("Address:", address)
    print("PAN Number:", pan_number)


addhar_card()
voting_id()
pan_card()

