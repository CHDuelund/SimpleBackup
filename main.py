# IMPORTERING AF PAKKER

import shutil  # modul som gør det muligt at flytte, kopiere og slette filer.
import os  # modul som giver mulighed for administration af mapper, fx. skift af CWD samt oprettelse/sletning af mapper.
import sys  # modul som bla. giver mulighed for udlæsning og evt. logning af in- og output direkte fra interpreteren.
from termcolor import colored
from datetime import date  # funktionen date importeres fra datetime modulet, til angivelse af dato ved backupkørsler.


# GLOBALE VARIABLER

get_today = date.today()
today = get_today.strftime("%d_%m_%Y_")


# DEFINERING AF FUNKTIONER

def Main_Menu():
    print(colored("Simple Backup by CHDuelund v1.0a\n", "blue", attrs=["bold", "underline"]))

    print(colored("Choose function:", attrs=["underline"]))
    print("1 = Full Backup\n2 = Differential Backup\n3 = Incremental Backup\n")

    while (True):
        function = input("Enter your choice: ")
        if function == "1":
            Full_Backup()
            break
        elif function == "2":
            Differential_Backup()
            break
        elif function == "3":
            Incremental_Backup()
            break
        else:
            print(colored("Invalid input - please try again...\n", "red"))

def Full_Backup():
    print(colored("\nFull Backup\n", "blue", attrs=["bold", "underline"]))
    source_path = input("Specify the source path: ")

def Differential_Backup():
    print("Running Differential Backup")

def Incremental_Backup():
    print("Running Incremental Backup")


# HOVEDMENU

Main_Menu()