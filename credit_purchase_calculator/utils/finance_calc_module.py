def future_value_daily_compound(principal, annual_rate, days):
    
    daily_rate = annual_rate / 365

    return principal * (1 + daily_rate) ** days
