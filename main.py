# This program was created with Python 3.10
# This program is a research project on detecting plagiarism in pdf files
# Author: Ben Fisher (bsfisher@ualberta.ca)
# Date Created: January 21, 2023.
# Date Last Modified: January 21, 2023
# Parts of this program are referenced from pdfminer.six documentation

import os
import sys
from pdfminer.high_level import extract_text
from gst import match


# # set minimum pattern match
minimum_match = 20


def main():

    # Load inputted directory path
    directoryPath = format_path(sys.argv[1])

    # Load pdf files and extract their text
    files = [doc for doc in absolute_file_paths(directoryPath) if doc.endswith('.pdf')]
    content = []
    for File in files:
        content.append(extract_text(File).replace('\n', ' '))

    # Compare the content of the pdf files together
    compare_files(files, content)

    return


def format_path(path):
    # Formats string given to fit the file-naming standards of the running operating system
    if sys.platform == "linux":
        path = path.replace("\\", "/")
    elif sys.platform == "win32":
        path = path.replace("/", "\\")

    return path


def absolute_file_paths(directory):
    # Returns a list containing the root filepath for all files in the given directory
    filenames = []
    for root, dirs, files in os.walk(os.path.abspath(directory)):
        for file in files:
            filenames.append(os.path.join(root, file))
    return filenames


def compare_files(files, content):
    # Compares the given content and stores the file information in a list
    for comparison_content in content:
        for n_comparisons in range(content.index(comparison_content)+1, len(content)):
            # Find all matches between the two pdfs
            matched = match(comparison_content, '', content[n_comparisons], '', minimum_match)

            # print(matched)
            for i in matched:
                print(files[content.index(comparison_content)] + "vs." + files[n_comparisons])
                print("Matches Found:" + str(len(matched)))
                print(files[content.index(comparison_content)] + ':' + comparison_content[i[0]: i[0]+i[2]] + '')
                print(files[n_comparisons] + '_' + content[n_comparisons][i[1]: i[1] + i[2]] + '_')
                print('\n\n')
    return

main()

