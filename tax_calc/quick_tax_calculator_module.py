def calculate_progressive_tax(income):
    # Define the tax brackets and their corresponding rates
    fed_tax_brackets = [
        (0, 11000, 0.1), #(start, end, rate)
        (11000, 44725, 0.12),
        (44725, 95375, 0.22),
        (95375, 182100, 0.24),
        (182100, 231250, 0.32),
        (231250, 578125, 0.35),
        (578125, float('inf'), 0.37)
    ]

    state_tax_brackets = [
        (0, 10100, 0.01), #(start, end, rate)
        (10100, 23943, 0.02),
        (23943, 37789, 0.04),
        (37789, 52456, 0.06),
        (52456, 66296, 0.08),
        (66296, 338640, 0.093),
        (338640, 406364, 0.103),
        (406364, 677276, 0.113),
        (677276, float('inf'), 0.123)
    ]

    total_tax = 0
    fed_standard_deductions = 12500
    state_standard_deductions = 5202

    if income > fed_standard_deductions: #Adjust federal taxable income with standard deductions
        fed_adj_income = income - fed_standard_deductions
    else:
        fed_adj_income = income

    if income > state_standard_deductions: #Adjust state taxable income with standard deductions
        state_adj_income = income - state_standard_deductions
    else:
        state_adj_income = income

    fed_total_tax = tax_maths_procedure(fed_adj_income, fed_tax_brackets)
    state_total_tax = tax_maths_procedure(state_adj_income, state_tax_brackets)
    total_tax = fed_total_tax + state_total_tax

    income_tax_dict = {"total": total_tax, "fed": fed_total_tax, "state": state_total_tax}
    return income_tax_dict # returns a dictionary with broken down tax results

# function called calculate_progressive_tax function
def tax_maths_procedure(income, tax_brackets):
    total_tax = 0
    # Iterate through the tax brackets
    for bracket in tax_brackets:
        start, end, rate = bracket #each row of array

        # Calculate the taxable income within the current bracket
        taxable_income = min(end, income) - start

        # If the taxable income is positive, calculate the tax for this bracket
        if taxable_income > 0:
            bracket_tax = taxable_income*rate
            total_tax += bracket_tax

    return total_tax
