# Q13. Products with discount greater than 15%

from database_connection import get_connection
conn = get_connection()
cursor = conn.cursor()


cursor.execute(

    "Select * from products where discount >%s",\
        (15,)
)

for row in cursor.fetchall():
    print(row)