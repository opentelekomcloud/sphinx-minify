import os
from rjsmin import jsmin
from rcssmin import cssmin
from htmlmin import minify as htmlmin
import logging

# Function to minify JavaScript and CSS based on file extension
def minify_file(input_file, output_file):
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

    with open(output_file, 'w') as file:
        file.write(minified_contents)

# Function to recursively traverse a directory and minify files
def minify_directory(directory):
    for root, _, files in os.walk(directory):
        for singlefile in files:
            if ".min" in singlefile:
                continue
            print(singlefile)
            input_file = os.path.join(root, singlefile)
            output_file = (
                os.path.splitext(input_file)[0]
                + ".min"
                + os.path.splitext(input_file)[1]
            )
            minify_file(input_file, output_file)

def main():
    directory_to_minify = "doc/build/html_copy"  # Replace with the target directory path
    minify_directory(directory_to_minify)

main()