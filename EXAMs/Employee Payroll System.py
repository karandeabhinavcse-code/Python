# Global Variable
company_name = "Secure Valute"

# Create Variable

employee_name = ("Abhinav Karande")
employee_ID = ("88944")
deparment = "Cyber Security"
designation = ("Secure")

# Store

# salary = "550000"
# har = "10000"
# da = "9500"
# bonus = "50000"

# Calcuate

# multiple assignment

salary, har, da, bonus = 55000, 10000, 1000, 5000

# Gross Salary

GrossSalary = salary + har + da + bonus



# Calcualtion 

GrossSalary = salary+har+da+bonus

print(f"Company Name:    {company_name}")
print(f"Employee Name:   {employee_name}")
print(f"Employee ID:     {employee_ID}")
print(f"Deparment:       {deparment}")
print(f"Designation:     {designation}")
print(f"Salary:          {salary}")
print(f"HAR:             {har}")
print(f"DA               {da}")
print(f"Bonus:           {bonus}")


print("Swapping HRA and Bonus...")
har, bonus = bonus, har  # Multiple assignment swap

print(f"HRA (after swap)  : {har}")
print(f"Bonus (after swap) : {bonus}")