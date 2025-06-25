"""main.py"""
# Imports
import argparse
import os
import sys
from datetime import datetime
import shutil
import pandas as pd
import numpy as np

def parse_args():

    # command-line input argument method
    parser = argparse.ArgumentParser(add_help=True, description="Syntax")
    parser.add_argument('--sheetpath', 
                        type=str,
                        required=True,
                        help="Absolute path of input sheet."
                    )

    args = parser.parse_args() # parse arguments
    sheetpath = args.sheetpath

    # Convert path into absolute path
    abs_path = os.path.abspath(sheetpath)

    # Check if file exists

    if not os.path.isfile(abs_path):
        print(f"Error: File does not exist at: {abs_path}")
        sys.exit(1)

    return abs_path

def cost_after_taxes_method(cost, qty, sales_tax):
    """Calculates the total cost after quantity and sales tax"""
    tot_cost = cost * qty * (1 + sales_tax)
    return tot_cost

def term_interest_method(principal, apr, num_days_financed):
    """Calculate the total term interest of a loan (compound interest daily)"""
    daily_rate = apr / 365
    final_amt = principal * (1 + daily_rate) ** num_days_financed
    return final_amt - principal    

def append_timestamp_to_filename(filename):

    # Split the filename into base and extension
    base, ext = os.path.splitext(filename)

    # Format: output_2025-06-22_22-13-00
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    new_filename = f"{base}_{timestamp}{ext}"

    return new_filename


if __name__ == "__main__":
    LENGTH_OF_MONTH = 28
    filepath = parse_args()
    #print(f"File path received: {filepath}")

    # read excel file
    ORIGINAL_DATA = pd.read_excel(filepath) # Default: reads first sheet
    df = ORIGINAL_DATA.copy()  # Variable used to compare with output of this code.
                        # Determines if output needs to be written to a new excel file.

    pd.set_option('display.precision', 4) # global pandas precision

    print(df.head())
    print(df.shape)

    ## Calculation Methods
    # Calculate Total Cost
    df['Total Cost'] = df.apply(
        lambda row: cost_after_taxes_method(
            row['Cost'],
            row['Qty'],
            row['Sales_Tax']
        ),
            axis=1
    )

    # Calculate Term Interest
    df['Total Int.'] = df.apply(
        lambda row: term_interest_method(
            row['Total Cost'],
            row['APR_%'],
            row['Term_Period_Days']
        ),
            axis=1
    )

    # Calculate Total Financed Cost
    df['Total_Financed_Cost'] = df['Total Cost'] + df['Total Int.']
    # Calculate Monthly Payment (28-day Interval)
    df['Num_Payments'] = np.ceil( df['Term_Period_Days'] / LENGTH_OF_MONTH )
    df['Monthly_Payment'] = df['Total_Financed_Cost'] / df['Num_Payments']
    df.drop('Num_Payments', axis=1, inplace=True) # remove column so NOT shown in output

    print(df.head())
    print(df.shape)

    # Compare if new dataframe (after applying methods) is different
    # from the input argument dataframe (from excel file)
    df_isdiff = not ORIGINAL_DATA.equals(df)

    # Save to Excel (If file exists, rename old file by appending date and time)
    if os.path.exists(filepath) and df_isdiff:
        BACKUP_FILENAME = append_timestamp_to_filename(filepath)
        shutil.move(filepath, BACKUP_FILENAME)
        print(f"Renamed exisiting file to: {BACKUP_FILENAME}")


    # Save dataframe into Excel file
    if df_isdiff:
        df.to_excel(filepath, index=False)
        print(f"New file saved as {filepath}")
    else:
        print("Output dataframe is the same as input dataframe. No new file saved.")
        