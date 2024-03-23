import ast
import pandas as pd

# Used this file for debugging our processes, by exports large matrices into csv files

# Specify the path to your text file
text_file_path = "list.txt"

# Read the content of the text file
with open(text_file_path, "r") as file:
    # Read each line and parse the string representation of the list into an actual list
    lists = [ast.literal_eval(line.strip()) for line in file]

# Create a DataFrame for each list
dfs = [pd.DataFrame(lst, columns=[f"Column{i+1}"]) for i, lst in enumerate(lists)]

# Specify the Excel file path
excel_file_path = "output.xlsx"

# Write each DataFrame to a separate sheet in Excel
with pd.ExcelWriter(excel_file_path, engine='xlsxwriter') as writer:
    for i, df in enumerate(dfs):
        sheet_name = f"Sheet{i+1}"
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"Excel file '{excel_file_path}' created successfully.")
