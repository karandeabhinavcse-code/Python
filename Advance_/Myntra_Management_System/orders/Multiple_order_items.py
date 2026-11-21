from database_connection import get_connection

conn = get_connection()
cursor = conn.cursor()

order_id = int(input("Enter Order ID: "))

items = [
    (order_id, 1, 2, 1599),
    (order_id, 2, 1, 899),
    (order_id, 3, 1, 2499)
]

query = """
INSERT INTO order_items
(order_id, product_id, quantity, item_price)
VALUES (%s,%s,%s,%s)
"""

cursor.executemany(query, items)
conn.commit()

print("Order Items Added Successfully!")

cursor.close()
conn.close()