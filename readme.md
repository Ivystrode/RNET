# RNET

*"One hub to link them all, and in the browser, manage them"*

**RNET** is a control system for area surveillance - as well as being capable of some active measures. A server hosts the control "hub", that links to numerous "units" over the cellular network using a VPN for security. The server hosts a web GUI for operators to manage and control the various units. Each unit is built around a micro computer/SBC (RPi) running the RNET OS image, either as a standalone static unit (essentially a smart CCTV camera with extra features) or integrated into an autonomous vehicle ("drone") that can take any form - multirotor, fixed wing, wheeled, water-borne, etc.

I couldn't think of a name for this project, so I just went with RNET for "Remote Network" and it stuck.

---

### Running RNET

You will need a lot of hardware to run RNET properly, or a lot of patience to set up a sim environment - preferably with at least two machines instead of one. Furthermore you'll need to create your own bot token, map token/API key and install SITL & MP. Otherwise this probably isn't worth you doing.

1. Clone repo
2. Install requirements (into a virtual env preferably)
3. Create telegram bot - set key as environment variable - and maps token. Also create new django settings secret key.
4. Download media dir (I haven't uploaded this yet so the web GUI ("interface") will look ***terrible*** without this FYI!!!)
5. For simulated testing:
    a. Install Mission Planner
    b. Install ardupilot/SITL (Software In The Loop)
6. Run manage.py runserver in the project directory, and open the web interface
7. Click "Activate Hub" to activate the server
8. On a separate machine - from the main project dir, run unit_con/unit_main.py (live units will autorun on startup)
9. Hub and one test unit are now running

---

### READMES:
1. Main readme (here)
2. unit_con/drone_control
3. data_management

Note - arstoahrta is a user that signed up with the email address "b@b.com". He'll appear as a contributor if you try to sign in to the git CLI with that as your "fake" email address...