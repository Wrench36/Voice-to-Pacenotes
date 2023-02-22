import os
noteDictArray = []
noteDictArray.append("noteDict = [\n\t'DISTANCE',\n")
rbrDir = R"D:\\Richard Burns Rally\\"
  
# opening and reading the file
fileNames = [
    rbrDir+R"Plugins\\Pacenote\\config\\pacenotes\\packages\\additional\\Extended.ini",
    rbrDir+R"Plugins\\Pacenote\\config\\pacenotes\\packages\\corners\\Numeric-Swapped.ini",
    rbrDir+R"Plugins\\Pacenote\\config\\pacenotes\\packages\\adjectives\\Extended.ini",
    rbrDir+R"Plugins\\Pacenote\\config\\pacenotes\\packages\\cautions\\Extended.ini",
    rbrDir+R"Plugins\\Pacenote\\config\\pacenotes\\packages\\condition\\Extended.ini",
    rbrDir+R"Plugins\\Pacenote\\config\\pacenotes\\packages\\construction\\Extended.ini",
    rbrDir+R"Plugins\\Pacenote\\config\\pacenotes\\packages\\driving\\Extended.ini",
    rbrDir+R"Plugins\\Pacenote\\config\\pacenotes\\packages\\line\\Extended.ini",
    rbrDir+R"Plugins\\Pacenote\\config\\pacenotes\\packages\\links\\Extended.ini",
    rbrDir+R"Plugins\\Pacenote\\config\\pacenotes\\packages\\modifier\\Extended.ini",
    rbrDir+R"Plugins\\Pacenote\\config\\pacenotes\\packages\\obstacles\\Extended.ini",
    rbrDir+R"Plugins\\Pacenote\\config\\pacenotes\\packages\\prepositions\\Extended.ini",
    rbrDir+R"Plugins\\Pacenote\\config\\pacenotes\\packages\\road\\Extended.ini",
    rbrDir+R"Plugins\\Pacenote\\config\\pacenotes\\packages\\surface\\Extended.ini",
]

for i in range(len(fileNames)):
    file_read = open(fileNames[i], "r")

    # reading file content line by line.
    lines = file_read.readlines()
    # looping through each line in the file
    for j in range(len(lines)):
        thisLine = lines[j]
        if thisLine.find("::") > -1:
            thisSeg = thisLine.replace("[PACENOTE::","")
            thisSeg = thisSeg.replace("]","")
            thisSeg = thisSeg.replace("'","")
            thisSeg = thisSeg.replace("     ; legacy sound and modifier","")
            thisSeg = thisSeg.replace("    ; legacy sound and modifier","")
            thisSeg = thisSeg.replace(" ; legacy sound and modifier","")
            thisSeg = thisSeg.replace("\n","")
            thisSeg = thisSeg.replace("_"," ")
            noteDictArray.append("\t'"+thisSeg+"',\n")
noteDictArray.append("]")
file1 = open("generatedDict.py", "w")  # append mode
file1.writelines(noteDictArray)
file1.close()
