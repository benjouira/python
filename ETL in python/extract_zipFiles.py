    # Import the required method
from zipfile import ZipFile

path =r"ETL in python/data/PPR-ALL.zip"
with ZipFile(path, "r") as f:
    # Get the list of files
    file_names = f.namelist()
    print(file_names)
    # Extract the CSV file
    csv_file_path = f.extract(file_names[0])
    print(csv_file_path)