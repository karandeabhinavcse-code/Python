sql = "INSERT INTO students (id, name, city) VALUES (%s,%s,%s)"
Values = (1,"Parikh","KOp")

cursor.execute(sql, Values)
conn.commit()

print("Record Inserted Successfully!") 

