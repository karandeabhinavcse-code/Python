# Remove Duplicates 
list1 = [10, 20, 10, 30, 20, 40]
list2 = []
for item in list1:
    if item not in list2:
        list2.append(item)
print("Removing duplicates:", list2)