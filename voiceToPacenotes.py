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

"""
    to do: 
    test, test, and re test.
"""
import socket
import struct
import os
import sys
import keyboard
import pygame
import pyaudio
import speech_recognition as sr
import pyttsx3
import tkinter
from tkinter import filedialog
import operator
import winsound
import wave
from io import BytesIO
from inspect import currentframe, getframeinfo
import inspect
import json
import gc
try:
    os.system('cls')
    frameinfo = getframeinfo(currentframe())
    def print_ln(arg):
        frameinfo = currentframe()
        print(frameinfo.f_back.f_lineno,":",arg)
    global debugMode
    debugMode = False

    n = len(sys.argv)
    for i in range(1, n):
        print(sys.argv[i], end = "\n")
        if sys.argv[i] == "debug":
            debugMode = True
    if debugMode:
        print("debugMode MODE!")


    pygame.init()

    UDP_IP = "127.0.0.1"
    #UDP_PORT = 6776
    UDP_PORT = 8000

    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))
    sock.settimeout(0.5)

    # Initialize the recognizer
    r = sr.Recognizer()

    engine = pyttsx3.init()
    engine.setProperty('rate', 200)
    def SpeakText(command):
        engine.say(command)
        engine.runAndWait()

    import iniInterpret

    noteIdDict = iniInterpret.noteIdDict

    def checkDict(note):
        if not note:
            return False
        noteLen = len(note)+1
        foundAr = {}
        for key, value in noteIdDict.items():      
            found = note.find(key)
            if found > -1:
                if not foundAr.get(found):
                    foundAr[found]={}
                foundAr[found][len(foundAr[found])+1]=key
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
                    getDict = noteIdDict.get(longest)
            if longest in noteIdDict:
                pacenoteIds.append(noteIdDict[longest])
            else:
                SpeakText(f"{longest} is missing from note Dict.")
            pacenote = pacenote + longest + " "
            pacenote = pacenote.replace("and","empty call and")
            pacenote = pacenote.replace("empty call empty call","empty call")
            pacenoteLen = len(pacenote)
        if pacenoteLen == noteLen:
            return(pacenoteIds)
        else:
            return False



    joysticks = {}

    joystick_count = pygame.joystick.get_count()
    print("Please press your desired VTP PTT button.")
    for i in range(joystick_count):
        joysticks[i] = {}
        joysticks[i]["pygame"] = pygame.joystick.Joystick(i)
        joysticks[i]["pygame"].init()
        joysticks[i]["name"] = joysticks[i]["pygame"].get_name()
    pressed = False
    while pressed == False:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN:
                btnNum = event.button
                joyNum = event.joy
                pressed = True

    joy = pygame.joystick.Joystick(joyNum)
    joy.init()
    links = {
        #'into' : '0',
        'and' : '256',#no link
        'onto' : '256',
    } 
    def handleLink(case):
        thisFlag = links.get(case)
        if thisFlag:
            return thisFlag
        else:
            return 0
        
    modifiers = {
        'narrows' : '533741569',
        'wideout' : '2',
        'tightens' : '4',
        'tightensbad' : '128',
        'cut' : '64',
        'dontcut' : '32',
        'long' : '1024'
    }

    def speechRec(editBool):
        print("listening")
        try:
            # use the microphone as source for input.
            with sr.Microphone() as source2:
                #r.adjust_for_ambient_noise(source2, duration=0.2)
                audio2 = r.record(source=source2,duration=2)
                # Using google to recognize audio
                try:
                    MyText = r.recognize_google(audio2)
                    if editBool:
                        MyText = editSpeech(MyText)
                    return MyText

                except sr.RequestError as e:
                    print("Could not request results; {0}".format(e))
                    
                except sr.UnknownValueError:
                    print("unknown error occurred")
        except:
            return False

    def speechRecord2(audio,audio_format, channels, rate, chunk):
        """Start recording audio and return the stream and frames."""
        frames = []
        stream = audio.open(format=audio_format, channels=channels,
                            rate=rate, input=True, frames_per_buffer=chunk)
        stream.start_stream()
        return stream, frames


    def editSpeech(MyText):
        MyText = MyText.lower()
        MyText = MyText.replace("'", "")
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
        MyText = MyText.replace("titans", "TIGHTENS")
        MyText = MyText.replace("brakeing", "BRAKING")
        MyText = MyText.replace("two site distance", "TO SIGHT DISTANCE")
        MyText = MyText.replace("think", "kink")
        MyText = MyText.replace("pink", "kink")
        MyText = MyText.replace("on to", "onto")
        MyText = MyText.replace("wide out", "wideout")
        MyText = MyText.replace("tightens bad", "tightensbad")
        MyText = MyText.replace("dont cut", "dontcut")
        MyText = MyText.replace("over crest", "overcrest")
        
        #MyText = MyText.replace("onto", "onto2")
        #MyText = MyText.replace("on to", "onto2")
        #MyText = MyText.replace("bridge", "bridge2")
        MyText = MyText.lower()
        
        
        return MyText

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
                audio_format = pyaudio.paInt16
                channels = 1
                rate = 44100
                chunk = 1024
                audio = pyaudio.PyAudio()
                recording = False
                global modeEditLast
                global modeEditNearest
                global modeMoveLast
                global modeMoveNearest
                modeEditLast = False
                modeEditNearest = False
                modeMoveLast = False
                modeMoveNearest = False
                winsound.Beep(800, 125)
                print_ln("ready for pacenotes.")
            if keyboard.is_pressed("q"):
                winsound.Beep(800, 125)
                postLoop(rawStringsTab)
                break
            if recording:
                    # Append audio frames while recording
                    frames.append(stream.read(chunk))
            try:
                tele, adress = sock.recvfrom(664) # buffer size is 664 bytes
                firstTimeout = True
            except socket.timeout:
                if firstTimeout:
                    print_ln("no tele data")
                    firstTimeout = False
                pass
            events = pygame.event.get()
            for event in events:
                
                ##### on button press
                if event.type == pygame.JOYBUTTONDOWN and event.button == btnNum:
                    if debugMode:
                        progress = 30
                        print("debugMode means all notes are at 30m!!!")
                    else:
                        try:
                            progress = round(struct.unpack_from('<f', tele , offset=16)[0],1)
                        except Exception as e:
                            if not 'tele' in locals():
                                print("not receiving telemetry")
                                SpeakText("not receiving telemetry")
                            else:
                                print(e)
                                SpeakText(e)
                            continue
                    print("Recording...")
                    if not recording:
                        recording = True
                        frames = []
                        stream, frames = speechRecord2(audio,audio_format, channels, rate, chunk)
                        
                ##### on button release
                elif event.type == pygame.JOYBUTTONUP and event.button == btnNum:
                        print("Stopped recording.")
                        if recording:
                            recording = False
                            stream.stop_stream()
                            stream.close()

                            # Process audio
                            audio_data = BytesIO()
                            wf = wave.open(audio_data, 'wb')
                            wf.setnchannels(channels)
                            wf.setsampwidth(audio.get_sample_size(audio_format))
                            wf.setframerate(rate)
                            wf.writeframes(b''.join(frames))
                            wf.close()
                            audio_data.seek(0)

                            # Recognize speech
                            with sr.AudioFile(audio_data) as source:
                                audio_content = r.record(source)
                                try:
                                    note = r.recognize_google(audio_content)
                                    note = editSpeech(note)
                                    
                                    ##### EDITS
                                    ##### edit last
                                    if note == "edit last":
                                        prevNote = rawStringsTab[len(rawStringsTab)-1]["string"]
                                        SpeakText(f"edit {prevNote}")
                                        modeEditLast = True
                                        continue
                                    if modeEditLast:
                                        print("editing last")
                                        rawStringsTab = editLast(rawStringsTab,note)
                                        continue
                                    ##### edit nearest
                                    if note == "edit nearest":
                                        modeEditNearest = True
                                        continue
                                    if modeEditNearest:
                                        print("editing nearest")
                                        rawStringsTab = editNearest(progress,rawStringsTab,note)
                                        continue

                                    ##### continue
                                    pacenoteIds = checkDict(note)
                                    if pacenoteIds:
                                        rawStringsTab.append({
                                            "string" : note,
                                            "progress" : progress,
                                            })
                                        SpeakText(note)
                                    else:
                                        SpeakText("I'm sorry, I don't think I heard you correctly.")
                                        
                                except sr.UnknownValueError:
                                    SpeakText("I'm sorry, I don't think I heard you correctly.")
                                except sr.RequestError as e:
                                    SpeakText(f"API error: {e}")
                                    print(f"API error: {e}")
                        

    def editLast(rawStringsTab,note):
        prevNote = rawStringsTab[len(rawStringsTab)-1]["string"]
        if note == "cancel":
            SpeakText("cancel")
        pacenoteIds = checkDict(note)
        if pacenoteIds:
            rawStringsTab[len(rawStringsTab)-1]["string"] = note
            SpeakText(f"{prevNote} changed to {note}")
            global modeEditLast
            modeEditLast = False
            
        else:
            SpeakText("I'm sorry, I don't think I heard you correctly.")
        return rawStringsTab

    def editNearest(progress,rawStringsTab,note):
        SpeakText("Edit Nearest")
        idx = find_nearest(rawStringsTab, progress)
        if note == "cancel":
            SpeakText("cancel")
        pacenoteIds = checkDict(note)
        if pacenoteIds:
            prevNote = rawStringsTab[idx]["string"]
            rawStringsTab[idx]["string"] = note
            SpeakText(f"{prevNote} changed to {note}")
            global modeEditNearest
            modeEditNearest = False
        else:
            SpeakText("I'm sorry, I don't think I heard you correctly.")
        return rawStringsTab

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
            note = _list[i]["string"]
            for key in links.keys():
                if key in note:
                    note = note.replace(key, f"empty call {key}")
            note = note.replace("into","empty call")
            noteSeg = checkDict(note)
            if noteSeg:
                progress = _list[i]["progress"]
                for j in range(len(noteSeg)):
                    progress = progress + (0.1*j)
                    thisId = noteSeg[j][0]
                    thisName = noteSeg[j][2]
                    if thisName in links.keys():
                        flag = handleLink(thisName)
                    elif thisName in modifiers.keys():
                        flag = modifiers.get(thisName)
                        totalNotesTab[len(totalNotesTab)-1]['flag'] = flag
                        continue
                    else:
                        flag = 0
                    noteLine = {
                        'progress' : round(progress,2),
                        'noteSeg': thisId,
                        'flag' : flag,
                        'note' : note,
                    }
                    totalNotesTab.append(noteLine)
        return totalNotesTab


    def organizeNotes(notesTab):
        sortedTab = sorted(notesTab, key=operator.itemgetter('progress'))
        return sortedTab

    def postLoop(rawStringsTab):
        #with open("postLoop.json", "w") as f:
            #json.dump(rawStringsTab, f, indent=4)
            
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


    def testoutput():
        print_ln("testOutput")
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        postLoopTestFile = os.path.abspath(os.path.join(parent_dir, "postloop.json"))
        if os.path.exists(postLoopTestFile):
            with open(postLoopTestFile, 'r') as f:
                postLoopData = json.load(f)
            postLoop(postLoopData)


    #testoutput()
    loop()


except KeyboardInterrupt:
    print("\nKeyboard interrupt detected. Exiting...")

finally:
    print("Releasing resources...")
    gc.collect()
    os.system('cls')
    print("Resources cleared.")