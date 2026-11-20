# Modifying a Global Variable

# Use the global keyword.

count = 10

def update():
    global count
    count = 20

update()
print(count)
