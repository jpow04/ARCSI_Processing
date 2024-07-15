import os
import re
import subprocess
from tqdm import tqdm

# Function to translate .kea files to .tif files
def convert_kea_to_geotiff(input_dir):
    # Check if the input directory exists
    if not os.path.exists(input_dir):
        print(f"Directory {input_dir} does not exist.")
        return

    # Get all subdirectories in the input directory
    subdirectories = [os.path.join(input_dir, d) for d in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, d))]

    # Initialize tqdm progress bar for subdirectories
    with tqdm(total=len(subdirectories), desc="Translating to GeoTIFF") as pbar:
        for subdirectory in subdirectories:
            for root, dirs, files in os.walk(subdirectory):
                kea_files = [file for file in files if file.endswith('.kea')]

                # Convert each .kea file to .tif
                for kea_file in kea_files:
                    kea_path = os.path.join(root, kea_file)
                    tiff_path = os.path.join(root, kea_file.replace('.kea', '.tif'))

                    try:
                        # Run gdal_translate command
                        subprocess.run(['gdal_translate', '-of', 'GTiff', kea_path, tiff_path], check=True, stdout=subprocess.DEVNULL)
                        '''tqdm.write(f"Successfully converted {kea_file} to {tiff_path}")'''  # Terminal output

                    except subprocess.CalledProcessError as e:  # Report errors
                        tqdm.write(f"Failed to convert {kea_file}: {e}")

                pbar.update(1)  # Update the progress bar after processing each subdirectory

# Function to remove .kea files after translation to GeoTIFF
def remove_kea_files(input_dir):
    # Check if the directory exists
    if not os.path.exists(input_dir):
        print(f"Directory {input_dir} does not exist.")
        return
    pattern = re.compile(r'SEN2.*kea')  # Searches for .kea files in Sentinel format

    # Get all subdirectories in the input directory
    subdirectories = [os.path.join(input_dir, d) for d in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, d))]

    # Initialize tqdm progress bar for subdirectories
    with tqdm(total=len(subdirectories), desc="Removing .kea files") as pbar:
        for subdirectory in subdirectories:
            for root, dirs, files in os.walk(subdirectory):
                for file in files:
                    match = pattern.match(file)
                    if match:
                        kea_path = os.path.join(root, file)
                        try:
                            os.remove(kea_path)
                            '''tqdm.write(f"File '{kea_path}' deleted successfully.")'''  # Terminal output

                        except Exception as e:  # Report errors
                            tqdm.write(f"Failed to remove {kea_path}: {e}")

                pbar.update(1)  # Update the progress bar after processing each subdirectory

def postprocess(input_dir):
    convert_kea_to_geotiff(input_dir)
    remove_kea_files(input_dir)


# Execute script
if __name__ == "__main__":
    # Define directories
    input_directory = "sentinel/Outputs"
    # Call functions
    convert_kea_to_geotiff(input_directory)
    remove_kea_files(input_directory)
