# Palindrome 
# Write a Python program to check whether a given string is a palindrome 
# Output "Palindrome"

string = "madam"
reversed_string = string[::-1]
if string == reversed_string:
    print("Palindrome")
