import mysql.connector
# Create connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="college"
)

cursor=conn.cursor()


# # Check connection
# if conn.is_connected():
#     print("Connected to MySQL Successfully!")
# # Close connection
# conn.close()

# cursor = conn.cursor()

# create_table_query = """
# CREATE TABLE Students (
#     id INT PRIMARY KEY,
#     name VARCHAR(255),
#     city VARCHAR(255)
# )
# """

# cursor.execute(create_table_query)
# print("Table Create 100%")

# conn.close()


# Insert 


# sql = "INSERT INTO students (id, name, city) VALUES (%s,%s,%s)"
# Values = (1,"Parikh","KOp")

# cursor.execute(sql, Values)
# conn.commit()

# print("Record Inserted Successfully!") 


# cursor.execute("select * from students")

 #for row in cursor.fetchall():
#      print(row)

# sql = "INSERT INTO students (id, name, city) VALUES (%s, %s, %s)"
# values = (2, "Karande", "Mumbai")

# cursor.execute(sql, values)
# conn.commit()

# print("Record inserted successfully!")

