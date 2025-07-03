def calculate_progressive_tax(income):
    # Define the tax brackets and their corresponding rates
    tax_brackets = [
        (0, 11000, 0.1), #(start, end, rate)
        (11000, 44725, 0.12),
        (44725, 95375, 0.22),
        (95375, 182100, 0.24),
        (182100, 231250, 0.32),
        (231250, 578125, 0.35),
        (578125, float('inf'), 0.37)
    ]

    total_tax = 0
    standard_deductions = 12500

    if income > standard_deductions: #Adjust taxable income with standard deductions
        adj_income = income - standard_deductions
    else:
        adj_income = income


    # Iterate through the tax brackets
    for bracket in tax_brackets:
        start, end, rate = bracket #each row of array

        # Calculate the taxable income within the current bracket
        taxable_income = min(end, adj_income) - start

        # If the taxable income is positive, calculate the tax for this bracket
        if taxable_income > 0:
            bracket_tax = taxable_income*rate
            total_tax += bracket_tax

    return total_tax

# Example usage
income = int(input("Enter gross income: "))
tax = calculate_progressive_tax(income)
print(f"Progressive tax for income ${income}: ${tax: .2f}")
