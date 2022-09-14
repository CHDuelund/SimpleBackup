import os, shutil, re, glob, filecmp

folder1 = "c:\\temp\\test\\src"
get_folder1_root = re.split(r'\\', folder1)
folder1_root = get_folder1_root[-1]
folder2 = "c:\\temp\\test\\dst\\backup"
get_folder2_root = re.split(r'\\', folder2)
folder2_root = get_folder2_root[-1]
latest_backup = "C:\\Temp\\Test\\dst\\src_full_14_09_2022_23_38_45"

for dir1 in glob.glob(folder1 + "\\**\\*", recursive=True):
    if os.path.isdir(dir1):
        crop_folder = dir1.split(folder1_root ,1)[1]
        os.makedirs(folder2 + crop_folder, exist_ok=True)

for file in glob.glob(folder1 + "\\**\\*", recursive=True):
    if os.path.isfile(file):
        crop_file = file.split(folder1_root, 1)[1]
        no_changes = filecmp.cmp(file, latest_backup + crop_file, shallow=True)
        if no_changes == False:
            shutil.copy2(file, folder2 + crop_file)

for dir2 in glob.glob(folder2 + "\\**\\*", recursive=True):
    if os.path.isdir(dir2):
        crop_folder = dir2.split(folder2_root ,1)[1]
        shutil.rmtree(folder2 + crop_folder, ignore_errors=True)

if len(os.listdir(folder2)) == 0:
    shutil.rmtree(folder2)
    print("No files were backed up.")