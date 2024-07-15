import os
import subprocess

# Function that builds arcsi batch processing command from parameters
def build_batch_command(params):
    # Construct the command from parameters
    command = (f"arcsibuildcmdslist.py -s {params['s']} -f {params['f']} {'--stats' if params['stats'] else ''} "
               f"-p {' '.join(params['p'])} --outpath {params['outpath']} --dem {params['dem']} "
               f"--demnodata {params['demnodata']} --cloudmethods {params['cloudmethods']} "
               f"{'--fullimgouts' if params['fullimgouts'] else ''} "
               f"--keepfileends {' '.join(params['keepfileends'])} --tmpath {params['tmpath']} "
               f"-i {params['i']} -e \"{params['e']}\" -o {params['o']}")

    # Print the constructed command (optional, for debugging)
    print(f"Constructed command: {command}")

    # Execute the command in the terminal
    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL)

# Function that defines arcsi parameters and runs batch script
def batch_parameters(output_dir, dem_dir, temp_dir, input_dir, batch_process):
    # Check directories
    if not os.path.exists(input_dir):
        print(f"Directory {input_dir} does not exist.")
        return
    if not os.path.exists(dem_dir):
        print(f"Directory {dem_dir} does not exist.")
        return
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory {output_dir}")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
        print(f"Created directory {temp_dir}")

    # Define the parameters
    parameters = {
        's': 'LANDSAT',  # Satellite type
        'f': 'KEA',  # Data format type
        'stats': True,  # Stats flag
        'p': ['CLOUDS', 'DOSAOTSGL', 'STDSREF', 'SATURATE', 'TOPOSHADOW', 'METADATA'],  # Processing options
        'outpath': output_dir,  # Output directory
        'dem': dem_dir,  # DEM directory
        'demnodata': -99.0,  # No data value for dem
        'cloudmethods': 'LSMSK',  # Cloud mask method
        'fullimgouts': True,  # Include full image outputs flag
        'keepfileends': ['meta.json', 'stdsref.kea'],  # File endings to keep
        'tmpath': temp_dir,  # Temp directory
        'i': input_dir,  # Input directory
        'e': '*MTL.txt',  # Metadata file to search for
        'o': batch_process  # Batch command name
    }

    build_batch_command(parameters)  # Construct batch processing command
    cpu_count = os.cpu_count()  # Check available processing power
    cores = cpu_count  # Amount of cores to be used in processing

    # Batch command run sequence
    while True:
        user_input = True, '''input("Do you want to proceed with processing? (Y/N): ").strip().upper()'''  # Request user input
        if user_input:  # user_input == 'Y':
            batch_command = f'parallel -j {cores} < {batch_process}'  # Allocates processing power to ARCSI
            print(f"Executing: {batch_command}")  # Print batch command to terminal
            print(f"Batch processing landsat data using {cores} cores")
            subprocess.run(batch_command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            break
        '''elif user_input == 'N':
            print("Processing aborted by the user.")
            break
        else:
            print("Invalid input. Please enter 'Y' to proceed or 'N' to abort.")'''


# Execute script
if __name__ == "__main__":
    # Define directories
    output_directory = "landsat/Outputs"
    dem_directory = "landsat/Data/aotea_dem.tif"
    temp_directory = "landsat/tmp"
    input_directory = "landsat/Inputs"
    command_name = "LSARCSIC.sh"
    # Call functions
    batch_parameters(output_directory, dem_directory, temp_directory, input_directory, command_name)
