# Q12. Display all orders of a customer

from database_connection import get_connection

conn = get_connection()
cursor = conn.cursor()

customer_id = int(input("Enter Customer ID: "))

query = """
select * from orders
where customer_id = %s
 """

cursor.execute(query,(customer_id,))

for row in cursor.fetchall():
    print(row)