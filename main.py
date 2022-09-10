# IMPORTERING AF PAKKER

import shutil  # modul som gør det muligt at flytte, kopiere og slette filer.
import os  # modul som giver mulighed for administration af mapper, fx. skift af CWD samt oprettelse/sletning af mapper.
import sys  # modul som giver mulighed for udlæsning og evt. logning af in- og output direkte fra interpreteren.
from termcolor import colored # modul som gør det muligt at formatere tekst med farve og type.
import re # modul som gør det muligt at splitte en string ved brug af regex.
from datetime import date,datetime  # funktionen date importeres fra datetime modulet, til angivelse af dato ved backupkørsler.


# GLOBALE VARIABLER

get_today = date.today() # hent dato til variabel.
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


def Clear_Console():
    os.system('cls' if os.name == 'nt' else 'clear')


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

            shutil.copytree(source_path, destination_path + folder_name[-1] + "_full" + date_stamp + time_stamp)

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
    print("Running Differential Backup")


def Incremental_Backup():
    print("Running Incremental Backup")


# HOVEDMENU

while(True):
    Main_Menu()