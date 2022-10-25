import csv

path = r"C:\Users\rabi3\OneDrive\Bureau\python\ppr-all.csv"

new_column_names = {
    "Date of Sale (dd/mm/yyyy)": "date_of_sale",
    "Address": "address",
    "Postal Code": "postal_code",
    "County": "county",
    "Price (€)": "price",
    "Description of Property": "description",
}

with open(path, mode="r", encoding="windows-1252") as reader_csv_file:
    reader = csv.DictReader(reader_csv_file)
    # The new file is called "PPR-2021-Dublin-new-headers.csv"
    # and will be saved inside the "tmp" folder    
    with open(r"C:\Users\rabi3\OneDrive\Bureau\python\ppr-all.csv",
                    mode="w",
                    encoding="windows-1252",
                ) as writer_csv_file:
        writer = csv.DictWriter(writer_csv_file, fieldnames=new_column_names)
        # Write header as first line
        writer.writeheader()
        for row in reader:
	        # Write all rows in file
	        writer.writerow(row)