""" 
THIS SCRIPT IS PROVIDED AS IS WITH NO WARRANTY, NO GARUNTEE IT WON'T BREAK YOUR PACENOTES, OR ANYTHING ELSE
That said, it should be reasonably safe. It will read your pacenotes config files, but won't write to them.

LICENCE:
    Feel free to use, share, edit, and steal from this script however you'd like. I would like a mention whenever applicable, though,
        so please mention it in videos in which it appears, or in comments section of code you write using chunks of it.
        
Please see "Voice to Pacenotes Documentation.pdf" for more information.

tele code taken from post on reddit
VERION 0.2
"""
import socket
import struct
import os
import keyboard
import pygame
import speech_recognition as sr
import pyttsx3
import tkinter
from tkinter import filedialog
import operator
import winsound
import time

pygame.init()

UDP_IP = "127.0.0.1"
UDP_PORT = 6776

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
sock.settimeout(0.5)

# Initialize the recognizer
r = sr.Recognizer()

engine = pyttsx3.init()
engine.setProperty('rate', 400)
def SpeakText(command):
    engine.say(command)
    engine.runAndWait()

import noteDict
noteDictArray = noteDict.noteDict

import iniInterpret
noteIdArray = iniInterpret.noteIdArray

def checkDict(note):
    if not note:
        return False
    noteLen = len(note)+1
    foundAr = {}
    for i in range(len(noteDictArray)):
        found = note.find(noteDictArray[i])
        if found > -1:
            if not foundAr.get(found):
                foundAr[found]={}
            foundAr[found][len(foundAr[found])+1]=noteDictArray[i]
    sorted_keys = sorted(foundAr.keys())

    pacenote = ""
    pacenoteLen = 0
    pacenoteIds = []
    for key in sorted_keys:
        if key < pacenoteLen:
            continue
        value = foundAr[key]
        longest = ""
        longestNum = 0
        for seg in value:
            noteSeg = value.get(seg)
            length = len(noteSeg)
            if length > longestNum:
                longestNum = length
                longest = noteSeg
                pacenoteIds.append(noteIdArray[longest])
        pacenote = pacenote + longest + " "
        pacenoteLen = len(pacenote)
    if pacenoteLen == noteLen:
        return(pacenoteIds)
    else:
        return False

exportJB = input('Export Joystick and Buttons?: y/n')

#Edit the below to set defaults
joyNum = 0
btnNum = 8



joyNum = int(joyNum)
btnNum = int(btnNum)

if exportJB =="y":
    joystick_count = pygame.joystick.get_count()
    print("Number of joysticks: {}".format(joystick_count) )
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        name = joystick.get_name()
        print(i)
        print(name)
    joy = pygame.joystick.Joystick(1)
    joy.init()
    numBtn = joy.get_numbuttons()
    print(numBtn)
    joyNum = input('Which joystick would you like to use?')
    joyNum = int(joyNum)
    btnNum = input("Which button would you like to use?")
    btnNum = int(btnNum)

    
specialCases = {
    'CUT' : '64',
    "DONT CUT" : '32',
    'LONG' : '1024',
    'TIGHTENS' : '4',
    'DOUBLE TIGHTENS' : '128',
    'INTO' : '256',#no link
}
joy = pygame.joystick.Joystick(joyNum)
joy.init()
def handleSpecialCase(case,totalNotesTab):
    thisFlag = specialCases[case]
    totalNotesTab[len(totalNotesTab)-1]['flag'] = thisFlag

def speechRec():   
    print("listening")
    try:
        # use the microphone as source for input.
        with sr.Microphone() as source2:
            #r.adjust_for_ambient_noise(source2, duration=0.2)
            while True:
                pygame.event.get()
                if joy.get_button(btnNum):
                    audio2 = r.listen(source2)
                else:
                    print('break')
                    break
            # Using google to recognize audio
            try:
                MyText = r.recognize_google(audio2)
                
                MyText = MyText.replace("1", "one")
                MyText = MyText.replace("2", "two")
                MyText = MyText.replace("too", "two")
                MyText = MyText.replace(" to", " two")
                MyText = MyText.replace("3", "three")
                MyText = MyText.replace("4", "four")
                MyText = MyText.replace("for", "four")
                MyText = MyText.replace("5", "five")
                MyText = MyText.replace("6", "six")
                MyText = MyText.replace("write", "right")
                MyText = MyText.replace("intwo", "into")
                MyText = MyText.replace("break", "brake")
                MyText = MyText.replace("Titans", "TIGHTENS")
                MyText = MyText.replace("BRAKEING", "BRAKING")
                MyText = MyText.replace("TWO SITE DISTANCE", "TO SIGHT DISTANCE")
                MyText = MyText.replace("'", "")
                MyText = MyText.upper()
                return MyText

            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))
                
            except sr.UnknownValueError:
                print("unknown error occurred")
    except:
        return False

def basicSpeechRec():
    try:
        with sr.Microphone() as source2:
            audio2 = r.listen(source2)
            MyText = r.recognize_google(audio2)
            return MyText
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    except sr.UnknownValueError:
        print("unknown error occurred")

def getBaseNotes(filename):
    totalNotesTab = []
    requirements = [
        '21', #start
        '23', #split
        '22', #finish
        '24', #end of track
    ]
    default_file = open(filename,"r")
    lines = default_file.readlines()
    for i in range(len(lines)):
        thisLine = lines[i]
        for j in range(len(requirements)):
            if thisLine.find("type = " + requirements[j]) > -1:
                progressline = str(lines[i+1])
                progress = progressline.replace("distance = ","")
                progress = progress.replace("\n","")
                progress = progress.replace("distance = ","")
                noteLine = {
                    'progress' : float(progress),
                    'noteSeg': requirements[j],
                    'flag' : 0,
                }
                totalNotesTab.append(noteLine)
    return totalNotesTab

def loop():
    rawStringsTab = []
    firstLoop = True
    firstTimeout = True
    while True:
        if firstLoop:
            firstLoop = False
            winsound.Beep(800, 125)
            print("ready for pacenotes.")
        if keyboard.is_pressed("q"):
            winsound.Beep(800, 125)
            postLoop(rawStringsTab)
            break
        try:
            tele, adress = sock.recvfrom(664) # buffer size is 664 bytes
            firstTimeout = True
        except socket.timeout:
            if firstTimeout:
                print("no tele data")
                firstTimeout = False
            pass
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN:
                if exportJB == "y":
                        print(str(event.button))
                if event.button == btnNum:
                    #progress = round(struct.unpack_from('<f', tele , offset=16)[0],1)
                    progress = 30
                    note = speechRec()
                    if note:
                        print("note = " + note)
                    if note == "EDIT LAST":
                        rawStringsTab = editLast(rawStringsTab) or rawStringsTab
                        continue
                    if note == "EDIT NEAREST":
                        rawStringsTab = editNearest(progress,rawStringsTab) or rawStringsTab
                        continue
                    if note == "MOVE LAST":
                        rawStringsTab = moveLast(rawStringsTab) or rawStringsTab
                    pacenoteIds = checkDict(note)
                    print(pacenoteIds)
                    if pacenoteIds:
                        rawStringsTab.append({
                            "string" : note,
                            "progress" : progress,
                            })
                        SpeakText(note)
                    else:
                        SpeakText("I'm sorry, I don't think I heard you correctly.")

def editLast(rawStringsTab):
    SpeakText("edit Last")
    note = speechRec()
    if note == "CANCEL":
        SpeakText("cancel")
        return False
    pacenoteIds = checkDict(note)
    if pacenoteIds:
        prevNote = rawStringsTab[len(rawStringsTab)-1]["string"]
        rawStringsTab[len(rawStringsTab)-1]["string"] = note
        SpeakText(prevNote + " Changed to " + note)
        return rawStringsTab
    else:
        SpeakText("I'm sorry, I don't think I heard you correctly.")
        return False

def editNearest(progress,rawStringsTab):
    SpeakText("Edit Nearest")
    idx = find_nearest(rawStringsTab, progress)
    SpeakText(rawStringsTab[idx]["string"])
    note = speechRec()
    if note == "CANCEL":
        SpeakText("cancel")
        return False
    noteSeg = checkDict(note)
    if noteSeg:
        prevNote = rawStringsTab[idx]["string"]
        rawStringsTab[idx]["string"] = note
        SpeakText(prevNote + " Changed to " + note)
        return rawStringsTab
    else:
        SpeakText("I'm sorry, I don't think I heard you correctly.")
        return False

def moveLast(rawStringsTab):
    SpeakText("move Last")
    delta = basicSpeechRec()
    if delta == "CANCEL":
        SpeakText("cancel")
        return False
    try:
        delta = delta.replace("plus", "+")
        delta = delta.replace("minus", "-")
        delta = delta.replace(" ", "")
        delta = float(delta)
        progress = rawStringsTab[len(rawStringsTab)-1]["progress"]
        rawStringsTab[len(rawStringsTab)-1]["progress"] = progress + delta
        SpeakText("%s moved from %i to %i" % (rawStringsTab[len(rawStringsTab)-1]["string"],progress,rawStringsTab[len(rawStringsTab)-1]["progress"]))
        return rawStringsTab
    except Exception as e:
        SpeakText(e)
        return False

def moveNearest(progress,rawStringsTab):
    SpeakText("Move Nearest")
    idx = find_nearest(rawStringsTab, progress)
    SpeakText("%s at %s" % (rawStringsTab[idx]["string"],rawStringsTab[idx]["progress"]))
    delta = basicSpeechRec()
    if delta == "CANCEL":
        SpeakText("cancel")
        return False
    try:
        delta = delta.replace("plus", "+")
        delta = delta.replace("minus", "-")
        delta = delta.replace(" ", "")
        delta = float(delta)
        progress = rawStringsTab[idx]["progress"]
        rawStringsTab[idx]["progress"] = progress + delta
        SpeakText("%s moved from %i to %i" % (rawStringsTab[idx]["string"],progress,rawStringsTab[idx]["progress"]))
        return rawStringsTab
    except Exception as e:
        SpeakText(e)
        return False


def find_nearest(array, value):
    idx = 0
    minSep = float('inf')
    for i in range(len(array)):
        thisSep = abs(array[i]["progress"] - value)
        if thisSep < minSep:
            minSep = thisSep
            idx = i
    return idx

def convertNotes(_list):
    tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing
    filename = filedialog.askopenfilename(title='Select the default pacenotes file',)
    totalNotesTab = getBaseNotes(filename)
    for i in range(len(_list)):
        noteSeg = checkDict(_list[i]["string"])
        if noteSeg:
            for j in range(len(noteSeg)):
                if isinstance(noteSeg[j], set):
                    for k in noteSeg[j]:
                        handleSpecialCase(k,totalNotesTab)
                elif noteSeg[j] == 1024:
                    handleSpecialCase("INTO",totalNotesTab)
                    noteLine = {
                        'progress' : round(_list[i]["progress"]+0.1*j,2),
                        'noteSeg': noteSeg[j],
                        'flag' : 0,
                        'note' : _list[i]["string"],
                    }
                    totalNotesTab.append(noteLine)
                else:
                    noteLine = {
                        'progress' : round(_list[i]["progress"]+0.1*j,2),
                        'noteSeg': noteSeg[j],
                        'flag' : 0,
                        'note' : _list[i]["string"],
                    }
                    totalNotesTab.append(noteLine)
    return totalNotesTab

def testMovelast():
    print("testMoveLast")
    thisList = [
        {'string': 'LEFT ONE', 'progress': 30.0},
        {'string': 'LEFT TWO', 'progress': 35.0},
        {'string': 'LEFT THREE', 'progress': 40.0},
    ]
    thisList = moveNearest(36,thisList) or thisList
    print(thisList)

def organizeNotes(notesTab):
    sortedTab = sorted(notesTab, key=operator.itemgetter('progress'))
    return sortedTab

def postLoop(rawStringsTab):
    totalNotesTab = convertNotes(rawStringsTab)
    totalNotesTab = organizeNotes(totalNotesTab)
    tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing
    file1Name = tkinter.filedialog.asksaveasfilename(title='New pacenotes file',)
    file1 = open(file1Name,"w")
    file1.write(";Pacenotes trascribed by Wrench's python script.\n")
    file1.write("[PACENOTES]\n")
    paceNoteNmStr = "count = %s\n" % (len(totalNotesTab))
    file1.write(paceNoteNmStr + "\n")

    for i in range(len(totalNotesTab)):
        if 'note' in totalNotesTab[i]:
            thisNote = totalNotesTab[i]['note']
        else:
            thisNote = ""
        file1.write(";%s\n" %(thisNote))
        file1.write("[P%s]\ntype = %s\n" % (i,totalNotesTab[i]['noteSeg']))
        file1.write("distance = %0.2f\n" % (totalNotesTab[i]['progress']))
        file1.write("flag = %s\n\n" % totalNotesTab[i]['flag'])

    file1.close()
    loop()

loop()