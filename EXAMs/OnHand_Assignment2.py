# Employee Payroll System
# Demonstrates variables, a global variable, f-strings,
# multiple assignment, and swapping two values.

# --- Global Variable ---
company_name = "TechCorp Solutions"


def calculate_gross_salary():
    # --- Employee Details ---
    employee_name = "Amit Verma"
    employee_id = "E101"
    department = "Engineering"
    designation = "Software Developer"

    # --- Salary Components ---
    basic_salary = 45000
    hra = 12000        # House Rent Allowance
    da = 8000          # Dearness Allowance
    bonus = 5000

    # --- Multiple Assignment (demonstration) ---
    # Assign the same value to three variables at once.
    # Here we use it to store the values before calculating Gross Salary.
    hra_value = hra
    da_value = da
    bonus_value = bonus

    # --- Calculate Gross Salary ---
    gross_salary = basic_salary + hra + da + bonus

    # --- Display output using f-strings ---
    print(f"Company Name      : {company_name}")
    print(f"Employee Name     : {employee_name}")
    print(f"Employee ID       : {employee_id}")
    print(f"Department        : {department}")
    print(f"Designation       : {designation}")
    print("-" * 40)
    print(f"Basic Salary      : {basic_salary}")
    print(f"HRA               : {hra}")
    print(f"DA                : {da}")
    print(f"Bonus             : {bonus}")
    print("-" * 40)
    print(f"Gross Salary      : {gross_salary}")
    print()

    # --- Demonstrate Swapping HRA and Bonus ---
    print("Swapping HRA and Bonus...")
    hra, bonus = bonus, hra  # Multiple assignment swap

    print(f"HRA (after swap)  : {hra}")
    print(f"Bonus (after swap) : {bonus}")


if __name__ == "__main__":
    calculate_gross_salary()
