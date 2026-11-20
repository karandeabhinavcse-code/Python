class Student:
    def __init__(self, roll_no, name, marks):
        self.roll_no = roll_no
        self.name = name
        self.marks = marks

    def calculate_grade(self):
        if self.marks >=90:
            grade = "A"

        elif self.marks >= 75:
            grade = "B"

        elif self.marks >= 60:
            grade = "c"

        elif self.marks >=40:
            grade = "D"

        else:
            grade = "F"

        print("\nStudent Details")
        print("-"*30)
        print("Roll No :",self.roll_no)
        print("Name    :",self.name)
        print("Marks   :",self.marks)
        print("Grade   :",grade)

s1 = Student(101, "Superuer",88)
s1.calculate_grade()