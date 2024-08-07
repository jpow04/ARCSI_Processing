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
    pattern = re.compile(r'LS.*_(\d{4})')

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

def organize_xml_files(input_dir):
    # Get all subdirectories in the input directory
    subdirectories = [os.path.join(input_dir, d) for d in os.listdir(input_dir) if
                      os.path.isdir(os.path.join(input_dir, d))]

    # Initialize tqdm progress bar for subdirectories
    with tqdm(total=len(subdirectories), desc="Sorting .xml files") as pbar:
        for subdirectory in subdirectories:
            # Traverse the output directory
            for root, dirs, files in os.walk(subdirectory):
                # List to hold XML files in the current folder
                xml_files = [file for file in files if file.endswith('.xml')]

                # If there are XML files, create an XML subfolder and move the files
                if xml_files:
                    xml_folder = os.path.join(root, 'XML')
                    os.makedirs(xml_folder, exist_ok=True)

                    for xml_file in xml_files:
                        src_path = os.path.join(root, xml_file)
                        dest_path = os.path.join(xml_folder, xml_file)
                        shutil.move(src_path, dest_path)
                        # print(f"Moved {xml_file} to {xml_folder}")

            pbar.update(1)  # Update the progress bar after processing each subdirectory


# Execute script
if __name__ == "__main__":
    # Define directories
    output_directory = "landsat/Outputs"
    # Call functions
    organize_xml_files(output_directory)
    organize_output_folders(output_directory)
