import xlsxwriter

workbook = xlsxwriter.Workbook("Products.xlsx")
worksheet = workbook.add_worksheet()
    
data = [[1, 'books', 'Sapiens', 12]
[2, 'electronics', 'iPhone', 900]
[3, 'books', 'Measure What Matters', 10]
[4, 'books', 'Greenlights', 14]
[5, 'electronics', 'Macbook Pro 13', 1500]]

# Create a table with the available data in the current sheet
worksheet.add_table(
    "B3:E8",
    {
        "data": data,
        "columns": [
          	# Use the appropriate names for the columns
            {"header": "id"},
            {"header": "category"},
            {"header": "name"},
            {"header": "price"},
        ],
    },
)

# Close the current file
workbook.close()