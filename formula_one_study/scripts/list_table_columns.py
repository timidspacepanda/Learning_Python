import os
import pandas as pd

# Folder containing files
folder_path = r"C:\Users\iamky\10_Learning_Python\formula_one_study\data\formula-one-data"

# Iterate over all files in folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        try:
            # Read CSV Files (only headers)
            df = pd.read_csv(file_path, nrows=0)
            print(f"File: {filename}")
            print("Columns: ", list(df.columns))
            print("-" * 50)
        except Exception as e:
            print(f"Error reading {filename}: {e}")