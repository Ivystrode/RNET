Nascent watchers in the weeds

Local bash alias is annoying. Use activate-rnet in home alias (for pyvenv)

- The UNIT directory is what will be installed on each static/rover unit. This will contain control code for the individual unit (inc for motion if a rover), communication code for talking to the hub, and a unique unit_id file

- The HUB directory is what will run on the server. This will contain a web interface and a telegram bot to control and check the status of all units.

- Status channel = 7501
- Command channel = 7502

CURRENT STATE
Connection over same network functional. Servo move and CPU commands work. Status updates work (STATREPs). Hub tracks units in a local db file.

Next - test camera functions and sending pictures/videos to hub over the network

NOTES

- May get stuck on a process continuing to listen on a port even after application (hub or unit) is closed, but machine stays on. In order not to get Errno 98 - Address already in use, will need to kill the process:
    - sudo netstat -nlp | grep [port number]
    - cp        0      0 0.0.0.0:8069            0.0.0.0:*               LISTEN      10869/python2 
    - or a line to that effect...the process number is 10869
    - sudo kill -9 10869
- May need to disable or add exception to firewall to communicate