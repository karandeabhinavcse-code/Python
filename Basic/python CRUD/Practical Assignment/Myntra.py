import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="myntra_db"
)

cursor = conn.cursor()

# if conn.is_connected():
#     print("Connected to sql")

#     conn.close()

# Read 

tables = ['categories','products','customers','order','order_items']

for tables in tables:
    # print(f"\n--- Data from {tables.upper()} table ---")
    print(f"")

cursor.execute("select * from tables")

cursor.close()
conn.close()


# update

# update_query = """
# UPDATE products 
# SET price = %s, discount = %s 
# WHERE product_id = %s
# """


# new_values = (799.00, 15.00, 2)
# new_values = (799.00, 15.00, 2)

# conn.commit()
# print(f"{cursor.rowcount} record(s) updated successfully.")

# cursor.close()
# conn.close()









# Questions 

# Level 1 – CREATE (INSERT)
# Easy
# 1. Write a Python program to add a new product to the Myntra products table. Accept product name, brand, category ID, price, discount, stock, size and color from the user.

# 2. Create a Python program to register a new Myntra customer. Accept customer name, email, phone and city.

# 3. Write a program to insert five new products using executemany().

# 4. Create a Python program to add a new customer order. Accept customer ID, order date, total amount and order status.

# 5. Create a Python program to add multiple products to an existing order using the order_items table.