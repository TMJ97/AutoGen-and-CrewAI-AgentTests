#python
# filename: financial_data_analysis.py

import csv

# Read the contents of the file
file_path = 'Financial-Sample-Much-Shortened.csv'

# Create lists to store the financial data
units_sold = []
gross_sales = []
discounts = []
sales = []
cogs = []
profit = []

with open(file_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Process the data and extract relevant fields
        units_sold.append(float(row['Units Sold']))

        # Clean up the string formatting for numerical fields
        gross_sales.append(float(row[' Gross Sales '].replace(',', '').replace('$', '').strip()))
        discounts.append(float(row[' Discounts '].replace(',', '').replace('$', '').strip()))
        sales.append(float(row[' Sales '].replace(',', '').replace('$', '').strip()))
        cogs.append(float(row[' COGS '].replace(',', '').replace('$', '').strip()))
        profit.append(float(row[' Profit '].replace(',', '').replace('$', '').strip()))

# Perform financial analysis
total_units_sold = sum(units_sold)
total_gross_sales = sum(gross_sales)
total_discounts = sum(discounts)
total_sales = sum(sales)
total_cogs = sum(cogs)
total_profit = sum(profit)

# Analyze the data
average_profit_per_unit = total_profit / total_units_sold
profit_margin = (total_profit / total_sales) * 100

# Output the analysis results
print(f"Total Units Sold: {total_units_sold}")
print(f"Total Gross Sales: ${total_gross_sales}")
print(f"Total Discounts: ${total_discounts}")
print(f"Total Sales: ${total_sales}")
print(f"Total COGS: ${total_cogs}")
print(f"Total Profit: ${total_profit}")
print(f"Average Profit per Unit: ${average_profit_per_unit:.2f}")
print(f"Profit Margin: {profit_margin:.2f}%")