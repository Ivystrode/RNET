# RNET

*"One hub to control them all, and in the browser, manage them"*

**RNET** is a control system for area surveillance - as well as being capable of some active measures. A server hosts the control "hub", that links to numerous "units" over the cellular network using a VPN for security. The server hosts a web GUI for operators to manage and control the various units. Each unit is simply a companion computer (RPi) running the RNET OS image, either as a standalone static unit (essentially a smart CCTV camera with extra features) or integrated into an autonomous vehicle ("drone") that can take any form - multirotor, fixed wing, wheeled, water-borne, etc.

---

This readme is mostly my own notes

###READMES:
1. Main readme (here)
2. unit_con/drone_control - drone control readme

LMT-Desktop: Local bash alias is annoying. Use activate-rnet in home alias (for pyvenv)

LMT-Desktop-2: use project_env dir for virtual env (same alias as LMT DT 1)

Make sure all PCs have git config set to match github account email address, otherwise commits will appear to come from some random user (FFS!)

- The UNIT directory is what will be running on each static/rover unit. This will contain control code for the individual unit (inc for motion if a rover), communication code for talking to the hub, etc. There is also a unit OS image that should be flashed to each unit first.

- The other files will run on the server. This is the web interface, control hub and a telegram bot to help control and check the status of all units. Bot will get grumpy.

- Status channel = 7501
- Command channel = 7502

DRONE TESTING - NOTE THAT HUB_ADDRESS IS CHANGED TO LOOPBACK ADDRESS
CHANGE THIS BACK TO SERVER ADDRESS WHEN NOT SIM TESTING (THIS APPLIES ONLY WHEN RUNNING HUB, UNIT, MISSION PLANNER AND SITL ON SAME MACHINE)

- Command pathway done from bot --> hub --> cmd router --> unit --> router --> drone controller
- Signaller messages FC status back to hub
- For working with drones/sim drones
    - Start hub
    - Start drone
    - Start unit (unit_main.py)
    - Start mission planner on hub machine - try pointing it to the [unit address]:14550 udp port
    - Send commands via bot or web interface
- When testing - running unit AND mission planner on loopback (127.0.0.1) stops mission planner from working so may need two machines to do proper testing
- However it does seem to still run the sim (sim_vehicle.py output still showing the sim vehicle is active). Just mission planner that doesn't work.




TODO
- Telegram bot keyboard commands & nested options
- Run object recognition model/recognition alerts
- RF silent mode
- sqlite3 is rubbish, migrate to postgres

How to use:
IMPORTANT - You will need to create your own telegram bot and use its key. For obvious reason I'm not letting anyone else have my bot key! Same goes for the django settings key. Store them as environment variables or however you want.

1. Set up a new wireguard VPN on host machine - if you don't know how to do this then...google it
2. Clone repository
3. Install from requirements.txt into a virtual env
4. Create a superuser ("python manage.py createsuperuser)
5. Run server ("django manage.py runserver"), go to /admin and set your account status to authorised (custom user attribute that allows you to use the interface)
5. Add yourself to the authorised users of the telegram bot by sending "/start" to the bot. You will see an "activate hub" button...press that and the hub will start, the telegram bot will run


6. Install RNET OS image on SD card
7. Insert SD card into raspberry pi (preferable 4B+)
8. Switch on RPi - VPN will attempt to connect automatically (should see a blue or green light on the 4G stick)
9. It probably won't work - see #1 - you will need to change the .conf file and add the server endpoint and public key
10. If red light on 4G stick try to find somewhere with better cellular reception. Or connect to ethernet to simulate it if that's not possible - it will not work well on wifi as it has to disconnect the second wifi antenna to use the other one in monitor mode.
11. Depending on whether I get this done in time, it should start the unit_main script right away (via crontab)
    - If not, either ssh into it or do via monitor & keyboard, and start the script
    - I need to create an up-to-date OS image but I probably won't until I have created a fresh install with raspian-lite (desktop version is bigger than necessary)
12. Unit should now send activation report to the hub

13. To use with drones (simulated, unless you have a custom one pre-built):
    a. Install Mission Planner and SITL &/ sim_vehicle.py -- sim_vehicle.py -v ArduCopter -L devon
    b. Run sim_vehicle.py (as quad/plane/anything) or switch on drone/FC
    c. Open MP and then control as you would a real drone using RNET
    d. For a physical drone you will need one built to house RNET (ie an RPi in it with mountings for peripherals) and a means of telemetry (3DR/SiK radio)


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
