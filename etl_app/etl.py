import pandas as pd
import sqlite3
import os
import logging

logging.basicConfig(
    filename='etl_detailed.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

db_path = "datawarehouse.db"  
conn = sqlite3.connect(db_path)

csv_files = {
    "Service_Dimension.csv": "Service_Dimension",
    "Charity_Dimension.csv": "Charity_Dimension",
    "User_Dimension.csv": "User_Dimension",
    "Date_Dimension.csv": "Date_Dimension",
    "User_Demographics_Dimension.csv": "User_Demographics_Dimension",
    "Transaction_Type_Dimension.csv": "Transaction_Type_Dimension",
    "Service_Category_Dimension.csv": "Service_Category_Dimension",
    "Charity_Category_Dimension.csv": "Charity_Category_Dimension",
    "Transaction_Fact.csv": "Transaction_Fact"
}


def validate_data(df, table_name):
   
    issues = []

    if table_name == "User_Dimension":
        if df['phone'].duplicated().any():
            issues.append("Duplicate phone numbers found.")
        if (df['phone_credit'] < 0).any():
            issues.append("Negative phone credit values found.")
    elif table_name == "Transaction_Fact":
        if df['amount'].isnull().any():
            issues.append("Null transaction amounts found.")
        if df['amount'].min() < 0:
            issues.append("Negative transaction amounts found.")
        if df['date_id'].isnull().any():
            issues.append("Missing date_id in transactions.")

    return issues


print("Starting ETL process...\n")
logging.info("Starting ETL process...")

for file, table in csv_files.items():
    print(f"Processing {file} for table {table}...")
    logging.info(f"Processing {file} for table {table}...")
    try:
        # Extract: Read the CSV file
        print(f"Extracting data from {file}...")
        df = pd.read_csv(file)

        # Transform: Clean and prepare data
        print(f"Transforming data for {table}...")
        df = df.drop_duplicates()  

        # Data validation
        validation_issues = validate_data(df, table)
        if validation_issues:
            for issue in validation_issues:
                print(f"Validation issue in {table}: {issue}")
                logging.warning(f"Validation issue in {table}: {issue}")
            raise ValueError(f"Data validation failed for {table}. Issues: {', '.join(validation_issues)}")

        # Load: Insert into SQLite database
        print(f"Loading data into {table}...")
        df.to_sql(table, conn, if_exists='append', index=False, method='multi', chunksize=1000)

        print(f"SUCCESS: {file} loaded into {table} with {len(df)} rows.\n")
        logging.info(f"SUCCESS: {file} loaded into {table} with {len(df)} rows.")
    except Exception as e:
        print(f"ERROR: Failed to process {file} for {table}. Check logs for details.\n")
        logging.error(f"FAILURE: Could not load {file} into {table}. Error: {e}")



print("Generating ETL summary report...\n")
logging.info("Generating ETL summary report...")
summary = []

for table in csv_files.values():
    try:
        count = pd.read_sql_query(f"SELECT COUNT(*) AS RowCount FROM {table}", conn)
        row_count = count['RowCount'].iloc[0]
        summary.append({'TableName': table, 'RowCount': row_count})
        print(f"{table}: {row_count} rows loaded.")
    except Exception as e:
        logging.error(f"Error fetching row count for {table}: {e}")
        summary.append({'TableName': table, 'RowCount': 'Error'})
        print(f"{table}: Error fetching row count.")
from datetime import datetime

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ETL Summary Report</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            background: linear-gradient(135deg, #f4f4f4, #e8f5e9);
            color: #444;
            padding: 20px;
        }
        h1 {
            color: #2E7D32;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2rem;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
        }
        p {
            text-align: center;
            font-size: 1.1rem;
            margin-bottom: 30px;
            color: #555;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 0 auto;
            background-color: #fff;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            border-radius: 10px;
            overflow: hidden;
            animation: fadeIn 1s ease-in-out;
        }
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        thead {
            background: linear-gradient(90deg, #4CAF50, #81C784);
            color: white;
        }
        th, td {
            padding: 14px 16px;
            text-align: left;
        }
        th {
            text-transform: uppercase;
            font-size: 0.95rem;
            letter-spacing: 1px;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        tr:hover {
            background-color: #e0f2f1;
            transition: background-color 0.3s;
        }
        td {
            font-size: 1rem;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            font-size: 0.9rem;
            color: #666;
        }
        @media (max-width: 600px) {
            table, thead, tbody, th, td, tr {
                display: block;
            }
            th, td {
                text-align: right;
                padding: 10px;
                position: relative;
                border: none;
            }
            th {
                background-color: transparent;
                color: #4CAF50;
                text-align: left;
            }
            td:before {
                content: attr(data-label);
                font-weight: bold;
                text-transform: uppercase;
                position: absolute;
                left: 10px;
                color: #4CAF50;
            }
            td:last-child {
                border-bottom: none;
            }
        }
    </style>
</head>
<body>

<h1>ETL Process Summary</h1>
<p>The following table provides a summary of the ETL process, showing the row count for each table.</p>

<table>
    <thead>
        <tr>
            <th>Table Name</th>
            <th>Row Count</th>
        </tr>
    </thead>
    <tbody>
"""

# Add table rows
for item in summary:
    html_content += f"""
        <tr>
            <td data-label="Table Name">{item['TableName']}</td>
            <td data-label="Row Count">{item['RowCount']}</td>
        </tr>
    """

# Inject the current datetime into the HTML
html_content += f"""
    </tbody>
</table>

<div class="footer">
    <p>Generated on: <strong>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</strong></p>
</div>

</body>
</html>
"""




# Save the HTML report to a file
html_report_path = "etl_summary_report.html"
with open(html_report_path, "w") as file:
    file.write(html_content)

print(f"\nETL summary saved to {html_report_path}.")
logging.info("ETL process completed. Check etl_detailed.log and etl_summary_report.html for details.")

# Close the database connection
conn.close()
print("\nETL process completed successfully.")
