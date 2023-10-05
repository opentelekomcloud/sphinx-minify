import os
from rjsmin import jsmin
from rcssmin import cssmin
from htmlmin import minify as htmlmin
import logging

# Function to minify JavaScript and CSS based on file extension
def minify_file(input_file):
    try:
        with open(input_file, 'r') as file:
            file_contents = file.read()
    except UnicodeDecodeError as e:
        logging.warning(f"File {input_file} is not a text file!")
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
        logging.warning(f"Unable to minify {input_file}")
        return

    return minified_contents

# Function to recursively traverse a directory and minify files
def minify_directory(input_directory, output_directory):
    for root, _, files in os.walk(input_directory):
        for singlefile in files:
            if ".min" in singlefile:
                continue
            input_file = os.path.join(root, singlefile)
            relative_path = os.path.relpath(input_file, input_directory)
            output_file = os.path.join(output_directory, relative_path)
            
            # Ensure the output directory structure exists
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            output = minify_file(input_file)
            if output:
                with open(output_file, 'w') as file:
                    file.write(output)

def main():
    input_directory = "doc/build/html_copy"
    output_directory = "doc/build/html_copy/out"
    logging.info("Starting to minify all output files...")
    minify_directory(input_directory, output_directory)

main()