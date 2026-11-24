# Q6. Display all products

from database_connection import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT * FROM products")

for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()

