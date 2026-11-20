# Global Keyword

salary = 25000

def increment():
    global salary
    salary += 5000

increment()
print(salary)
