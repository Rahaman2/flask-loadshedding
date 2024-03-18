import os
import re
# Relative directory path
directory = 'schedules'

# Get the absolute path
absolute_directory = os.path.abspath(directory)

# List all files in the directory
files = os.listdir(absolute_directory)

# Print each filename
for file in files:
    if file.startswith("western-cape-"):
        pattern = r"western-cape-(.*?)\.csv"
        pattern2 = r'western-cape-(.*?)\.csv'
        # municipality = 
        municipality_match = re.search(pattern2,file)
        match = re.search(pattern, file)
        # print(1)
        if match and municipality_match:
            municipality = municipality_match.group(1)
            # print(municipality)
            extracted_text = match.group(1)
            print(f"{re.sub(r'-', ' ', extracted_text.capitalize())},western-cape-{municipality}")
    