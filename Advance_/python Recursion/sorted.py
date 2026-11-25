# employees = [
#     {"name": "Rahul", "salary": 45000},
#     {"name": "Priya", "salary": 60000},
#     {"name": "Amit", "salary": 35000},
#     {"name": "Sneha", "salary": 75000}
# ]

# sorted_employees = sorted(
#     employees,
#     key=lambda employee: employee["salary"]
# )

# for employee in sorted_employees:
#     print(employee)


# Dissting 

employees = [
    {"name": "Rahul", "salary": 45000},
    {"name": "Priya", "salary": 60000},
    {"name": "Amit", "salary": 35000},
    {"name": "Sneha", "salary": 75000}
]

sorted_employees = sorted(
    employees,
    key=lambda employee: employee["salary"],
    reverse=True
)

for employee in sorted_employees:
    print(employee)