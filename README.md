
# SimpleBackup by CHDuelund

SimpleBackup is a console driven backup script that enables the user to make backup of every local folder. It was made as part of a project in school, in order to learn how to code in Python. Due to this, the code used in this script might have design flaws and is to be used at your own responsibility.
## Features

- Full Backup
- Differential Backup


## Installation

No installation is required. Just unpack the files and run the main.py in your terminal.
    
## Usage

#### Full Backup
```
1. Type in the source folder (The folder that you want to backup)
2. Type in the destination folder (The folder where you would like to store the backup)

Please note that the destination folder needs to be an existing folder!
```
#### Differential Backup
```
1. Type in the source folder (The folder that you want to backup)
    - The script will check the log file to see if a full backup i present for the folder
    - If a Full Backup is not present, one has to be made. Alternatively you can exit the script
2. Type in the destination folder (The folder where you would like to store the backup)
    - The script will compare files from the source folder with the latest Full Backup

Please note that the destination folder needs to be an existing folder!
```
## Roadmap

- Incremental Backup
- Restore function
- General optimization of the code
- GUI

