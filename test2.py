import os, shutil, re, glob, filecmp

folder1 = "c:\\temp\\test\\src" # source mappen
get_folder1_root = re.split(r'\\', folder1) # stien til source mappen opdeles
folder1_root = get_folder1_root[-1] # mappenavnet på roden til source hives
folder2 = "c:\\temp\\test\\dst\\backup" # den mappe hvor backup filer kopieres til
get_folder2_root = re.split(r'\\', folder2) # stien til backup mappen opdeles
folder2_root = get_folder2_root[-1] # mappenavnet på roden til backup mappen hives
latest_backup = "C:\\Temp\\Test\\dst\\src_full_14_09_2022_23_38_45" # den mappe hvor seneste full backup ligger

for dir1 in glob.glob(folder1 + "\\**\\*", recursive=True): # loop som bruger glob til at rende alle stier igennem i source mappen
    if os.path.isdir(dir1): # kontrollerer om stien er en mappe
        crop_folder = dir1.split(folder1_root ,1)[1] # hiver stien efter mappenavnet for roden til source
        os.makedirs(folder2 + crop_folder, exist_ok=True) # opretter en mappe i backup mappen, magen til source

for file in glob.glob(folder1 + "\\**\\*", recursive=True): # endnu et loop som bruger glob til at rende alle stier igennem i source mappen
    if os.path.isfile(file): # kontrollerer om stien er en fil
        crop_file = file.split(folder1_root, 1)[1] # hiver stien efter mappenavnet for roden til source
        no_changes = filecmp.cmp(file, latest_backup + crop_file, shallow=True) # sammenligner filer fra source og seneste full backup
        if no_changes == False: # hvis filerne ikke er identiske...
            shutil.copy2(file, folder2 + crop_file) # kopierer filen fra source til backup mappen

for dir2 in glob.glob(folder2 + "\\**\\*", recursive=True): # loop som bruger glob til at rende alle stier igennem i backup mappen
    if os.path.isdir(dir2): # kontrollerer om stien er en mappe
        shutil.rmtree(dir2, ignore_errors=True) # sletter tomme mapper

if len(os.listdir(folder2)) == 0: # hvis backup mappen er tom...
    shutil.rmtree(folder2) # slet backup mappen
    print("No files were backed up.")