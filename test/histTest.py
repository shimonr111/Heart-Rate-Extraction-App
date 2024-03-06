import pandas as pd
import matplotlib.pyplot as plt

# Replace 'your_excel_file.xlsx' with the path to your Excel file
excel_file_path = 'output.xlsx'  # Assuming the Excel file is named 'output'

# Read data from Excel file
df = pd.read_excel(excel_file_path)

# Assuming the column name containing the data is 'Column1'
column_name = 'Column1'

# Check if the specified column exists in the dataframe
if column_name not in df.columns:
    print(f"Error: Column '{column_name}' not found in the Excel file.")
else:
    # Extract the data from the specified column
    data = df[column_name]

    # Create a histogram plot using matplotlib
    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=30, color='blue', edgecolor='black')
    plt.title('Histogram Plot of Data')
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()
