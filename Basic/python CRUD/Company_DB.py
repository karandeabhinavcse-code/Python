import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="company_db"
)

if conn.is_connected():
    print("Connected to mysql successfully")

    conn.close()