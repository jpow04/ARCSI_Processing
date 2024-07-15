import os
import glob
import tempfile
import subprocess

# function that merges all tif files within a directory
def merge_tif_files(input_dir, output_dir, output_filename):
    # Check directories
    if not os.path.exists(input_dir):
        print(f"Directory {input_dir} does not exist.")
        return
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory {output_dir}")

    # Construct the output file path
    output_filepath = os.path.join(output_dir, output_filename)

    # List all .tif files in the input directory
    tif_files = glob.glob(os.path.join(input_dir, '*.tif'))
    if not tif_files:  # Check input directory for .tif files
        print(f"No .tif files found in {input_dir}")
        return

    # Create a temporary file to hold the list of .tif files
    with tempfile.NamedTemporaryFile(delete=False, mode='w') as tmpfile:
        tmpfile_name = tmpfile.name
        for tif_file in tif_files:
            tmpfile.write(tif_file + '\n')

    # Prepare the gdal_merge.py command
    cmd = f'gdal_merge -o {output_filepath} --optfile {tmpfile_name}'

    # Execute the command
    subprocess.call(cmd, shell=True)

    # Clean up the temporary file
    os.remove(tmpfile_name)

    print(f"Merged .tif files into: {output_filepath}")


# Execute script
if __name__ == "__main__":
    # Define directories
    input_directory = "landsat/dem"
    output_directory = "landsat/Data"
    merged_filename = "aotea_dem.tif"
    # Call functions
    merge_tif_files(input_directory, output_directory, merged_filename)
