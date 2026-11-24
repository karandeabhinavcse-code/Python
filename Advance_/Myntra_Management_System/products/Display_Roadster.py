# Q8. Display Roadster products

from database_connection import get_connection
conn = get_connection()
cursor = conn.cursor()


query = "SELECT * FROM products where brand = %s"

cursor.execute(query, ("Roadster",))

for product in cursor.fetchall():
    print(product)

