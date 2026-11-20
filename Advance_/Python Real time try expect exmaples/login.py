# Login System
correct_password = "admin123"
try:
    password = input("Enter your password: ")

    if password != correct_password:
        raise ValueError("Incorrect password.")

    print("Login successful!")
except ValueError as e:
    print("Login failed:", e)