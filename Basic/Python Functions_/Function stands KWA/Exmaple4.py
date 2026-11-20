def student(**kwargs):
    for key, value in kwargs.items():
        print(key,":",value)

student(
    roll_no=1,
    name="Abhi",
    course="sc",
    marks="33"
)

