import mysql.connector
#  Data base connaction 

conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root",
    database = "companydb"

)
# Create 
cursor = conn.cursor()

def add_employees():
    name = input("Enter Name: ")
    salary = float(input("Enter Salary: "))
    dept = input("Enter Department: ")

    sql = """
    INSERT INTO employees(emp_name,salary,department)
    VALUES(%s,%s,%s)
"""

    values = (name, salary, dept)

    cursor.execute(sql,values)
    conn.commit()

    print("Employees Addes Successfully")

# READ

def view_employees():

    cursor.execute("SELECT * FROM employees")

    records = cursor.fetchall()

    print("\n Employees Records")
    print("-"*50)

    for row in records:
        print(row)

#  UPDATE

def update_employee():
    emp_id = int(input("Enter Employee ID: "))
    salary = float(input("Enter New Salary: "))
    sql = """
    UPDATE employees
    set salary=%s
    WHERE emp_id=%s
    """

    values = (salary,emp_id)

    cursor.execute(sql,values)
    conn.commit()

    print("Employee Updated Successfully")

# DELETE 

def delete_employee():
    emp_id = int(input("Enter Employee ID: "))

    sql = """
    DELETE FROM employees
    WHERE emp_id=%s
"""

    values = (emp_id,)

    cursor.execute(sql, values)
    conn.commit()

    print("Employee delete successfully")

#  menu

while True:
    print("\n ===== EMPLOYEE MANAGEMENT=====")
    print("1. Add Employee")
    print("2. View Employee")           
    print("3. Update Employee")
    print("4. Delete Employee")
    print("5. Exit")

    choice = input("Enter Choice: ")

    if choice == "1":
        add_employees()

    elif choice =="2":
        view_employees()

    elif choice == "3":
        update_employee()

    elif choice == "4":
        delete_employee()

    elif choice == "5":
        print("Thank You")
        break

    else:
        print("Invalid Choice")

cursor.close()
