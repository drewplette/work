#DocAcess Report Workaround -- dplette
#For use when document access details are not available from builtin report
#Use in conjuction with adhoc SQL query for doc access details in RA article [INSERT ARTICLE HERE]

import csv

#Read the Role_keys CSV
role_mapping = {}
with open('G:\\Work\\Role_keys.csv', mode='r', newline='') as role_keys_file:
    role_keys_reader = csv.reader(role_keys_file)
    for row in role_keys_reader:
        role_id, role_name = row
        role_mapping[role_id] = role_name

#Read the Role Report CSV
with open('G:\\Work\\Role_Report.csv', mode='r', newline='') as role_report_file:
    role_report_reader = csv.reader(role_report_file)
    header = next(role_report_reader)  # Read the header row
    updated_rows = []

    #Replace role_id values with role_name values and handle multiple IDs
    for row in role_report_reader:
        role_ids = row[-1].split(',')  # Split multiple role_ids from the last column
        role_names = [role_mapping.get(role_id, role_id) for role_id in role_ids]
        row[-1] = ', '.join(role_names)  # Concat role_names back into the last column
        updated_rows.append(row)

#Save the updated Role Report CSV
with open('G:\\Work\\Updated_Role_Report.csv', mode='w', newline='') as updated_role_report_file:
    updated_role_report_writer = csv.writer(updated_role_report_file)
    updated_role_report_writer.writerow(header)  # Write the updated header
    updated_role_report_writer.writerows(updated_rows)
