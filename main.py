# IMPORTERING AF PAKKER

import shutil  # modul som gør det muligt at flytte, kopiere og slette filer.
import os  # modul som giver mulighed for administration af mapper, fx. skift af CWD samt oprettelse/sletning af mapper.
import sys  # modul som bla. giver mulighed for udlæsning og evt. logning af in- og output direkte fra interpreteren.
from pick import pick
from termcolor import colored
from datetime import date  # funktionen date importeres fra datetime modulet, til angivelse af dato ved backupkørsler.


# DEFINERING AF FUNKTIONER

# def Full_Backup():
#    do something

# def Differential_Backup():
#    do something

# def Incremental_Backup():
#    do something


# HOVEDMENU

print(colored("Simple Backup by CHDuelund v1.0a", "blue", attrs=["bold", "underline"]))
title = "Please choose your favorite programming language: "
options = ["Java", "JavaScript", "Python", "PHP", "C++", "Erlang", "Haskell"]
option, index = pick(options, title, indicator="=>", default_index=2)
print(f"You choosed {option} at index {index}")
