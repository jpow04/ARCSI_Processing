import os
import shutil
from tqdm import tqdm

# Function to check output folders for correctly processed data by the amount of files in the respective folder
def log_file_errors(input_dir, log_dir, product_num):
    log_entries = []
    # Check if the directory exists
    if not os.path.exists(input_dir):
        print(f"Directory {input_dir} does not exist.")
        return
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Get all subdirectories in the output directory
    products = [os.path.join(input_dir, d) for d in os.listdir(input_dir) if
                os.path.isdir(os.path.join(input_dir, d))]

    # Initialize tqdm progress bar for subdirectories
    with tqdm(total=len(products), desc="Checking products") as pbar:
        for product in products:
            # Get the list of files in the subdirectory
            files = os.listdir(product)

            # Check if the number of files is not equal to expected products
            if len(files) != product_num:
                log_entries.append(f"{product} did not produce {product_num} products, check corresponding RAW file.")
                log_file = os.path.join(log_dir, f"product_errors.txt")
                if log_entries:
                    with open(log_file, 'w') as log:
                        for entry in log_entries:
                            log.write(entry + "\n")

            pbar.update(1)  # Update the progress bar after processing each subdirectory

# Function to check output folders for correctly processed data by the amount of files in the respective folder
def remove_null_data(input_dir, product_num):
    # Check if the directory exists
    if not os.path.exists(input_dir):
        print(f"Directory {input_dir} does not exist.")
        return

    # Get all subdirectories in the output directory
    products = [os.path.join(input_dir, d) for d in os.listdir(input_dir) if
                os.path.isdir(os.path.join(input_dir, d))]

    # Initialize tqdm progress bar for subdirectories
    with tqdm(total=len(products), desc="Removing unprocessed data") as pbar:
        for product in products:
            # Get the list of files in the subdirectory
            files = os.listdir(product)

            # Check if the number of files is not equal to expected products
            if len(files) != product_num:
                try:
                    # Remove the subdirectory if it does not have exactly 5 files
                    shutil.rmtree(product)
                    '''tqdm.write(f"Removed folder: {subdirectory}")'''  # Terminal output

                except Exception as e:  # Report errors
                    tqdm.write(f"Failed to remove folder {product}: {e}")

            pbar.update(1)  # Update the progress bar after processing each subdirectory


# Execute script
if __name__ == "__main__":
    # Define directories
    output_directory = "landsat/Outputs"
    log_directory = "landsat/Log"
    expected_products = 9
    # Call functions
    log_file_errors(output_directory, log_directory, expected_products)
    remove_null_data(output_directory, expected_products)
