import os
import noteDict
noteDictArray = noteDict.noteDict
noteIdArray = {}
failedArray = []
#edit the below to match your RBR installation
rbrDir = R"D:\\Richard Burns Rally\\"

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
    lines = file_read.readlines()
    for j in range(len(lines)):
        thisLine = lines[j]
        for k in range(len(noteDictArray)):
            note = noteDictArray[k]
            thisNote = noteDictArray[k]
            thisNote = thisNote.upper()
            thisNote = thisNote.replace(" ","_")
            thisNote = thisNote.replace("\t","")
            thisNote = thisNote.replace("'","")
            if thisLine.find("::" + thisNote + "]") > -1:
                thisId = lines[j+1]
                thisId = thisId.replace("id=","")
                thisId = thisId.replace("\n","")
                try:
                    noteIdArray[note] = int(thisId)
                except:
                    noteIdArray[note] = {note}
                    continue
noteIdArray["INTO"] = int(1003)
noteIdArray["DISTANCE"] = int(13)
for note in noteDictArray:
    thisNote = note
    thisNote = thisNote.upper()
    failed= True
    for note2,id in noteIdArray.items():
        if thisNote == note2:
            failed = False

    if failed == True:
        failedArray.append(thisNote)

file1 = open("types.txt", "w")
file1.write(str(noteIdArray))
file1.close()

file2 = open("failed types.txt","w")
file2.write(str(failedArray))
file2.close()
print("ini interpreter done")
