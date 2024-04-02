import csv
import tkinter as tk
from tkinter import filedialog, messagebox

# Create tkinter GUI window
root = tk.Tk()
root.withdraw()

# Display a message box to instruct
messagebox.showinfo("Instructions", "Please select first the Role_keys CSV file and then the Role_Report CSV file.")

# Ask to select the Role_keys CSV file
role_keys_file_path = filedialog.askopenfilename(title="Select Role_keys CSV File", filetypes=[("CSV Files", "*.csv")])

# Ask to select the Role_Report CSV file
role_report_file_path = filedialog.askopenfilename(title="Select Role_Report CSV File", filetypes=[("CSV Files", "*.csv")])

if not role_keys_file_path or not role_report_file_path:
    print("File selection canceled. Exiting.")
    exit()

# Read the Role_keys CSV
role_mapping = {}
with open(role_keys_file_path, mode='r', newline='') as role_keys_file:
    role_keys_reader = csv.reader(role_keys_file)
    for row in role_keys_reader:
        if len(row) >= 2:  # Ensure there are at least two columns in the row
            role_id, role_name = row[:2]  # Take the first two columns
            role_mapping[role_id] = role_name

# Read the Role Report CSV
with open(role_report_file_path, mode='r', newline='') as role_report_file:
    role_report_reader = csv.reader(role_report_file)
    header = next(role_report_reader)  # Read the header row
    updated_rows = []

    # Replace role_id values with role_name values
    for row in role_report_reader:
        role_ids = row[-1].split(',')  # Split role_ids
        role_names = [role_mapping.get(role_id, role_id) for role_id in role_ids]
        row[-1] = ', '.join(role_names)  # Concat role_names 
        updated_rows.append(row)

# Display a message box instructing to save the updated file
messagebox.showinfo("Instructions", "Please choose where to save the updated Role_Report CSV file.")

# Save the updated Role Report CSV to a new file
updated_role_report_file_path = filedialog.asksaveasfilename(title="Save Updated Role_Report CSV File", filetypes=[("CSV Files", "*.csv")])
if updated_role_report_file_path:
    with open(updated_role_report_file_path, mode='w', newline='') as updated_role_report_file:
        updated_role_report_writer = csv.writer(updated_role_report_file)
        updated_role_report_writer.writerow(header)  # Write the updated header
        updated_role_report_writer.writerows(updated_rows)
        messagebox.showinfo("Information", f"Updated Role_Report CSV saved to {updated_role_report_file_path}")
else:
    print("File save canceled.")

# Close tkinter GUI
root.destroy()