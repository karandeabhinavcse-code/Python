# *7. Calling Parent Method Using super()*

# Sometimes we don't want to completely replace the parent's method.

# We want:

# Run parent's method first, then run child's additional code.

# Use:

super()

# Example:

class Employee:

    def work(self):
        print("Employee logged in")


class Developer(Employee):

    def work(self):

        super().work()

        print("Developer started coding")

# Now:

dev = Developer()

dev.work()