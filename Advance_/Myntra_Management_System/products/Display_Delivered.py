# Q14. Display delivered orders

from database_connection import get_connection
conn = get_connection()
cursor = conn.cursor()


cursor.execute(

    "Select * from orders where order_status = %s",
    ("Delivered",)
)

for row in cursor.fetchall():
    print(row)