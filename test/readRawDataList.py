import pandas as pd

# Replace 'your_file.xlsx' with the actual Excel file path
excel_file_path = 'output.xlsx'

# Replace 'Sheet1' with the sheet name and 'Column1' with the column header you want to read
sheet_name = 'Sheet1'
column_name = 'Column1'

# Read the Excel file and store the specified column in a list
try:
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
    column_list = df[column_name].tolist()
    print("List from Excel column:", column_list)
    print("Size list is:", len(column_list))
except FileNotFoundError:
    print(f"Error: File '{excel_file_path}' not found.")
except KeyError:
    print(f"Error: Sheet or column name not found in the Excel file.")
