# Import the required library
import requests

path ="https://assets.datacamp.com/production/repositories/5899/datasets/19d6cf619d6a771314f0eb489262a31f89c424c2/ppr-all.zip"
# Get the zip file
response = requests.get(path)

# Print the status code
print(response.status_code) 
# men 8iir a9wes el status code

# Save the file locally (more about open() in the next lesson)
local_path = f"ETL in python/data/PPR-ALL.zip"
with open(local_path, "wb") as f:
    f.write(response.content)



    # 

