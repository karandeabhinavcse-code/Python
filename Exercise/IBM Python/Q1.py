# Find the common elements between two lists 

list1 = [10, 20, 30, 40, 50]
list2 = [30, 40, 50, 60, 70]

common_elements = list(set(list1) & set(list2))
print("Common elements:", common_elements)

