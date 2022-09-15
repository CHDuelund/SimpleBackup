# IMPORTERING AF PAKKER

import os, shutil, re, glob, filecmp, csv
from termcolor import colored
from datetime import date,datetime


# GLOBALE VARIABLER

get_today = date.today() # hent dato til variabel.
date_today = get_today.strftime("%d-%m-%Y")
date_stamp = get_today.strftime("_%d_%m_%Y") # konverter dato til ønsket format.
source_path = ""


# DEFINERING AF FUNKTIONER

def Main_Menu():
    print(colored("Simple Backup by CHDuelund v1.0a\n", "blue", attrs=["bold", "underline"]))

    print(colored("Choose function:", attrs=["underline"]))
    print("1 = Full Backup\n2 = Differential Backup\n3 = Exit\n")

    while (True):
        function = input("Enter your choice: ")
        if function == "1":
            Clear_Console()
            Full_Backup()
            break
        elif function == "2":
            Clear_Console()
            Differential_Backup()
            break
        elif function == "3":
            Clear_Console()
            exit()
        else:
            print(colored("Invalid input - please try again...\n", "red"))


def Full_Backup():
    print(colored("\nFull Backup\n", "blue", attrs=["bold", "underline"]))

    while(True):
        source_path = input("Specify the source path: ")
        folder_exists = os.path.exists(source_path) # kontrollerer om den angivne sti findes.
        folder_name = re.split(r'\\',source_path) # deler variablen source_path op ved brug af regex med \ som "delimiter".
        if folder_exists == True:
            break
        else:
            print(colored("The path does not exist - please try again...\n", "red"))

    while (True):
        destination_path = input("Specify the destination path: ")
        if destination_path[-1] != "\\":
            destination_path = destination_path + "\\" # tilføjer en \ til enden af den angivne sti, hvis den mangler.
        folder_exists = os.path.exists(destination_path)  # kontrollerer om den angivne sti findes.

        if folder_exists == True:
            get_time = datetime.now()  # hent tid til variabel.
            time_stamp = get_time.strftime("_%H_%M_%S")  # konverter tid til ønsket format.
            time_now = get_time.strftime("_%H:%M:%S")

            new_folder_path = destination_path + folder_name[-1] + "_full" + date_stamp + time_stamp

            shutil.copytree(source_path, new_folder_path)

            log_data = [source_path, destination_path + folder_name[-1] + "_full" + date_stamp + time_stamp, "full", date_today + time_now]
            with open('backup_log.csv', 'a', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(log_data)

            print(colored("\nBackup done!\n", "green"))

            while(True):
                return_main_menu = input("Return to main menu? (y/n): ")
                if return_main_menu == "y":
                    Clear_Console()
                    break
                elif return_main_menu =="n":
                    Clear_Console()
                    exit()
                else:
                    print(colored("Invalid input - please try again...\n", "red"))

            break

        else:
            print(colored("The path does not exist - please try again...\n", "red"))


def Differential_Backup():
    print(colored("\nDifferential Backup\n", "blue", attrs=["bold", "underline"]))

    while (True):
        global source_path
        source_path = input("Specify the source path: ")
        folder_exists = os.path.exists(source_path)  # kontrollerer om den angivne sti findes.
        folder_name = re.split(r'\\',source_path)  # deler variablen source_path op ved brug af regex med \ som "delimiter".
        if folder_exists == True:

            break
        else:
            print(colored("The path does not exist - please try again...\n", "red"))

    full_backup_exists = 0
    with open('backup_log.csv') as csv_file:
        for data in csv.DictReader(csv_file):
            if data['type'] == "full" and data['src-path'] == source_path:
                full_backup_exists = 1
                break

    if full_backup_exists == 1:
        while (True):
            destination_path = input("Specify the destination path: ")
            folder_exists = os.path.exists(destination_path)  # kontrollerer om den angivne sti findes.

            if folder_exists == True:
                get_time = datetime.now()  # hent tid til variabel.
                time_stamp = get_time.strftime("_%H_%M_%S")  # konverter tid til ønsket format.
                time_now = get_time.strftime("_%H:%M:%S")

                backup_folder_path = destination_path + "\\" + folder_name[-1] + "_diff" + date_stamp + time_stamp

                latest_full = Latest_Full()

                os.mkdir(backup_folder_path)

                for dir1 in glob.glob(source_path + "\\**\\*", recursive=True):  # loop som bruger glob til at rende alle stier igennem i source mappen
                    if os.path.isdir(dir1):  # kontrollerer om stien er en mappe
                        crop_folder = dir1.split(folder_name[-1], 1)[1]  # hiver stien efter mappenavnet for roden til source
                        os.makedirs(backup_folder_path + crop_folder, exist_ok=True)  # opretter en mappe i backup mappen, magen til source

                for file in glob.glob(source_path + "\\**\\*", recursive=True):  # endnu et loop som bruger glob til at rende alle stier igennem i source mappen
                    if os.path.isfile(file):  # kontrollerer om stien er en fil
                        crop_file = file.split(folder_name[-1], 1)[1]  # hiver stien efter mappenavnet for roden til source
                        if os.path.isfile(latest_full + crop_file):  # hvis filen eksisterer i seneste full backup...
                            no_changes = filecmp.cmp(file, latest_full + crop_file, shallow=True)  # sammenligner filer fra source og seneste full backup
                            if no_changes == False:  # hvis filerne ikke er identiske...
                                shutil.copy2(file, backup_folder_path + crop_file)  # kopierer filen fra source til backup mappen
                        else:
                            shutil.copy2(file, backup_folder_path + crop_file)  # kopierer filen fra source til backup mappen hvis den ikke findes i seneste full backup

                backup_dirs = []
                for dir2 in glob.glob(backup_folder_path + "\\**\\*", recursive=True):  # loop som bruger glob til at rende alle stier igennem i backup mappen
                    if os.path.isdir(dir2):  # kontrollerer om stien er en mappe
                        backup_dirs.append(dir2)
                for reverse_dir in backup_dirs[::-1]:
                    if len(os.listdir(reverse_dir)) == 0:  # hvis backup mappen er tom...
                        shutil.rmtree(reverse_dir)  # slet backup mappen

                if len(os.listdir(backup_folder_path)) == 0:  # hvis backup mappen er tom...
                    shutil.rmtree(backup_folder_path)  # slet backup mappen
                    print(colored("\nJob done. No files were backed up.\n", "green"))
                else:
                    print(colored("\nBackup done!\n", "green"))

                log_data = [source_path, destination_path + folder_name[-1] + "_diff" + date_stamp + time_stamp, "differential", date_today + time_now]
                with open('backup_log.csv', 'a', encoding='UTF8') as f:
                    writer = csv.writer(f)
                    writer.writerow(log_data)

                while (True):
                    return_main_menu = input("Return to main menu? (y/n): ")
                    if return_main_menu == "y":
                        Clear_Console()
                        break
                    elif return_main_menu == "n":
                        Clear_Console()
                        exit()
                    else:
                        print(colored("Invalid input - please try again...\n", "red"))
                break
            else:
                print(colored("The path does not exist - please try again...\n", "red"))
    else:
        while (True):
            return_main_menu = input(
                "No Full Backups detected for the specified folder - do you wish to run a Full Backup instead? (y/n): ")
            if return_main_menu == "y":
                Clear_Console()
                Full_Backup()
                break
            elif return_main_menu == "n":
                Clear_Console()
                exit()
            else:
                print(colored("Invalid input - please try again...\n", "red"))



def Clear_Console():
    os.system('cls' if os.name == 'nt' else 'clear')


def Latest_Full():
    global source_path
    get_dates = []
    with open('backup_log.csv') as csv_file:
        for data in csv.DictReader(csv_file):
            if data['type'] == "full" and data['src-path'] == source_path:
                get_dates.append(data)
    latest_full_backup = max(get_dates, key=lambda x: x['date-time'])
    result = latest_full_backup['bck-path']
    return result


# START PROGRAM

while(True):
    Main_Menu()
