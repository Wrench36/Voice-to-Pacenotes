# Voice-to-Pacenotes
Create pacenotes for RBR with voice commands.

Please see the [PDF](https://github.com/Wrench36/Voice-to-Pacenotes/blob/main/VTP%20Doc.pdf) at  for more information.

The Short version:<br>
Voice to pacenotes is a python script that uses your RBR pacenotes plugin install to determine the internal IDs of pacenotes, and then uses that information to write valid pacenote files using google speech recognition.
Have a look at the PDF file so I don't have to copy and reformat it here.

v0.3.0A:
Almost completley rewritten.
When starting VTP, you will need to specify your 'packages' file, that's the file in plugins/pacenote/config/pacenotes/packages and should be an ini.
Once this is done VTP will store a json file to remember the settings.
VTP PTT button binding is as simple as pressing the button when asked to do so.
VTP now records only as long as the button is held down.
Many bug fixes and updates.
