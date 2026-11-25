from database_connection import get_connection

conn = get_connection()
cursor = conn.cursor()

customer_id = int(input("Customer ID: "))
new_email = input("New Email: ")

query = """
UPDATE customers
SET email = %s
WHERE customer_id = %s
"""

cursor.execute(query, (new_email, customer_id))
conn.commit()

print("Email Updated!" if cursor.rowcount > 0 else "Customer Not Found!")

cursor.close()
conn.close() 