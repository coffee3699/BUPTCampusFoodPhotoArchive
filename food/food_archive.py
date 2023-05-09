import re
import os
from collections import defaultdict


# Function to create folder if it doesn't exist
def create_folder(folder_path):
    os.makedirs(folder_path, exist_ok=True)


# Function to process file names
def process_files(files, location_mapping):
    summary = defaultdict(lambda: defaultdict(int))
    todo_folder = "TODO"

    for file in files:
        if "TODO" in file:
            create_folder(todo_folder)
            os.rename(file, os.path.join(todo_folder, file))
            continue

        # Regular expression to match the file name format
        match = re.match(r"^(.*?)-(.+?)\s*(\(\d+\))?\.jpg$", file)

        if match:
            location_code = match.group(1)
            food_name = match.group(2)

            if location_code in location_mapping:
                location = location_mapping[location_code]
            else:
                location = location_code

            location_path = os.path.join(os.getcwd(), location)
            create_folder(location_path)

            food_folder_path = os.path.join(location_path, food_name)
            dest = os.path.join(food_folder_path, file)

            if match.group(3):
                create_folder(food_folder_path)
            else:
                if not os.path.exists(food_folder_path):
                    create_folder(food_folder_path)
                    os.rename(file, dest)
                    summary[location][food_name] += 1
                    continue

            # Move the file to the respective folder
            os.rename(file, dest)

            # Update summary
            summary[location][food_name] += 1

    return summary


# Function to save the summary to a text file
def save_summary(summary, file_name="summary.txt"):
    with open(file_name, "w", encoding="utf-8") as f:
        for location, food_counts in summary.items():
            f.write(f"{location}\n")
            for food_name, count in food_counts.items():
                f.write(f"  {food_name}: {count}\n")
            f.write("\n")


# Location mapping from location code to location name
location_mapping = {
    "JG1": "教工餐厅一层",
    "JG2": "教工餐厅二层",
    "JG3": "教工餐厅三层",
    "JG4": "教工餐厅四层",
    "JG5": "教工餐厅五层",
    "FW1": "风味餐厅一层",
    "FW2": "风味餐厅二层",
    "FW3": "风味餐厅三层",
    "FW4": "风味餐厅四层",
    "FW5": "风味餐厅五层",
    "NQ1": "南区餐厅一层",
    "NQ2": "南区餐厅二层",
    "NQ3": "南区餐厅三层",
    "OUT": "校外美食",
    "WM": "外卖",
    "OTH": "其他",
}

# Get all jpg files in the directory
all_files = [file for file in os.listdir() if file.endswith(".jpg")]


# Process and move the files
summary = process_files(all_files, location_mapping)

# Save the summary to a text file
save_summary(summary)
