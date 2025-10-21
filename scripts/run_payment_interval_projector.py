from datetime import datetime, timedelta
from payment_interval_projector import PaymentScheduler

if __name__ == '__main__':
    # Create scheduler with 'modified_following' adjustment rule
    scheduler = PaymentScheduler(adjustment_rule='modified_preceding')

    # General monthly example
    print("=" * 70)
    print("Payment A: Monthly payments")
    print("=" * 70)
    schedule = scheduler.generate_schedule(
        start_date = datetime(2025, 1, 1),
        end_date = datetime(2025, 12, 31),
        interval_months = 1
    )

    for payment in schedule:
        adj_marker = " (ADJUSTED)" if payment['is_adjusted'] else ""
        print(f"Payment {payment['payment_number']}: "
              f"{payment['original_date']} → {payment['adjusted_date']} "
              f"({payment['day_of_week']}){adj_marker}")

    # Bi-weekly Example
    print("=" * 70)
    print("Payment B: Direct-Deposit")
    print("=" * 70)
    schedule = scheduler.generate_schedule(
        start_date=datetime(2025, 10, 24),
        end_date=datetime(2026, 12, 31),
        interval_days = 14
    )

    for payment in schedule:
        adj_marker = " (ADJUSTED)" if payment['is_adjusted'] else ""
        print(f"Payment {payment['payment_number']}: "
              f"{payment['original_date']} → {payment['adjusted_date']} "
              f"({payment['day_of_week']}){adj_marker}")

    # COH Payment
    print("=" * 70)
    print("Payment C: COH Payment Plan")
    print("=" * 70)
    schedule = scheduler.generate_schedule(
        start_date=datetime(2025, 10, 18),
        end_date=datetime(2026, 4, 18),
        interval_months=1
    )

    for payment in schedule:
        adj_marker = " (ADJUSTED)" if payment['is_adjusted'] else ""
        print(f"Payment {payment['payment_number']}: "
              f"{payment['original_date']} → {payment['adjusted_date']} "
              f"({payment['day_of_week']}){adj_marker}")

    # General monthly example
    print("=" * 70)
    print("Payment D: SoCal Edison")
    print("=" * 70)
    schedule = scheduler.generate_schedule(
        start_date = datetime(2025, 10, 2),
        end_date = datetime(2026, 12, 31),
        interval_months = 1
    )

    for payment in schedule:
        adj_marker = " (ADJUSTED)" if payment['is_adjusted'] else ""
        print(f"Payment {payment['payment_number']}: "
              f"{payment['original_date']} → {payment['adjusted_date']} "
              f"({payment['day_of_week']}){adj_marker}")