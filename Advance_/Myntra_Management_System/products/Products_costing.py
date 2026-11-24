# Q9. Products costing more than ₹2,000

from database_connection import get_connection
conn = get_connection()
cursor = conn.cursor()

cursor.execute(
    "select * from products where price > %s",
    (2000,)
)

for row in cursor.fetchall():
    print(row)

conn.close()
cursor.close()