import os
import re
import shutil
from tqdm import tqdm

def organize_output_folders(input_dir):
    # Check if the directory exists
    if not os.path.exists(input_dir):
        print(f"Directory {input_dir} does not exist.")
        return

    # Regex to match the year in the folder name
    pattern = re.compile(r'SEN2_(\d{4})')

    # Traverse the output directory to find the folders
    for item in tqdm(os.listdir(input_dir), desc="Sorting files"):
        item_path = os.path.join(input_dir, item)
        if os.path.isdir(item_path):
            match = pattern.match(item)
            if match:
                year = match.group(1)
                year_folder_path = os.path.join(input_dir, year)

                # Create year folder if it doesn't exist
                if not os.path.exists(year_folder_path):
                    os.makedirs(year_folder_path)
                    '''tqdm.write(f"Created folder for year {year}")'''  # Terminal output

                # Move the processed data folder into the year folder
                dest_path = os.path.join(year_folder_path, item)
                shutil.move(item_path, dest_path)
                '''tqdm.write(f"Moved {item} to {year_folder_path}")'''  # Terminal output


# Execute script
if __name__ == "__main__":
    # Define directories
    output_directory = "sentinel/Outputs"
    # Call functions
    organize_output_folders(output_directory)
