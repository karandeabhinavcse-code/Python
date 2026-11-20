import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="company_db"
)

cursor = conn.cursor()

query = """
insert into employees
(emp_name,department,salary,city)
values(%s, %s, %s, %s)
"""


values = (
    "Sneha",
    "Python Development",
    48000,
    "Pune"
)


cursor.execute(query, values)

conn.commit()

print("Employee inserted successfully!")

cursor.close()
conn.close()