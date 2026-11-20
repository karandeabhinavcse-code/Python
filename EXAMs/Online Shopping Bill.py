# Global Variable
store_name = "Super Store Online"

# Customer Details
customer_name = ("Jarvis")
mobile_number = (12345678910)
city = ("Pune")

# Multiple Assignment
laptop_price, mouse_price, keyboard_price, headphones_price, pendrive_price = 55000, 800, 1500, 2500, 700

#Swaping 

#  Total Bill

total_bill = ( laptop_price+ mouse_price+ keyboard_price+ headphones_price+ pendrive_price)


# Display Bill using f-strings
print("\n" + "=" * 40)
print(f"\t{store_name}")
print("=" * 40)

print(f"Customer Name : {customer_name}")
print(f"Mobile Number : {mobile_number}")
print(f"City          : {city}")

print("\nProduct Prices (After Swapping)")
print(f"Laptop     : ₹{laptop_price}")
print(f"Mouse      : ₹{mouse_price}")
print(f"Keyboard   : ₹{keyboard_price}")
print(f"Headphones : ₹{headphones_price}")
print(f"Pen Drive  : ₹{pendrive_price}")

print("-" * 40)
print(f"Total Bill : ₹{total_bill}")
print("=" * 40)
print("Thank You for Shopping!")