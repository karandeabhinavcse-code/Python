# Q7. Search product using Product ID

from database_connection import get_connection

conn = get_connection()
cursor = conn.cursor()

product_id = int(input("Enter Product ID"))

query = "SELECT * FROM products where product_id = %s"

cursor.execute(query,(product_id,))

result = cursor.fetchone()

if result:
    print("Product Details",result)

else:
    print("Product Not Found")


cursor.close()
conn.close()