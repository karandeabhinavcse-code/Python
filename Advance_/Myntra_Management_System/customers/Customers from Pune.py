# Q11. Customers from Pune

from database_connection import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute(
    "select * from customers where city = %s",
    ("Pune",)
)

for row in cursor.fetchall():
    print(row)


    