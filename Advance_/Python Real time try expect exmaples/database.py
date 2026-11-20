# Database Connection 

try:
    import mysql.connector

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="college"
    )
except mysql.connector.Error as e:
    print("Database connection failed:", e)