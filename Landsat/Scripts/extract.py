import os
import subprocess
from tqdm import tqdm

# Function to extract landsat data files from RAW directory using the arcsiextractdata.py command
def extract_landsat_data(input_dir, output_dir):
    # Check for and create output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory {output_dir}")

    # Collect all .tar files in subdirectories
    tar_files = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.tar'):
                tar_files.append((root, file))

    # Run command through all collected .tar files
    for root, file in tqdm(tar_files, desc="Extracting RAW data"):
        input_dir = root  # Use the directory containing the .tar file
        extract_command = f"arcsiextractdata.py -i {input_dir} -o {output_dir}"
        subprocess.run(extract_command, shell=True, stdout=subprocess.DEVNULL)
        '''tqdm.write(f"Extracted data from {input_dir} to {output_dir}")'''  # Terminal output


# Execute script
if __name__ == "__main__":
    # Define directories
    raw_directory = "landsat/RAW"
    temp_directory = "landsat/tmp"
    # Call functions
    extract_landsat_data(raw_directory, temp_directory)
