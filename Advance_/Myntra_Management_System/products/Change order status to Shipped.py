# Q19. Change order status to Shipped

from database_connection import get_connection
conn = get_connection()
cursor = conn.cursor()

order_id = int(input("Enter Order ID: "))

query = """
UPDATE orders
SET order_status = %s
WHERE order_id = %s
AND order_status = %s
"""

cursor.execute(
    query,
    ("Shipped", order_id, "Processing")
)

conn.commit()

if cursor.rowcount > 0:
    print("Order Status Updated!")
else:
    print("Order Not Found or Not Processing!")

cursor.close()
conn.close()