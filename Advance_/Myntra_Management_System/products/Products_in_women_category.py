# Q15. Products in Women Fashion category   

from database_connection import get_connection
conn = get_connection()
cursor = conn.cursor()

query = """

select p.*
from products p 
join categories c
on p.category_id = c.category_id
where c.category_name = %s

""" 

cursor.execute(query,("Women Fashion",))

for row in cursor.fetchall():
    print(row)

conn.close()
cursor.close()