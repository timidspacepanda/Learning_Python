from loan_calc_tool_class import Loan

mortgage = Loan(principal=500000, annual_rate=0.065, term_months=360)

print("Loan Summary")
for key, value in mortgage.summary().items():
    print(f"   {key}:  {value}")

print("\nFirst 3 months of amortization:")
schedule = mortgage.amortization_schedule()

for payment in schedule[:3]:
    print(f"   Month {payment['month']}: Payment=${payment['payment']}, "
          f"Principal=${payment['principal']}, Interest=${payment['interest']}, "
          f"Balance=${payment['balance']}")
print(f"\nRemaining balance after 5 years: ${mortgage.remaining_balance(60)}")