# Voice-to-Pacenotes
Create pacenotes for RBR with voice commands.

Please see the PDF at https://github.com/Wrench36/Voice-to-Pacenotes/blob/main/Voice%20to%20Pacenotes%20Documentation.pdf for more information.

The Short version:<br>
Voice to pacenotes is a python script that uses your RBR pacenotes plugin instal to determine the internal IDs of pacenotes, and then uses that information to write valid pacenote files using google speech recognition.

Python requirements:<br>
See requirements.txt for a list of requirements.<br>
Install requirements using the batch file "install requirements.bat" provided, or the command "pip install -r requirements.txt"

Pacenotes plugin config:<br>
Included is a pacenotes mod to make this easier, but some may not want to use it (numeric swapped)<br>
If you don't want to use it, go to "Advanced configuration" below.

RBR config:<br>
In RSF the launcher, set the UDP telemetry on, and port to 6776. You can edit the port below if needed for some reason.

Script Config:<br>
Open iniInterpret.py and edit the RBR install directory in line 6 to match yours.<br>

Usage:<br>
Simply run the python script to get started (I use a shortcut)<br>
The script will ask "Export Joystick and Buttons?” y/n" if you enter "y" and then press enter, the script will list all available joysticks, along with their assigned number as the script sees them. It will then ask which joystick and button to use, hereafter referred to as "the button".<br>
I recommend changing the defaults in voicetopacenotes.py so you don't have to do this every time.<br>
This can be skipped by simply pressing enter.<br>
The script should now beep, and show a message "ready for pacenotes."

To set defaults:<br>
  Find the line "#Edit the below to set defaults" below (use ctrl+f) and enter the joystick and button numbers you'd like to use on the next two lines.
  
If RBR isn't already running on a stage, you'll see the message "no telemetry" printed.<br>
If you see this while RBR is running on a stage, verify telemetry is on and ports are set properly.<br>
If it still doesn't work, ¯"\"_(ツ)_/¯<br>
Start your recce run as normal

Writing notes:<br>
Press and hold the button, wait a half-second or so, then say wahtever you'd like the co-driver to say, the same as you would have previously typed in Roadbook or entered via the pacenotes UI.<br>
-To add distance calls, simply drive to the corner exit, press the button, and say "distance"<br>
-To edit the last pacenote (like if you think a turn is a Left 3, then realize that it tightens) press the button and say "edit last"<br>
  --The script will say "edit last" to confirm, then listen for the correction. Simply respond with the correct note, like "Left 3 tightens"<br>
  --The script will respond with the existing pacenote and the correction, i.e. "Left 3 changed to Left 3 Tightens"<br>
-To edit any pacenote, drive as close as possible to where you put it, press the button, and say "edit nearest".<br>
  --For example, let's say we put down the distance call before realizing that the turn tightens, as above.<br>
  --If we try to edit last, it will edit the distance call, not the turn, so we use "Edit nearest".<br>
  --The script will say "edit nearest" and then the existing note.<br>
  --Respond with the correction.<br>
  --The script will confirm the correction, i.e., "Left 3 changed to Left 3 Tightens."<br>
-Moving notes is done the same as above, only say "move last" or "move nearest", and then say "plus" or "minus" and the distance. i.e.<br>
  --"Plus 10" or "Minus 15"<br>

Outputting the result:<br>
-To exit the pacenotes writing loop, press the "Q" key. Note: You may have to hold it for a second.<br>
-The script will beep to confirm it's entering output mode.<br>
-The script will open an explorer dialog named 'Select the default pacenotes file'<br>
-Select the default pacenote file for the stage from <Richard Burns Rally Install>/Plugins/NGPCarMenu/MyPacenotes/<stage name><br>
-The script will then immediately open another called 'New pacenotes file.'<br>
-Pick a name for the new pacenotes ("made with Wrench's awesome python script" would be a great name, just sayin')<br>
  --Remember to include the ".ini

Using the pacenotes:<br>
RBR RSF mod's version of the pacenotes plugin should use the latest pacenote file by default, so simply exit to the main menu (RSF menu) and reload the stage.<br>

ADVANCED CONFIGURATION:<br>
See the included PDF. This will also be updated as the script is updated.<br>
-The additional scripts are not documented yet, but generateDict.py scans your pacenotes config and creates a noteDict for you. Notice that it is named
  generatedDict.py" so you can look it over before you overwrite our original.<br>
-Translation fix edits the translation files of the pacenotes plug-in to match any config edits you've done.<br>
  -This does edit your RBR install so be aware there could be potential problems.<br>
  -This really only affects the pacenotes UI so it's not really needed.<br>
-Using languages other than English<br>
  -This is theoretically possible, see the pdf.
  
If you run into problems, or if I forgot anything here, join the support discord at https://discord.gg/Mqk53VRj













