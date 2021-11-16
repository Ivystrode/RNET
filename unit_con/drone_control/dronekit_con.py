"""
Dronekit version of drone control
It has a much nicer syntax than pymavlink, but fewer features
For example no way of confirming commands were successful
No way of indicate when a moving vehicle has reached its destination (whereas pymavlink constantly sending telemetry)
This can be done by measuring distance to target though
"""

from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

import unit_dbcontrol
from drone_control import signaller
from unit_id import unit_details

# connecting to local vehicle simulated
# can this work if we use VPN/local network IP addresses??
vehicle = connect("127.0.0.1:14550", wait_ready=True)

HUB_ADDRESS = unit_details['hub_address']
SIGNAL_PORT = 7501

#connecting over serial device (for rpi connected to the vehicle via serial port, use com14 for windows serial AND telem radio)
# vehicle = connect("/dev/ttyAMA0", wait_ready=True, baud=57600)

"""
Connect to multiple vehicles by calling connect() for each vehicle
Each vehicle will need to be a separate class?
"""
print("Connected")
print(f"Global location: {vehicle.location.global_frame}")
print(f"GPS: {vehicle.gps_0}")
print(f"Can be armed: {vehicle.is_armable}")
print(f"Mode: {vehicle.mode.name}")
print(f"Armed: {vehicle.armed}")


def command_subrouter(command):
    print("[FLIGHT CONTROLLER] - COMMAND RECEIVED")
    print(command)
    if command[1] == "launch":
        print("launching...")
        initialise()
        launch(10)
    else:
        print(f"unknown command: {command[1]}")

def initialise():
    while not vehicle.home_location:
        cmds = vehicle.commands
        cmds.download()
        cmds.wait_ready()
        if not vehicle.home_location:
            print("Waiting for home to be set...")
            time.sleep(0.5)
            
# def get_params():
#     params = {}
#     for k,v in vehicle.parameters.iteritems():
#         params[k] = v
#     return params

def launch(starting_alt):
    """Arms and launches the UAV"""
    
    while not vehicle.is_armable:
        print("Vehicle initialising...")
        time.sleep(1)
    
    print("!!!WARNING - ARMING MOTORS!!!")
    time.sleep(1)
    
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True
    
    while not vehicle.armed:
        print("arming...")
        time.sleep(1)

    print("LAUNCHING")
    vehicle.simple_takeoff(starting_alt)
    
    while True:
        print(f"Alt: {vehicle.location.global_relative_frame.alt}")
        if vehicle.location.global_relative_frame.alt >= starting_alt*0.95:
            print("Takeoff successful - UAV at target altitude")
            signaller.message(HUB_ADDRESS, SIGNAL_PORT, f"{unit_details['unit_name']} Takeoff successful")
            unit_dbcontrol.update_status("Airborne")
            break
        time.sleep(1)
        
def travel(dest, groundspeed: float):
    target = LocationGlobalRelative(dest[0], dest[1], dest[2])
    vehicle.simple_goto(target, groundspeed=groundspeed)
    print("Vehicle moving")
    signaller.message(HUB_ADDRESS, SIGNAL_PORT, f"{unit_details['unit_name']} Travelling to {dest[0]} | {dest[1]} Final Alt: {dest[2]}")
    unit_dbcontrol.update_status("Travelling")

if __name__ == '__main__':
    if not vehicle.armed:
        launch(10)
    travel([51.1415097, -4.2534511, 30], 15.0)