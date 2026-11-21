from database_connection import get_connection

conn = None
cursor = None

try:
    conn = get_connection()
    cursor = conn.cursor()

    product_name = input("Product Name: ")
    brand = input("Brand: ")
    category_id = int(input("Category ID: "))
    price = float(input("Price: "))
    discount = float(input("Discount: "))
    stock = int(input("Stock: "))
    size = input("Size: ")
    color = input("Color: ")

    query = """
    INSERT INTO products
    (product_name, brand, category_id,
     price, discount, stock, size, color)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        product_name, brand, category_id,
        price, discount, stock, size, color
    )

    cursor.execute(query, values)
    conn.commit()

    print("Product Added Successfully!")
    print("Product ID:", cursor.lastrowid)

except Exception as e:
    if conn and conn.is_connected():
        conn.rollback()
    print("Error:", e)

finally:
    if cursor:
        cursor.close()
    if conn and conn.is_connected():
        conn.close()