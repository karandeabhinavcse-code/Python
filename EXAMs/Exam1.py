
print(" Question 1")

list_1 = [1,2,3,4,5]
list_2 = [6,7,8,9,10]

a = list_1 + list_2

print(a)


print("Question 2")


list_super = [1,2,3,4,5,6,7]

nums = [10, 24, 76, 23, 12]
Big_number = max(nums)

print(Big_number)

print("Question Q3")


my_tuple = ("Apple", "Banana", "Cherry", "Date", "Elderberry")

print("First element:", my_tuple[0])

print("Last element:", my_tuple[-1])

print("Question Q4")

t = (10, 20, 30)

print(20 in t)     
print(50 not in t)

print("Question Q5")

numbers_tuple = (10, 20, 10, 30, 10, 40, 50)

print(numbers_tuple.count(10))

super = {"name": "Alice", "age": 25, "city": "New York"}
print(super)

print("Question Q6")


person = {"name": "Alex", "age": 28, "city": "New York", "salary": 50000}

# Update
person["age"] = 25
print("Updated Dictionary:- ", person)

# Remove
person.pop("city")
print("Dictionary after removing city:- ", person)

# Check existence   
print("Does 'name' exist?:- ", "name" in person)

# Print keys
print("Keys:- ", person.keys())

# Print values
print("Values:- ", person.values())


