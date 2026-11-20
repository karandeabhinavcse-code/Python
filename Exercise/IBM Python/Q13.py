# Anagram input list1 = "listen"

string1 = input("Enter first string: ")
string2 = input("Enter second string: ")

frequency1 = {}
frequency2 = {}

for char in string1:
    frequency1[char] = frequency1.get(char, 0) + 1

for char in string2:
    frequency2[char] = frequency2.get(char, 0) + 1

if frequency1 == frequency2:
    print("Anagram")
else:
    print("Not Anagram")