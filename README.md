# Voice-to-Pacenotes
Create pacenotes for RBR with voice commands.

Please see the [PDF](https://github.com/Wrench36/Voice-to-Pacenotes/blob/main/VTP%20Doc.pdf) at  for more information.

The Short version:<br>
Voice to pacenotes is a python script that uses your RBR pacenotes plugin instal to determine the internal IDs of pacenotes, and then uses that information to write valid pacenote files using google speech recognition.

Voice to Pacenotes (VTP) Documentation
Requirements:
Python:
Install requirements using the batch file "install requirements.bat" provided, or the 
command "pip install -r requirements.txt" 
Note that python and pip are required. That can be its own rabbit hole, so google is your 
friend here if you don't already use python.
Rbr Config:
Turn on UDP telemetry and add a slot for port 8000.
 
Note:
This can also be changed in voiceToPacenotes.py
Script Config:
This is done automatically when VTP starts for the first time. VTP will ask for your “packages” file, that’s the ini that’s in \Plugins\Pacenote\config\pacenotes\packages and will relate to your co-driver mod. Once VTP has loaded your co-driver mod, it will save a .json file of the configuration. This means VTP won’t need to load the ini every time it starts, but the .json fil will need to be deleted when/if the co-driver mod is changed.
YouTube Tutorials:
Check my YouTube channel for tutorials on VTP.
 
Usage
Startup:
1.	Run the python script to get started.
2.	The script will list any notes that it can’t build definitions for, verify that the “Failed Types” it prints is blank.
3.	VTP will prompt for a PTT button, press the desired button to start listening.
4.	VTP will beep and print “ready for pacenotes”
5.	If RBR isn't already running on a stage, the message "no telemetry" will be printed. 
5.1.	If this happens while RBR is running on a stage (and not paused from alt+tab), verify telemetry is on and ports are set properly.
Writing Notes:
1.	Press and hold the PTT button
2.	Speak the note at a measured pace.
2.1.	Any number of “not segments” can be recorded at once, for example,
"left three long into right four tightens over crest and bump into chicane left"
would work, but it’s not recommended to use more than three note segments at a time.
2.2.	If more than a handful of segments are needed, try breaking them up into multiple calls.
3.	Wait a half-second before releasing the button.
4.	VTP will process the audio and if a correct combination of notes can be found, it will speak the notes back.
5.	To add distance calls, simply drive to the corner exit, press the button, and say "distance".
Editing Notes:
1.	Edit the nearest note 
1.1.	Press PTT and say “Edit Last”
1.2.	VTP will respond with “Edit Last” and enter edit mode
1.3.	Press PTT and say the correct note, i.e. “Left Five”
1.4.	VTP will respond with “<previous note> changed to <new note>” i.e. “Left Four changed to Left Five”
2.	Edit any note
2.1.	Drive as close as possible to the note you’d like to change
2.2.	Press PTT and say “Edit Nearest”
2.3.	VTP will respond with “Edit Nearest” and enter edit mode
2.4.	Press PTT and say the correct note, i.e. “Left Five”
2.5.	VTP will respond with “<previous note> changed to <new note>” i.e. “Left Four changed to Left Five”
3.	To cancel an edit , simply say "Cancel" instead of a correction.
Outputting the Result:
1.	To exit the pacenotes writing loop, press the "Q" key. 
1.1.	Note: You may have to hold it for a second. 
2.	VTP will beep to confirm it's entering output mode. 
3.	VTP will open an explorer dialog named 'Select the default pacenotes file' 
4.	Select the default pacenote file for the stage from <Richard Burns Rally Install>/Plugins/NGPCarMenu/MyPacenotes/<stage name> 
5.	VTP will then immediately open another explorer window called 'New pacenotes file.' 
6.	Pick a name for the new pacenotes file
6.1.	 Remember to include the ".ini". 
7.	 Press "save"
