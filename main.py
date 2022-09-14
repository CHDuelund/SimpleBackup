# IMPORTERING AF PAKKER

import shutil  # modul som gør det muligt at flytte, kopiere og slette filer.
import os  # modul som giver mulighed for administration af mapper, fx. skift af CWD samt oprettelse/sletning af mapper.
import sys  # modul som giver mulighed for udlæsning og evt. logning af in- og output direkte fra interpreteren.
from termcolor import colored # modul som gør det muligt at formatere tekst med farve og type.
import re # modul som gør det muligt at splitte en string ved brug af regex.
from datetime import date,datetime  # funktionen date importeres fra datetime modulet, til angivelse af dato ved backupkørsler.
import csv
from difflib import SequenceMatcher
import ntpath


# GLOBALE VARIABLER

get_today = date.today() # hent dato til variabel.
date_today = get_today.strftime("%d-%m-%Y")
date_stamp = get_today.strftime("_%d_%m_%Y") # konverter dato til ønsket format.


# DEFINERING AF FUNKTIONER

def Main_Menu():
    print(colored("Simple Backup by CHDuelund v1.0a\n", "blue", attrs=["bold", "underline"]))

    print(colored("Choose function:", attrs=["underline"]))
    print("1 = Full Backup\n2 = Differential Backup\n3 = Incremental Backup\n")

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
            Incremental_Backup()
            break
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

            print("Backup done!\n")

            while(True):
                return_main_menu = input("Return to main menu? (y/n): ")
                if return_main_menu == "y":
                    Clear_Console()
                    break
                elif return_main_menu =="n":
                    exit()
                else:
                    print(colored("Invalid input - please try again...\n", "red"))

            break

        else:
            print(colored("The path does not exist - please try again...\n", "red"))


def Clear_Console():
    os.system('cls' if os.name == 'nt' else 'clear')


def Differential_Backup():
    print(colored("\nDifferential Backup\n", "blue", attrs=["bold", "underline"]))

    while (True):
        source_path = input("Specify the source path: ")
        folder_exists = os.path.exists(source_path)  # kontrollerer om den angivne sti findes.
        folder_name = re.split(r'\\',source_path)  # deler variablen source_path op ved brug af regex med \ som "delimiter".
        if folder_exists == True:
            break
        else:
            print(colored("The path does not exist - please try again...\n", "red"))

    while (True):
        destination_path = input("Specify the destination path: ")
        if destination_path[-1] != "\\":
            destination_path = destination_path + "\\"  # tilføjer en \ til enden af den angivne sti, hvis den mangler.
        folder_exists = os.path.exists(destination_path)  # kontrollerer om den angivne sti findes.

        if folder_exists == True:
            get_time = datetime.now()  # hent tid til variabel.
            time_stamp = get_time.strftime("_%H_%M_%S")  # konverter tid til ønsket format.
            time_now = get_time.strftime("_%H:%M:%S")

            new_folder_path = destination_path + folder_name[-1] + "_diff" + date_stamp + time_stamp + "\\"
            latest_full = Latest_Full()

            # define your two folders, full paths
            first_path = os.path.abspath(source_path)
            second_path = os.path.abspath(latest_full)

            # get files from folder
            first_path_files = os.listdir(first_path)
            second_path_files = os.listdir(second_path)

            # join path and filenames
            first_folder = [os.path.join(first_path, f) for f in first_path_files]
            second_folder = [os.path.join(second_path, f) for f in second_path_files]

            # empty list for matching results
            matched_files = []

            # iterate over the files in the first folder
            for file_one in first_folder:
                print(file_one)
                if os.path.isfile(file_one):
                    with open(file_one, "r") as f:
                        file_one_text = f.read()

                # iterate over the files in the second folder
                    for file_two in second_folder:
                        if os.path.isfile(file_two):
                            with open(file_two, "r") as f:
                                file_two_text = f.read()

                    # match the two file contents
                    match = SequenceMatcher(None, file_one_text, file_two_text)
                    if match.ratio() < 1.0:
                        print(f"Changes found ({match.ratio()}): '{file_one}' | '{file_two}'")
                        # here you have to decide if you rather want to remove files from the first or second folder
                        matched_files.append(file_one)  # i delete files from the second folder

            # remove duplicates from the resulted list
            matched_files = list(set(matched_files))

            # remove the files
            for f in matched_files:
                print("Copying " + f + " to " + new_folder_path)
                file = ntpath.basename(f)
                os.makedirs(new_folder_path, exist_ok=True)
                shutil.copy2(f, new_folder_path + file)

            log_data = [source_path, destination_path + folder_name[-1] + "_diff" + date_stamp + time_stamp, "differential", date_today + time_now]
            with open('backup_log.csv', 'a', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(log_data)

            print("Backup done!\n")

            while (True):
                return_main_menu = input("Return to main menu? (y/n): ")
                if return_main_menu == "y":
                    Clear_Console()
                    break
                elif return_main_menu == "n":
                    exit()
                else:
                    print(colored("Invalid input - please try again...\n", "red"))

            break

        else:
            print(colored("The path does not exist - please try again...\n", "red"))



def Incremental_Backup():
    print("Running Incremental Backup")


def Clear_Console():
    os.system('cls' if os.name == 'nt' else 'clear')


def Latest_Full():
    get_dates = []
    with open('backup_log.csv') as csv_file:
        for data in csv.DictReader(csv_file):
            if data['type'] == "full":
                get_dates.append(data)
    latest_full_backup = max(get_dates, key=lambda x: x['date-time'])
    result = latest_full_backup['bck-path']
    return result


# HOVEDMENU

while(True):
    Main_Menu()
