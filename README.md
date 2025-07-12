# Save timestamp to an EDL file with a shortcut

This is a **simple python script** that upon pressing a key, writes a timestamp of the current time (in seconds, minutes and hours from when the program started) to a file in **CMX 3600 EDL** format. Easy to later import into editing programs and to sync with your recorded clip for easy clips editing.
Currently supports just **Davinci Resolve**, will add **Adobe Premiere** later on.
The console windows needs to be open, but it doesn't need to be in focus of course, so you can use this in any program whatsoever.

If you're gonna run the python script **on its own**, you're gonna need to install the *"keyboard"* library.

If the script can't find the config file (edltimestamps_config.ini), it's gonna create one on its own in the same folder where the program or the script is, with **"alt gr+f10"** as a default for recording timestamps, and **"ctrl+del"** to stop the program.

You wanna change the shortcuts but you're not sure how a key you want to set is called? Run the **key_finder.exe** or **key_finder.py** and follow the istructions.
---
To **import** an **EDL file in Davinci Resolve**, right click on the timeline, then go to Timelines --> Import --> Timeline Markes from EDL... and simply choose the correct file.
![How to import EDL file in Resolve](https://i.imgur.com/Dkj8paw.png)
