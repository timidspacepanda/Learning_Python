""" 
main.py

Description: Runs inventory tasks and outputs user inventory list (.xlsx)

Arguments:

"""
import os
import numpy as np
import pandas as pd
import argparse
from datetime import date
from utils import generate_filename


def generate_user_inventory(df: pd.DataFrame, save_path: str) -> None:
    """
    
    """
    # Ensure 'date' column is in datetime format
    df['date'] = pd.to_datetime(df['date'])

    # Create a new dataframe with the latest `item_name` row
    latest_df = df.sort_values('date').groupby('item_name', as_index=False).last()
    latest_df['date'] = pd.NaT
    latest_df = move_column(latest_df, 'date', 0)

    # Apply restock_flag_logic
    latest_df = restock_flag_logic(latest_df)

    # Save user inventory list to data\processed\ directory
    print(latest_df)
    print(f"Saving user inventory to: {save_path}")
    filepath = generate_filename("user-inventory-", save_path, "xlsx")
    latest_df.to_excel(filepath, index=False)

def restock_flag_logic(df: pd.DataFrame) -> pd.DataFrame:
    """
    
    """
    # Calculate proportion
    stocked_proportion = df['current_quantity'] / df['preferred_stock_level']

    # Set Flag
    df['restock_flag'] = (stocked_proportion <= df['reorder_threshold'])

    return df

def move_column(df, col_name, new_position):
    """
    Moves position of dataframe column based on input arg(zero-based indexing)
    """
    cols = list(df.columns)
    current_position = cols.index(col_name)

    # Only move if the column is not already in the desired position
    if current_position != new_position:
        cols.insert(new_position, cols.pop(current_position))
        df = df[cols]

    return df



if __name__ == "__main__":

    MAIN_INVENTORY_FILEPATH = "C:\\Users\\iamky\\10_Learning_Python\\kitchen-inventory-analyzer\\data\\processed\\main-kitchen-inventory-tracker.xlsx"
    USER_INVENTORY_SAVEPATH = "C:\\Users\\iamky\\10_Learning_Python\\kitchen-inventory-analyzer\\data\\processed\\"

    MAIN_INVENTORY_FILEPATH = os.path.abspath(MAIN_INVENTORY_FILEPATH)
    

    if not os.path.isfile(MAIN_INVENTORY_FILEPATH):
        assert False, f"Error: File not found at {MAIN_INVENTORY_FILEPATH}"
    else:
        print(f"Reading file: {MAIN_INVENTORY_FILEPATH}")

    # Read xlsx file into code.
        df_main = pd.read_excel(MAIN_INVENTORY_FILEPATH)


    # Generate User Inventory Template
    generate_user_inventory(df_main, USER_INVENTORY_SAVEPATH)
    

    