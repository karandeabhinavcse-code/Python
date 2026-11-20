# Q1 def
# Q2 str
# Q3 flot
# Q4 **
# Q5 if
# Q6 input()
# Q7 <class 'int'>
# Q8 for
# Q9 #
# Q10 break
# Q11 []
# Q12 20
# Q13 insert()
# Q14 pop()  remove()
# Q15 3
# Q16 sort()
# Q17 reverse()
# Q18 Extracting elements
# Q19 20:30
# Q20 pop()
# Q21 ()
# Q22 NO
# Q23 10
# Q24 count()
# Q25 count()
# Q26 index()
# Q27 tuple()
# Q28 No
# Q29 Creating tupel
# Q30 Assinging tuple values to variables
# Q31 {}
# Q32 Key-Value Pairs
# Q33 John
# Q34 keys()
# Q35 values()
# Q36 items()
# Q37 Retrieves value safely 
# Q38 No
# Q39 remove()
# Q40 delete()
# Q41 SELECT
# Q42 CREATE TABLE
# Q43 INSERT
# Q44 GROUP BY
# Q45 UPDATE
# Q46 DROP
# Q47 DELETE
# Q48 SORT
# Q49 SUM
# Q50 mysql.connector

#  =================Coding Section============

#                        Q1 



# numbers = [23,33,44,1,43,58,81,66,65,99]
# largest = max(numbers)
# print(largest)


#                       Q2


# number1 = [34]

# if number1 % 2==0:
#     print("Even")
# else:
#     print("Odd")

#                      Q3


numbers = [10, 15, 22, 33, 44, 55, 66, 77, 88, 99]

even_count = 0
odd_count = 0

for num in numbers:
    if num % 2 == 0:
        even_count += 1
    else:
        odd_count += 1

print("Even numbers:", even_count)
print("Odd numbers:", odd_count)


#                        Q4

# Create a tuple
my_tuple = (10, 20, 30, 40, 50)

# Display tuple elements using a loop
print("Tuple elements are:")
for item in my_tuple:
    print(item)


#                        Q5 

my_tuple = (10, 20, 30, 20, 40, 20, 50)

value = 20

count = my_tuple.count(value)

# Display result
print("Occurrences of", value, "=", count)


#                  Q6
