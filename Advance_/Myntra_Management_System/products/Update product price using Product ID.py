# Q16. Update product price using Product ID

from database_connection import get_connection

conn = get_connection()
cursor = conn.cursor()

product_id = int(input("Enter Product ID: "))
new_price = float(input("Enter New Price: "))

query = """
UPDATE products
SET price = %s
WHERE product_id = %s
"""

cursor.execute(query, (new_price, product_id))
conn.commit()

if cursor.rowcount > 0:
    print("Product Price Updated!")
else:
    print("Product ID Not Found!")

cursor.close()
conn.close()