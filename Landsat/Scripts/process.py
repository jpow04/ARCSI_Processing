import time
from extract import extract_landsat_data
from aoi_clip import batch_clip
from build_batch import batch_parameters
from translate import postprocess
from file_sort import organize_output_folders
from directory_clear import clear_directory
from directory_clear import remove_directory
from check_data import remove_null_data
from check_data import log_file_errors

# Function that calls to all scripts for complete processing of Landsat data
def prepare_landsat_data():
    start_time = time.time()  # Start time
    print('Preparing landsat data | Extracting...')
    extract_landsat_data(raw_base_directory, temp_directory)  # Extract Landsat data to temp directory (extract.py)
    print("File extraction complete | Clipping to aoi...")
    batch_clip(temp_directory, input_directory, shapefile_path)  # Clip Landsat data (aoi_clip.py)
    clear_directory(temp_directory)  # Clear temp directory (directory_clear.py)
    print("Aoi clip complete | Building batch command...")
    batch_parameters(output_directory, dem_directory, temp_directory, input_directory, command_name)  # Process data with ARCSI (build_batch.py)
    print(f"Processing complete | Postprocessing...")
    remove_directory(temp_directory)  # Remove temp directory (directory_clear.py)
    remove_directory(input_directory)  # Remove input directory (directory_clear.py)
    log_file_errors(output_directory, log_directory, expected_products)  # Log unprocessed files (check_data.py)
    remove_null_data(output_directory, expected_products)  # Clear bad data (check_data.py)
    postprocess(output_directory)  # Covert .kea to GeoTIFF then remove .kea (translate.py)
    organize_output_folders(output_directory)  # Sort files by date (file_sort.py)
    print(f"Processed files located in {output_directory}")
    end_time = time.time()  # End time
    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    elapsed_time_minutes = elapsed_time / 60
    print(f"Total processing time: {elapsed_time:.2f} seconds ({elapsed_time_minutes:.2f} minutes)")


# Execute script
if __name__ == "__main__":
    # Define directories
    raw_base_directory = "landsat/RAW"
    temp_directory = "landsat/tmp"
    input_directory = "landsat/Inputs"
    output_directory = "landsat/Outputs"
    shapefile_path = "landsat/Data/aotea_landsat_aoi"
    dem_directory = "landsat/Data/aotea_dem.tif"
    command_name = "LSARCSI.sh"
    log_directory = "landsat/Log"
    expected_products = 5
    # Call functions
    prepare_landsat_data()
