"""
data_import_script.py

This script provides a basic import methods to new inventory data.

Usage:
    python data_import_script.py "absolute_path_of_file"

Arguments:


"""
import argparse
import os
import pandas as pd

def clean_strings(df: pd.DataFrame) -> pd.DataFrame:
    """ Clean dataframe strings so all variables are lowercase and are separated by underscores."""
    for col in df.select_dtypes(include=['object']):
        df[col] = df[col].str.strip().str.lower().str.replace(' ', '_')
        return df
    
def append_unique_rows(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    """ Determine column names match and append unqiue rows."""
    if list(df1.columns) == list(df2.columns):
        combined = pd.concat([df1, df2], ignore_index=True)
        combined = combined.drop_duplicates()
        return combined
    else:
        raise ValueError("DataFrames have different columns and cannot be appended.")

if __name__ == "__main__":
    MAIN_INVENTORY_FILEPATH = "C:\\Users\\iamky\\10_Learning_Python\\kitchen-inventory-analyzer\\data\\processed\\main-kitchen-inventory-tracker.xlsx"

    # Pass file to code (absolute path)
    parser = argparse.ArgumentParser(description="Process a file by absolute path.")
    parser.add_argument("filepath", help="Absolute path to the file")
    args = parser.parse_args()

    file_path = os.path.abspath(args.filepath)
    MAIN_INVENTORY_FILEPATH = os.path.abspath(MAIN_INVENTORY_FILEPATH)

    if not os.path.isfile(file_path):
        assert False, f"Error: File not found at {file_path}"
    else:
        print(f"Reading file: {file_path}")

    # Read xlsx file into code.
        df = pd.read_excel(file_path)
        df_main = pd.read_excel(MAIN_INVENTORY_FILEPATH)
        
    # Check and modify `item_name` to > strip leading and trailing spaces,
    # lowercase strings, and substitute word separtors (' ') with underscores
        #df = df.fillna('NaN')
        df = clean_strings(df)

    # Check column names are the same with main inventory dataset. Append new data into main inventory dataset. 
        df_main = append_unique_rows(df_main, df)

        print("Appended with duplicates removed:")
        print(df_main)

    # Overwrite main inventory list .xlsx file
    print(f"Overwriting main inventory file: {MAIN_INVENTORY_FILEPATH}")
    df_main.to_excel(MAIN_INVENTORY_FILEPATH, index=False)

