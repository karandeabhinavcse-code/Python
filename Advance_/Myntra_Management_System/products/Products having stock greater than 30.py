# Q10. Products having stock greater than 30

from database_connection import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute(
    "Select * from products where stock > %s",
    (30,)
)

for row in cursor.fetchall():
    print(row)

    