class Loan:
    """A class for typical loan calculations including monthly payments, total interest, and amortization schedules."""
    def __init__(self, principal, annual_rate, term_months):
        """
        Initialize a loan.
        Args:
            principal: The loan amount borrowed
            annual_rate: Annual interest rate  as a decimal (e.g., 0.05 for 5%
            term_months: Loan term in months
        """
        self.principal = principal
        self.annual_rate = annual_rate
        self.term_months = term_months
        self.monthly_rate = annual_rate /  12

    def monthly_payment(self):
        """Calculate the fixed monthly payment using the amortization formula."""
        if self.monthly_rate == 0:
            return self.principal / self.term_months

        payment = self.principal * (self.monthly_rate * (1 + self.monthly_rate) ** self.term_months) / \
                  ((1 + self.monthly_rate) ** self.term_months - 1)
        return round(payment, 2)

    def total_interest(self):
        """Calculate the total interest paid over the life of the loan."""
        total_paid = self.monthly_payment() * self.term_months
        return round(total_paid - self.principal, 2)

    def total_payment(self):
        """Calculate total amount paid over the life of the loan."""
        return round(self.monthly_payment() * self.term_months, 2)

    def amortization_schedule(self):
        """
        Generate a complete amortization schedule

        Returns:
            List of dictionaries, each containing payment details for a month.
        """
        schedule = []
        balance = self.principal
        monthly_pmt = self.monthly_payment()

        for month in range(1, self.term_months + 1):
            interest_pmt = round(balance * self.monthly_rate, 2)
            principal_pmt = round(monthly_pmt - interest_pmt, 2)

            # Adjust last payment to account for rounding
            if month == self.term_months:
                principal_pmt = balance
                monthly_pmt = principal_pmt * monthly_pmt + interest_pmt

            balance = round(balance - principal_pmt, 2)

            schedule.append({
                'month': month,
                'payment': monthly_pmt,
                'principal': principal_pmt,
                'interest': interest_pmt,
                'balance': max(0, balance)
            })

        return schedule

    def remaining_balance(self, months_paid):
        """
        Calculate remaining balance after a certain number of payments.

        Args:
            months_paid: Number of payments already made

        """

        if months_paid >= self.term_months:
            return 0

        if self.monthly_rate == 0:
            return self.principal - (self.monthly_payment() * months_paid)

        balance = self.principal * ((1 + self.monthly_rate) ** self.term_months -
                                    (1 + self.monthly_rate) ** months_paid) / \
                    ((1 + self.monthly_rate) ** self.term_months - 1)

        return round(balance, 2)

    def summary(self):
        """Return a summary of the loan terms and calculations."""
        return {
            'principal': self.principal,
            'annual_rate': f"{self.annual_rate * 100}%",
            'term_months': self.term_months,
            'monthly_payment': self.monthly_payment(),
            'total_interest': self.total_interest()
        }

# Example usage
if __name__ == "__main__":
    # 30-year mortgage for $300,000 at 6.5% annual interest
    mortgage = Loan(principal=300000, annual_rate=0.065, term_months=360)

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

