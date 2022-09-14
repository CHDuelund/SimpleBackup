import os, shutil, re
from difflib import SequenceMatcher

source = "c:\\temp\\test\\src"
destination = "C:\\Temp\\Test\\dst\\src_full_14_09_2022_14_38_25"
backup = "C:\\Temp\\Test\\dst\\test5\\"

files_source = []

for root, dirnames, filenames in os.walk(source):
    for filename in filenames:
        files_source.append(os.path.join(root, filename))

files_destination = []

for root, dirnames, filenames in os.walk(destination):
    for filename in filenames:
        files_destination.append(os.path.join(root, filename))

# empty list for matching results
matched_files = []

# iterate over the files in the first folder
for file_one in files_source:
    # read file content
    with open(file_one, "r") as f:
        file_one_text = f.read()

    # iterate over the files in the second folder
    for file_two in files_destination:
        # read file content
        with open(file_two, "r") as f:
            file_two_text = f.read()

            # match the two file contents
            match = SequenceMatcher(None, file_one_text, file_two_text)
            if match.ratio() < 1.0:
                print(f"Changes found ({match.ratio()}): '{file_one}' | '{file_two}'")
                # here you have to decide if you rather want to remove files from the first or second folder
                matched_files.append(file_one)  # i delete files from the second folder

#split_source_path = re.split(r'\\',source)
#root_folder_name = split_source_path[-1]

for src_file in matched_files:
    split_source_path = re.split(r'\\', src_file)
    file_path = split_source_path[:-1]
    print(file_path)
    #file_path = src_file.split(root_folder_name,1)
    #print(file_path[0])
    #shutil.copytree(src_file, backup)

