def employee(**kwargs):
    for key, value in kwargs.items():
        print(key,":",value)
        
employee(
    emp_id=101,
    name="Amith",
    department="IT",
    salary=50000
)
