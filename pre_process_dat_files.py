import pandas as pd
import os
import glob

# Set your input and output directories
input_dir = r'C:\Users\merup\OneDrive\Desktop\Python_Preprocess\Input_path'
output_dir = r'C:\Users\merup\OneDrive\Desktop\Python_Preprocess\Output_path'

#directory exists
os.makedirs(input_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

# Column names
columns = [
    "Accounts",
    "Account Number",
    "Customer Name",
    "Cradit Limit",
    "Spending",
    "email Id",
    "Available cradit balence",
    "Cradit utlization"
]

# Get all matching .DAT files
dat_files = glob.glob(os.path.join(input_dir, '*.DAT'))

# DEBUG OUTPUT
print(f"Looking in: {input_dir}")
print(f"Found {len(dat_files)} DAT file(s):")
for f in dat_files:
    print(" -", os.path.basename(f))

# Loop over each file
for file_path in dat_files:
    file_name = os.path.basename(file_path)
    file_root, _ = os.path.splitext(file_name)
    output_file = os.path.join(output_dir, f"{file_root}.xlsx")

    data = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.strip() and line.startswith("Account"):
                parts = line.strip().split("|")
                if len(parts) < 6:
                    print(f"Skipping line (not enough columns): {line.strip()}")
                    continue
                acc_type, acc_num, name, limit, spending, email = parts[:6]
                try:
                    limit = float(limit)
                    spending = float(spending)
                    available = limit - spending
                    utilization = round((spending / limit) * 100, 2)

                    row = [
                        acc_type,
                        acc_num,
                        name,
                        limit,
                        spending,
                        email,
                        available,
                        f"{utilization}%"
                    ]
                    data.append(row)
                except ValueError:
                    print(f"Skipped malformed data in file: {file_name}")

    if data:
        df = pd.DataFrame(data, columns=columns)
        df.to_excel(output_file, index=False)
        print(f"Created: {output_file}")
    else:
        print(f"No valid records in: {file_name}")