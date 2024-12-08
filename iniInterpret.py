"""
    Copy the package ini capability from CDT and set that on line 14.
    This could keep track of which ini file each call comes from, so it can add that to the failed types list
    I should also rename each "Array" to accuratley reflect if they're a dict or a list.
        This would require updating the main py with the new names.
        I could also print that information and stop saving the files since the script doesn't need them.
"""
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import configparser
import json

def select_file_dialog(file_type,initial_dir):
    root = tk.Tk()
    root.withdraw()
    file = filedialog.askopenfilename(initialdir=initial_dir,title=f"Select {file_type}",filetypes=[(file_type, "*")])
    return file

def read_and_process_ini(packages_ini_path):

    base_dir = os.path.dirname(os.path.abspath(packages_ini_path))
    
    fileNames = []
    """Reads the master ini file and processes the listed files."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    #base_dir = os.path.abspath(os.path.join(script_dir, "../../config/pacenotes/packages"))

    if not os.path.exists(packages_ini_path):
        print(f"INI file not found: {packages_ini_path}")
        return

    config = configparser.ConfigParser()
    config.read(packages_ini_path)

    for section in config.sections():
        if section.startswith("CATEGORY::"):
            relative_file = config[section].get("file")
            if relative_file:
                full_path = os.path.join(base_dir, relative_file)
                if os.path.exists(full_path):
                    fileNames.append(full_path)
                else:
                    print(f"File not found: {full_path}")
            else:
                print(f"No file path found in section {section}")
            
            relative_file = config[section].get("file2")
            if relative_file:
                full_path = os.path.join(base_dir, relative_file)
                if os.path.exists(full_path):
                    fileNames.append(full_path)
                else:
                    print(f"File not found: {full_path}")
            else:
                print(f"No file path found in section {section}")
    
    noteIdDict = build_noteDict(fileNames)
    return noteIdDict
 
def build_noteDict(fileNames):
    noteDictArray = []
    noteIdDict = {}
    failedArray = []
    #edit the below to match your RBR installation

    for i in range(len(fileNames)):
        config = configparser.ConfigParser()
        config.read(fileNames[i])

        for section in config.sections():
            if section.startswith("PACENOTE::"):
                print(section)
                print(config.items(section))
                name = section.replace("PACENOTE::","")
                name = name.replace("_"," ")
                name = name.lower()
                
                id = config.get(section, "id", fallback=False)
                print(id)
                if id:
                    last_folder = os.path.basename(os.path.dirname(fileNames[i]))
                    file_name = os.path.basename(fileNames[i])
                    result = os.path.join(last_folder, file_name)
                    noteIdDict[name] = [int(id),result,name]
                else:
                    noteIdDict[name] = [name,result,name]
    noteIdDict["empty call"] = [int(4075), "rbrLinks","empty call"]
    noteIdDict["and"] = [int(4084),"rbrLinks","and"]
    noteIdDict["onto"] = [int(4082), "rbrLinks","onto"]
    noteIdDict["jump"] = [int(20), "rbrObstacles","jump"]
    noteIdDict["overcrest"] = [int(16), "rbrObstacles","overcrest"]
    noteIdDict["ford"] = [int(17), "rbrObstacles","ford"]
    noteIdDict["bump"] = [int(19), "rbrObstacles","bump"]
    noteIdDict["bridge"] = [int(27), "rbrObstacles","bridge"]
    #print(noteIdDict)
                
                

    for note in noteDictArray:
        thisNote = note
        thisNote = thisNote.upper()
        failed= True
        for note2,id in noteIdDict.items():
            note2 = note2.upper()
            if thisNote == note2:
                failed = False

        if failed == True:
            failedArray.append(thisNote)
    
    with open("noteIdDict.json", "w") as f:
        json.dump(noteIdDict, f, indent=4)
    return noteIdDict
            
def main():
    global noteIdDict
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    
    noteDict_path = os.path.abspath(os.path.join(parent_dir, "noteDict.py"))
    noteIdDict_path = os.path.abspath(os.path.join(parent_dir, "noteIdDict.json"))
    if os.path.exists(noteIdDict_path):
        with open(noteIdDict_path, 'r') as f:
            noteIdDict = json.load(f)
    else:
        print("File does not exist.")
        packages_dir = os.path.abspath(os.path.join(parent_dir, "../../config/pacenotes/packages"))
        ini_path = select_file_dialog("Packages ini file",packages_dir)
        if ini_path:
            noteIdDict = read_and_process_ini(ini_path)
        else:
            print("No file selected.")
    


main()

