***USING DRONES***

These are my own notes...

Installation issues on prototype1. Reinstall from unit OS backup (simple enough to clone the repo) - NOT DONE YET

1. Simulation (for testing)
    - Start unit and hub, in this case unit will be a test unit (ie running SITL sim_vehicle)
    - On test unit, once SITL sim_vehicle is running, type in the SITL console: *output add [ip_address_of_hub]:14550* (the port you select to receive on)
    - On hub, open mission planner, in top right select UDP from ports list, choose which port to listen on (selected 14550 above) and connect
    - You should now be able to control the simulated drone on the hub via mission planner

2. Live drone
    - Connect RPi to FC UART (assuming FC is preprogrammed to accept the correct input on that UART first)
    - RPi must have wireguard VPN & rnet unit script set up to activate on reboot/switch on
    - 4G stick must be connected to RPi
    - Drone will now be controllable via RNET dashboard
    - To view in mission planner the output will have to be added
    - To control multiple drones from mission planner each unit/drone will need to output to a different port (see point 2 under simulation)

I think that about covers it