import os
import shutil
from tqdm import tqdm

# Function to check output folders for correctly processed data by the amount of files in the respective folder
def remove_null_data(output_dir):
    # Check if the directory exists
    if not os.path.exists(output_dir):
        print(f"Directory {output_dir} does not exist.")
        return

    # Get all subdirectories in the output directory
    subdirectories = [os.path.join(output_dir, d) for d in os.listdir(output_dir) if
                      os.path.isdir(os.path.join(output_dir, d))]

    # Initialize tqdm progress bar for subdirectories
    with tqdm(total=len(subdirectories), desc="Checking folders") as pbar:
        for subdirectory in subdirectories:
            # Get the list of files in the subdirectory
            files = os.listdir(subdirectory)

            # Check if the number of files is not equal to expected products
            if len(files) != 5:  # Expect 5 products to be generated
                try:
                    # Remove the subdirectory if it does not have exactly 5 files
                    shutil.rmtree(subdirectory)
                    '''tqdm.write(f"Removed folder: {subdirectory}")'''  # Terminal output

                except Exception as e:  # Report errors
                    tqdm.write(f"Failed to remove folder {subdirectory}: {e}")

            pbar.update(1)  # Update the progress bar after processing each subdirectory


# Execute script
if __name__ == "__main__":
    # Define directories
    output_directory = "sentinel/Outputs"
    # Call functions
    remove_null_data(output_directory)
