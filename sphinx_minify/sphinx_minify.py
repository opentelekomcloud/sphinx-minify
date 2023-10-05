import os
from rjsmin import jsmin
from rcssmin import cssmin
from htmlmin import minify as htmlmin
import logging
from multiprocessing import Pool
import shutil

# Function to minify JavaScript, CSS and HTML based on file extension
def minify_file(input_file, output_file):
    try:
        with open(input_file, 'r') as file:
            file_contents = file.read()
    except UnicodeDecodeError as e:
        logging.debug(f"File {input_file} is not a text file! Copying without modification.")
        shutil.copy2(input_file, output_file)
        return

    if input_file.endswith('.js'):
        minified_contents = jsmin(file_contents)
    elif input_file.endswith('.css'):
        minified_contents = cssmin(file_contents)
    elif input_file.endswith('.html'):
        minified_contents = htmlmin(
            file_contents,
            remove_comments=True,
            remove_empty_space=True
        )
    else:
        logging.debug(f"Unable to minify {input_file}. Copying without modification.")
        shutil.copy2(input_file, output_file)
        return

    with open(output_file, 'w') as file:
        file.write(minified_contents)

# Function to process a single file and create the output file path
def process_file(input_file, input_directory, output_directory):
    relative_path = os.path.relpath(input_file, input_directory)
    output_file = os.path.join(output_directory, relative_path)
    
    # Ensure the directory structure for the output file exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    minify_file(input_file, output_file)

# Function to recursively traverse a directory and minify files using multiprocessing
def minify_directory(input_directory, output_directory, num_processes):
    file_list = []
    for root, _, files in os.walk(input_directory):
        for singlefile in files:
            input_file = os.path.join(root, singlefile)
            file_list.append(input_file)

    # Create a multiprocessing pool
    with Pool(processes=num_processes) as pool:
        # Create processes
        # A list will be created for the processes containing 
        # all the required arguments for the function in tripplets
        trippletlist = [(input_file, input_directory, output_directory) for input_file in file_list]
        pool.starmap(process_file, trippletlist)

def main():
    input_directory = "doc/build/html_copy"
    output_directory = "doc/build/html_copy/out"
    num_processes = 4
    logging.info("Starting to minify all output files...")
    minify_directory(input_directory, output_directory, num_processes)

main()