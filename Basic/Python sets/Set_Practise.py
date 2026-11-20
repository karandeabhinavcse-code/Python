# visitors = ["Amit", "Rohit", "Amit", "Gaurav", "Rohit"]

# unique_visitors = set(visitors)
# print(unique_visitors)

# students = {"Amit", "Rohit", "Gaurav"}

# print("Rohit" in students)

# class_A = {"Amit", "Rohit", "Gaurav"}
# class_B = {"Gaurav", "Sahil", "Amit"}

# print(class_A & class_B)


#  find common , all ,only Electronics 

# electronics = {"Laptop", "Mobile", "Tablet"}
# fashion = {"Shirt", "Shoes", "Mobile"}

# print(electronics & fashion)
# print(electronics | fashion)
# print(electronics - fashion)



# you = {"Inception", "Titanic", "Avatar"}
# friend = {"Avatar", "Joker", "Titanic"}

# print("Both watched:", you & friend)
# print("Only you:", you - friend)
# print("Only friend:", friend - you)


python_devs = {"Amit", "Rohit", "Sahil"}
ml_devs = {"Sahil", "Gaurav", "Amit"}

print("Both skills:", python_devs & ml_devs)
print("Only Python:", python_devs - ml_devs)
print("At least one:", python_devs | ml_devs)