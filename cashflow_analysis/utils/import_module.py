import pandas as pd

def get_stmt_data(file_path):
    df = pd.read_csv(file_path)

    # Convert amount and running balance to numeric type
    df['Amount'] = pd.to_numeric(df['Amount'].str.replace(',', '', regex=False))
    df['Running Bal.'] = pd.to_numeric(df['Running Bal.'].str.replace(',', '', regex=False))
    
    # Convert to datetime
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    return df