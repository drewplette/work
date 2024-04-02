import pandas as pd
from tkinter import Tk, filedialog

# Function to select input CSV file
def select_input_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select CSV file", filetypes=[("CSV files", "*.csv")])
    return file_path

# Function to select export location
def select_export_location():
    root = Tk()
    root.withdraw()
    export_path = filedialog.asksaveasfilename(title="Select export location", defaultextension=".csv")
    return export_path

# Select input CSV file
input_file = select_input_file()

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(input_file)

# Drop duplicates based on Document ID for each distinct user
df_unique = df.drop_duplicates(subset=['document_id', 'login'])

# Group by Login, First Name, and Last Name, and sum the Accesses
df_sum_accesses = df_unique.groupby(['login', 'firstname', 'lastname', 'roles']).agg({'accesses': 'sum'}).reset_index()

# Select export location
export_location = select_export_location()

# Export the resulting DataFrame to CSV
df_sum_accesses.to_csv(export_location, index=False)

print("Export successful.")
