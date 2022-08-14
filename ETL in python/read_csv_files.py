import csv

with open (r"C:\Users\rabi3\OneDrive\Bureau\python\ppr-all.csv", mode='r') as csv_file:
    reader = csv.DictReader(csv_file)
    row = next(reader)
    print (row)