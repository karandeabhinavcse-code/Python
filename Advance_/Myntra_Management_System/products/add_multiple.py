from database_connection import get_connection

conn = get_connection()
cursor = conn.cursor()

query = """
INSERT INTO products
(product_name, brand, category_id,
 price, discount, stock, size, color)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
"""

products = [
    ("Formal Shirt", "Peter England", 1, 1800, 10, 40, "M", "White"),
    ("Sports Shoes", "Adidas", 3, 4500, 15, 25, "9", "Black"),
    ("Kurti", "Biba", 2, 2200, 20, 30, "L", "Red"),
    ("Wallet", "Wildcraft", 4, 1200, 5, 60, "Free", "Brown"),
    ("Sunscreen", "Minimalist", 5, 699, 10, 80, "50ml", "White")
]

cursor.executemany(query, products)
conn.commit()

print(cursor.rowcount, "Products inserted!")

cursor.close()
conn.close()