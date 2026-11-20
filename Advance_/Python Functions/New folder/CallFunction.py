# make a function of full addhar card and call 
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

# Call the function
addhar_card()