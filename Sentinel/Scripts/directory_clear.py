import os
import shutil
from tqdm import tqdm

# Function that clears directory contents
def clear_directory(input_dir):
    # Check if the directory exists
    if not os.path.exists(input_dir):
        print(f"Directory {input_dir} does not exist.")
        return

    # Iterate over all files and subdirectories within the temp directory
    for item in tqdm(os.listdir(input_dir), desc=f"Clearing {input_dir}"):
        item_path = os.path.join(input_dir, item)
        try:
            # Clear directories
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
                '''tqdm.write(f"Removed directory: {item_path}")'''  # Terminal output

            # Clear files
            elif os.path.isfile(item_path):
                os.remove(item_path)
                '''tqdm.write(f"Removed file: {item_path}")'''  # Terminal output

        except Exception as e:  # Report errors
            tqdm.write(f"Failed to remove {item_path}: {e}")

# Function that removes directory entirely
def remove_directory(input_dir):
    # Check if the directory exists
    if not os.path.exists(input_dir):
        print(f"Directory {input_dir} does not exist.")
        return
    try:
        shutil.rmtree(input_dir)  # Remove directory
        '''tqdm.write(f"Removed: {input_dir}")'''  # Terminal output

    except Exception as e:  # Report errors
        tqdm.write(f"Failed to remove {input_dir}: {e}")


# Execute script
if __name__ == "__main__":
    # Define directories
    directory = "Sentinel/tmp"
    # Call functions
    clear_directory(directory)
