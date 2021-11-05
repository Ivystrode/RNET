Local bash alias is annoying. Use activate-rnet in home alias (for pyvenv)

- The UNIT directory is what will be installed on each static/rover unit. This will contain control code for the individual unit (inc for motion if a rover), communication code for talking to the hub, and a unique unit_id file

- The HUB directory is what will run on the server. This will contain a web interface and a telegram bot to control and check the status of all units.

- Status channel = 7501
- Command channel = 7502

CURRENT STATE
Connection over same network functional. Servo move and CPU commands work. Status updates work (STATREPs). Camera command can send pictures from selected unit back to hub/telegram bot. Wifi scan functions in progress. Hub tracks units in a local db file.


NOTES

- All future units use raspbian-lite. NO NEED for gui on units!!!

- NEED TO GET UNITS TO SYNC TIME TO SERVER. NTP & timedatectl are being a pain.
- Sort out imports with __main__ and __init__.py (ehh I'll do this later)
- May get stuck on a process continuing to listen on a port even after application (hub or unit) is closed, but machine stays on. In order not to get Errno 98 - Address already in use, will need to kill the process (automate this?):
    - sudo netstat -nlp | grep [port number]
    - cp        0      0 0.0.0.0:8069            0.0.0.0:*               LISTEN      10869/python2 
    - or a line to that effect...the process number is 10869
    - sudo kill -9 [processNum]
- May need to disable or add exception to firewall to communicate
- Make an error handling file that kills all active port listening processes and re-starts them...?
- "Sleep" function - the unit_main script that is running gets stopped, and instead, a "listener" is activated in another port waiting for the wake up call from the hub...
- Autorotate function...need new thread? or can it be done by the command listener checking a boolean and activating/deactivating as necessary?
- GO SILENT command - specify a number of minutes to not emit any RF (so WIFI IS SHUT OFF and lose connection to the unit). During this time the unit scans the wifiband (and RF sweep when figured out), and logs any optically detected objects, and once it reaches the end of the silent period it sends the report back to the hub
- change STATREPs to use a unit db file to get unit status, that way don't have to store it as a variable in any file and so cana easily be accessed/changed from any file.
- design case that can hold the Li-Ion shield

error fixes

wifi monitor mode not activating:
The boot scripts softblock the wlan when you haven't entered your country in

raspi-config -> localisation options -> Change WLAN Country

I would REALLY like to know what file this changes, as I wasted a lot of time trying to bring up a raspberry pi that was supposed to be doing wlan. I imaged the SD card, edited /boot/ssh and /etc/wpa_supplicant/wpa_supplicant.conf expecting the pi to boot and join my network....