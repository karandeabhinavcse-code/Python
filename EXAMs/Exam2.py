print("Qusetion 1")

lst = [10, 5, 20, 8, 15, 3, 25, 7, 12, 18]

print("Max:", max(lst))
print("Min:", min(lst))
print("Sum:", sum(lst))


print("Question 3")

lst = [10, 20, 4, 45, 99]

lst.sort()
print("Second largest:", lst[-2])


print("Question 5")

sup = [ 89, 12, 144, 13, 169, 69, 44, 33, 16, 12, 12]
print(sup.count(12))


print("Question 6")

t = (10, 20, 5, 40, 15)

print("Length:", len(t))
print("Max:", max(t))
print("Min:", min(t))


t = (1, 2, 3)
lst = list(t)

print("Tuple to List:", lst)

print("Question 7")

lst2 = [4, 5, 6]
t2 = tuple(lst2)

print("List to Tuple:", t2)


print("Question 8")

t = (10, 20, 30, 40)
x = 20

print(x in t)


print("Question 9")

marks = {"A": 80, "B": 75}

# Add
marks["C"] = 90

# Update
marks["A"] = 85

# Delete
del marks["B"]

print(marks)


print("Question 10")

my_dict = {3: "C", 1: "A", 4: "D", 2: "B"}

sorted_dict = {}

for key in sorted(my_dict):
    sorted_dict[key] = my_dict[key]

print(my_dict)
print(sorted_dict)


print("Question 11")


d1 = {"a": 1, "b": 2}
d2 = {"c": 3, "d": 4}

d1.update(d2)

print(d1)

print("Question 12")

s1 = {1, 2, 3}
s2 = {2, 3, 4}

print("Common:", s1 & s2)

print("print 13")

s1 = {1, 2, 3}
s2 = {2, 3, 4}

print("Union:", s1 | s2)
print("Intersection:", s1 & s2)
print("Difference:", s1 - s2)

print("Question 14")

s1 = {1, 2}
s2 = {1, 2, 3}

print(s1.issubset(s2))

print("Question 15")

s = {1, 2, 3, 4}

print("Original set:", s)

s.remove(1)
print(s)

s.remove(2)
print(s)

s.remove(3)
print(s)

s.remove(4)
print(s)
