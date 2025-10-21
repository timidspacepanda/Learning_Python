from datetime import datetime, timedelta
from typing import List, Literal
import calendar


class PaymentScheduler:
    """Calculate project payment dates with business day adjustments."""

    # US Federal Holidays (fixed and observable dates)
    FEDERAL_HOLIDAYS = {
        'New Year': (1, 1),
        'Independence Day': (7, 4),
        'Juneteenth': (6, 19),
        'Veterans Day': (11, 11),
        'Christmas': (12, 25)
    }

    def __init__(self, adjustment_rule: Literal[
        'following', 'preceding', 'modified_following', 'modified_preceding'] = 'following'):
        """
        Initialize payment scheduler.

        Args:
            adjustment_rule: How to handle non-business days
                - 'following': Move to next business day
                - 'preceding': Move to previous business day
                - 'modified_following': Following, but stay in same month
                - 'modified_preceding': Preceding, but stay in same month
        """
        self.adjustment_rule = adjustment_rule

    def get_federal_holidays(self, year: int) -> List[datetime]:
        """Get all US federal holidays for a given year."""
        holidays = []

        # Fixed date holidays
        for name, (month, day) in self.FEDERAL_HOLIDAYS.items():
            holidays.append(datetime(year, month, day))

        # Floating holidays
        holidays.append(self._nth_weekday(year, 1, 0, 3))  # MLK Day (3rd Monday in Jan)
        holidays.append(self._nth_weekday(year, 2, 0, 3))  # Presidents Day (3rd Monday in Feb)
        holidays.append(self._last_weekday(year, 5, 0))  # Memorial Day (Last Monday in May)
        holidays.append(self._nth_weekday(year, 9, 0, 1))  # Labor Day (1st Monday in Sep)
        holidays.append(self._nth_weekday(year, 10, 0, 2))  # Columbus Day (2nd Monday in Oct)
        holidays.append(self._nth_weekday(year, 11, 3, 4))  # Thanksgiving (4th Thursday in Nov)

        return holidays

    def _nth_weekday(self, year: int, month: int, weekday: int, n: int) -> datetime:
        """Find the nth occurrence of a weekday in a month."""
        first_day = datetime(year, month, 1)
        first_weekday = first_day.weekday()

        # Calculate days until first occurrence
        days_until = (weekday - first_weekday) % 7
        first_occurrence = first_day + timedelta(days=days_until)

        # Add weeks to get nth occurrence
        return first_occurrence + timedelta(weeks=n - 1)

    def _last_weekday(self, year: int, month: int, weekday: int) -> datetime:
        """Find the last occurrence of a weekday in a month."""
        last_day = datetime(year, month, calendar.monthrange(year, month)[1])
        last_weekday = last_day.weekday()

        # Calculate days back to last occurrence
        days_back = (last_weekday - weekday) % 7
        return last_day - timedelta(days=days_back)

    def is_business_day(self, date: datetime) -> bool:
        """Check if a date is a business day (not weekend or federal holiday)."""
        # Check if weekend
        if date.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
            return False

        # Check if federal holiday
        holidays = self.get_federal_holidays(date.year)
        for holiday in holidays:
            if date.date() == holiday.date():
                return False

        return True

    def adjust_to_business_day(self, date: datetime) -> datetime:
        """Adjust a date to the nearest business day based on adjustment rule."""
        if self.is_business_day(date):
            return date

        original_month = date.month

        if self.adjustment_rule == 'following':
            while not self.is_business_day(date):
                date += timedelta(days=1)

        elif self.adjustment_rule == 'preceding':
            while not self.is_business_day(date):
                date -= timedelta(days=1)

        elif self.adjustment_rule == 'modified_following':
            while not self.is_business_day(date):
                date += timedelta(days=1)
            # If moved to next month, go back to previous month
            if date.month != original_month:
                date = datetime(original_month, calendar.monthrange(date.year, original_month)[1], date.year)
                while not self.is_business_day(date):
                    date -= timedelta(days=1)

        elif self.adjustment_rule == 'modified_preceding':
            while not self.is_business_day(date):
                date -= timedelta(days=1)
            # If moved to previous month, go forward to current month
            if date.month != original_month:
                date = datetime(date.year, original_month, 1)
                while not self.is_business_day(date):
                    date += timedelta(days=1)

        return date

    def generate_schedule(self,
                          start_date: datetime,
                          end_date: datetime,
                          interval_days: int = None,
                          interval_months: int = None,
                          num_payments: int = None) -> List[dict]:
        """
        Generate payment schedule.

        Args:
            start_date: Project start date
            end_date: Project end date
            interval_days: Payment interval in days (exclusive with interval_months)
            interval_months: Payment interval in months (exclusive with interval_days)
            num_payments: Optional number of payments (if not provided, calculates until end_date)

        Returns:
            List of payment dictionaries with original and adjusted dates
        """
        if interval_days and interval_months:
            raise ValueError("Specify either interval_days or interval_months, not both")

        if not interval_days and not interval_months:
            raise ValueError("Must specify either interval_days or interval_months")

        schedule = []
        current_date = start_date
        payment_num = 1

        while current_date <= end_date:
            if num_payments and payment_num > num_payments:
                break

            adjusted_date = self.adjust_to_business_day(current_date)

            schedule.append({
                'payment_number': payment_num,
                'original_date': current_date.strftime('%Y-%m-%d'),
                'adjusted_date': adjusted_date.strftime('%Y-%m-%d'),
                'is_adjusted': current_date.date() != adjusted_date.date(),
                'day_of_week': adjusted_date.strftime('%A')
            })

            # Calculate next payment date
            if interval_days:
                current_date += timedelta(days=interval_days)
            else:  # interval_months
                # Add months while handling month-end edge cases
                month = current_date.month + interval_months
                year = current_date.year + (month - 1) // 12
                month = ((month - 1) % 12) + 1

                # Handle day overflow (e.g., Jan 31 -> Feb 31 becomes Feb 28/29)
                max_day = calendar.monthrange(year, month)[1]
                day = min(current_date.day, max_day)

                current_date = datetime(year, month, day)

            payment_num += 1

        return schedule


# Example usage
if __name__ == "__main__":
    # Create scheduler with 'following' adjustment rule
    scheduler = PaymentScheduler(adjustment_rule='following')

    # Example 1: Monthly payments for a 6-month project
    print("=" * 70)
    print("EXAMPLE 1: Monthly payments")
    print("=" * 70)
    schedule = scheduler.generate_schedule(
        start_date=datetime(2025, 1, 15),
        end_date=datetime(2025, 7, 15),
        interval_months=1
    )

    for payment in schedule:
        adj_marker = " (ADJUSTED)" if payment['is_adjusted'] else ""
        print(f"Payment {payment['payment_number']}: "
              f"{payment['original_date']} → {payment['adjusted_date']} "
              f"({payment['day_of_week']}){adj_marker}")

    # Example 2: Bi-weekly payments
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Bi-weekly payments (14 days)")
    print("=" * 70)
    schedule = scheduler.generate_schedule(
        start_date=datetime(2025, 6, 30),  # Monday before July 4
        end_date=datetime(2025, 9, 30),
        interval_days=14
    )

    for payment in schedule:
        adj_marker = " (ADJUSTED)" if payment['is_adjusted'] else ""
        print(f"Payment {payment['payment_number']}: "
              f"{payment['original_date']} → {payment['adjusted_date']} "
              f"({payment['day_of_week']}){adj_marker}")

    # Example 3: Quarterly payments with modified_following rule
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Quarterly payments (modified_following rule)")
    print("=" * 70)
    scheduler_mod = PaymentScheduler(adjustment_rule='modified_following')
    schedule = scheduler_mod.generate_schedule(
        start_date=datetime(2025, 1, 31),
        end_date=datetime(2025, 12, 31),
        interval_months=3
    )

    for payment in schedule:
        adj_marker = " (ADJUSTED)" if payment['is_adjusted'] else ""
        print(f"Payment {payment['payment_number']}: "
              f"{payment['original_date']} → {payment['adjusted_date']} "
              f"({payment['day_of_week']}){adj_marker}")