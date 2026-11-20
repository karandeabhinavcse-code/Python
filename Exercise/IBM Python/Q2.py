# Find the first non-repeating character in a string 

string = "swiss"

for char in string:
    if string.count(char) == 1:
        print("First non-repeating character:", char)
        break
else:
    print("No non-repeating word")  
