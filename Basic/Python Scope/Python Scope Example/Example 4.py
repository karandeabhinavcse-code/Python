# Nested Function

def college():
    course = "BCA"

    def student():
        print(course)

    student()

college()