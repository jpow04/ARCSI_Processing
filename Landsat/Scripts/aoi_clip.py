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

# Function to clip all rasters, Landsat file format
def batch_clip(input_dir, output_dir, shapefile):
    # Check directories
    if not os.path.exists(input_dir):
        print(f"Directory {input_dir} does not exist.")
        return
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory {output_dir}")

    # Collect all files to be processed
    files_to_process = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            files_to_process.append((root, file))

    # Set filepaths
    for root, file in tqdm(files_to_process, desc="Clipping raster files"):
        relative_path = os.path.relpath(root, input_dir)
        output_folder = os.path.join(output_dir, relative_path)

        # Check for and create output folders in output directory
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        input_filepath = os.path.join(root, file)
        output_filepath = os.path.join(output_folder, file)

        if file.endswith('.TIF'):  # Landsat raster files are in GeoTIFF format
            clip_raster(input_filepath, output_filepath, shapefile)
        else:
            # Copy non-raster files as they are
            shutil.copy(input_filepath, output_filepath)


# Execute script
if __name__ == "__main__":
    # Define directories
    temp_directory = "landsat/tmp"
    input_directory = "landsat/Inputs"
    shapefile_path = "landsat/Data/aotea_landsat_aoi"
    print("Clipping raster files")
    # Call functions
    batch_clip(temp_directory, input_directory, shapefile_path)
