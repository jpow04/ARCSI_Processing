import os
import shutil
import rasterio
from tqdm import tqdm
import geopandas as gpd
from rasterio.mask import mask

# Function to clip raster to specified shape
def clip_raster(input_filepath, output_filepath, shapefile):
    # Read the shapefile using geopandas
    shapes = gpd.read_file(shapefile)

    # Convert the shapes to GeoJSON format
    geoms = shapes.geometry.values

    with rasterio.open(input_filepath) as src:
        # Clip the raster using the shapefile
        out_image, out_transform = mask(src, geoms, crop=True)

        # Update the metadata with the new dimensions, transform, and CRS
        out_meta = src.meta.copy()
        out_meta.update({
            "driver": "GTiff",
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform,
            "crs": src.crs
        })

        # Write the clipped raster to the output file
        with rasterio.open(output_filepath, "w", **out_meta) as dest:
            dest.write(out_image)

    '''tqdm.write(f"Clipped file: {input_filepath} to {output_filepath}")'''  # Terminal output

# Function to process .SAFE folders, Sentinel file format
def process_safe_folders(input_dir, output_dir, shapefile):
    # Check directories
    if not os.path.exists(input_dir):
        print(f"Directory {input_dir} does not exist.")
        return
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory {output_dir}")

    # Collect all .SAFE files in subdirectories
    safe_files = []
    for root, dirs, files in os.walk(input_dir):
        for dir_name in dirs:
            if dir_name.endswith('.SAFE'):
                safe_files.append((root, dir_name))

    # Set filepaths
    for root, dir_name in tqdm(safe_files, desc="Clipping raster files"):
        input_filepath = os.path.join(root, dir_name)
        output_filepath = os.path.join(output_dir, dir_name)

        # Copy the .SAFE folder structure to the input directory
        if not os.path.exists(output_filepath):
            shutil.copytree(input_filepath, output_filepath, dirs_exist_ok=True)

        # Find and clip all raster files within the .SAFE folder
        for subdir, _, subfiles in os.walk(output_filepath):
            for file in subfiles:
                if file.endswith('.jp2'):  # Sentinel-2 raster files are in JP2 format
                    src_file_path = os.path.join(input_filepath, os.path.relpath(subdir, output_filepath), file)
                    dest_file_path = os.path.join(subdir, file)
                    clip_raster(src_file_path, dest_file_path, shapefile)

        '''tqdm.write(f"Clipped and moved {input_filepath} to {output_filepath}")'''  # Terminal output


# Execute script
if __name__ == "__main__":
    # Define directories and shapefile path
    raw_directory = "sentinel/RAW"
    input_directory = "sentinel/Inputs"
    shapefile_path = "sentinel/Data/aotea_sentinel_aoi"
    # Call functions
    process_safe_folders(raw_directory, input_directory, shapefile_path)
