from database_connection import get_connection

conn = get_connection()
cursor = conn.cursor()

customer_id = int(input("Customer ID: "))
order_date = input("Order Date (YYYY-MM-DD): ")
total_amount = float(input("Total Amount: "))
status = input("Order Status: ")

query = """
INSERT INTO orders
(customer_id, order_date, total_amount, order_status)
VALUES (%s,%s,%s,%s)
"""

cursor.execute(
    query,
    (customer_id, order_date, total_amount, status)
)

conn.commit()

print("Order Created Successfully!")
print("Order ID:", cursor.lastrowid)

cursor.close()
conn.close()