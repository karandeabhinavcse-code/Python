# Student Management System
# global variable 
college_name = "Gopal Kirshna"

# Student dea

age = 45
student_name = "Super User"
roll_no = "34"

# # Multiple Assignment

python_marks, sql_marks, excel_marks, powerbi_marks, ai_marks = 85, 90, 88, 92, 95

# calclucation 

total =  python_marks+sql_marks+excel_marks+powerbi_marks+ai_marks

# Average Marks

Average = total/5


# percentage 

percentage = (total / 500) * 100

# Swapping two variables

# Before swapping 

print("Before Swapping")
print(f"Python Marks:- ")
print(f"Sql Marks:{sql_marks}")

print("===========================================")

print("      STUDENT MANAGEMENT SYSTEM")

print("===========================================")


print(f"College Name:{college_name}")
print(f"Student Name:{student_name}")
print(f"Age         :{age}")
print(f"Roll Numebr :{roll_no}")

print("\n------ Subject Marks ------")

print(f"python: {python_marks}")
print(f"Sql: {sql_marks}")
print(f"Exce: {excel_marks}")
print(f"PowerBI: {powerbi_marks}")
print(f"Ai: {ai_marks}")

print("\n------ Result ------")
print(f"Total Marks : {total}")
print(f"Average     : {Average:2f}")
print(f"Percentage  : {percentage:.2f}%")

print("\nCongratulations!")
print(f"{student_name} has successfully completed the examination.")