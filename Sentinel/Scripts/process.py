import time
from aoi_clip import process_safe_folders
from build_batch import batch_parameters
from translate import postprocess
from file_sort import organize_output_folders
from directory_clear import remove_directory
from check_data import remove_null_data
from check_data import log_file_errors
from file_sort import organize_xml_files

# Function that calls to all scripts for complete processing of Sentinel data
def prepare_sentinel_data():
    start_time = time.time()  # Start time
    print("Preparing Sentinel data | Clipping to aoi...")
    process_safe_folders(raw_base_directory, input_directory, shapefile_path)  # Clip Sentinel data (aoi_clip.py)
    print("Aoi clip complete | Building batch command...")
    batch_parameters(output_directory, dem_directory, temp_directory, input_directory, command_name)  # Process data with ARCSI (build_batch.py)
    print(f"Processing complete | Postprocessing...")
    remove_directory(temp_directory)  # Remove temp directory (directory_clear.py)
    remove_directory(input_directory)  # Remove input directory (directory_clear.py)
    log_file_errors(output_directory, log_directory, expected_products)  # Log unprocessed files (check_data.py)
    remove_null_data(output_directory, expected_products)  # Clear bad data (check_data.py)
    postprocess(output_directory)  # Covert .kea to GeoTIFF then remove .kea (translate.py)
    organize_xml_files(output_directory)  # Sorts .xml files into directory for organization (file_sort.py)
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
    raw_base_directory = "sentinel/RAW"
    temp_directory = "sentinel/tmp"
    input_directory = "sentinel/Inputs"
    output_directory = "sentinel/Outputs"
    shapefile_path = "sentinel/Data/aotea_sentinel_aoi"
    dem_directory = "sentinel/Data/aotea_dem.tif"
    command_name = "S2ARCSI.sh"
    log_directory = "sentinel/Log"
    expected_products = 9
    # Call functions
    prepare_sentinel_data()
