# Q17. Update stock quantity
from database_connection import get_connection

conn = get_connection()
cursor = conn.cursor()

product_id = int(input("Product ID: "))
new_stock = int(input("New Stock: "))

query = """
UPDATE products
SET stock = %s
WHERE product_id = %s
"""

cursor.execute(query, (new_stock, product_id))
conn.commit()

print("Stock Updated!" if cursor.rowcount > 0 else "Product Not Found!")

cursor.close()
conn.close()