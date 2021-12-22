"""
Dronekit version of drone control
It has a much nicer syntax than pymavlink, but fewer features
For example no way of confirming commands were successful
No way of indicate when a moving self.vehicle has reached its destination (whereas pymavlink constantly sending telemetry)
This can be done by measuring distance to target though
"""
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

import unit_dbcontrol
from drone_control import signaller
from unit_id import unit_details

class FlightController():
    """
    Represents the Flight Control board that the RPi will be connected to on each vehicle unit
    Will probably need a FlightController to be instantiated in hub_con?!?!? Yes duh get round to it
    """
    
    def __init__(self, port=14550):
        self.vehicle = connect(f"127.0.0.1:{port}", wait_ready=True)
        self.HUB_ADDRESS = unit_details['hub_address']
        self.SIGNAL_PORT = 7501
        
        print(f"[{unit_details['unit_name']}] FC CONTROL: Connected")
        print(f"---Location: {self.vehicle.location.global_frame}")
        print(f"---GPS: {self.vehicle.gps_0}")
        print(f"---Can be armed: {self.vehicle.is_armable}")
        print(f"---Mode: {self.vehicle.mode.name}")
        print(f"---Armed status: {self.vehicle.armed}\n")




    def command_subrouter(self, command):
        print(f"[FLIGHT CONTROLLER] - COMMAND RECEIVED: {command}")
        if command[1] == "launch":
            print(f"[{unit_details['unit_name']}] FC CONTROL: Launching...")
            self.initialise()
            self.launch(10)
        else:
            print(f"[{unit_details['unit_name']}] FC CONTROL: unknown command: {command[1]}")

    def initialise(self):
        while not self.vehicle.home_location:
            cmds = self.vehicle.commands
            cmds.download()
            cmds.wait_ready()
            if not self.vehicle.home_location:
                print(f"[{unit_details['unit_name']}] FC CONTROL: Waiting for home to be set...")
                time.sleep(0.5)
                
    # def get_params():
    #     params = {}
    #     for k,v in self.vehicle.parameters.iteritems():
    #         params[k] = v
    #     return params

    def launch(self, starting_alt):
        """Arms and launches the UAV"""
        
        while not self.vehicle.is_armable:
            print(f"[{unit_details['unit_name']}] FC CONTROL: self.vehicle initialising...")
            time.sleep(1)
        
        print(f"[{unit_details['unit_name']}] FC CONTROL: WARNING - ARMING MOTORS!")
        time.sleep(1)
        
        self.vehicle.mode = VehicleMode("GUIDED")
        self.vehicle.armed = True
        
        while not self.vehicle.armed:
            print(f"[{unit_details['unit_name']}] FC CONTROL: Arming...")
            time.sleep(1)

        print(f"[{unit_details['unit_name']}] FC CONTROL: LAUNCHING")
        self.vehicle.simple_takeoff(starting_alt)
        
        while True:
            print(f"[{unit_details['unit_name']}] FC CONTROL: Alt: {self.vehicle.location.global_relative_frame.alt}")
            if self.vehicle.location.global_relative_frame.alt >= starting_alt*0.95:
                print(f"[{unit_details['unit_name']}] FC CONTROL: Takeoff successful - UAV at target altitude")
                signaller.message(HUB_ADDRESS, SIGNAL_PORT, f"{unit_details['unit_name']} Takeoff successful")
                unit_dbcontrol.update_status("Airborne")
                break
            time.sleep(1)
            
    def travel(self, dest: list, groundspeed: float):
        target = LocationGlobalRelative(dest[0], dest[1], dest[2]) # lat, lng, alt (RELATIVE to home position)
        self.vehicle.simple_goto(target, groundspeed=groundspeed)
        print(f"[{unit_details['unit_name']}] FC CONTROL: vehicle moving")
        signaller.message(HUB_ADDRESS, SIGNAL_PORT, message=f"{unit_details['unit_name']} Travelling to {dest[0]} | {dest[1]} Final Alt: {dest[2]}", activity="Launch")
        unit_dbcontrol.update_status("Travelling")

if __name__ == '__main__':
    # connecting to local vehicle simulated
    # vehicle = connect("127.0.0.1:14550", wait_ready=True)
    vehicle = FlightController()

    HUB_ADDRESS = unit_details['hub_address']
    SIGNAL_PORT = 7501

    #connecting over serial device (for rpi connected to the vehicle via serial port, use com14 for windows serial AND telem radio)
    # vehicle = connect("/dev/ttyAMA0", wait_ready=True, baud=57600)

    """
    Connect to multiple vehicles by calling connect() for each vehicle
    Each vehicle will need to be a separate class?
    """
    print(f"[{unit_details['unit_name']}] FC CONTROL: Connected")
    print(f"---Global location: {vehicle.location.global_frame}")
    print(f"---GPS: {vehicle.gps_0}")
    print(f"---Can be armed: {vehicle.is_armable}")
    print(f"---Mode: {vehicle.mode.name}")
    print(f"---Armed: {vehicle.armed}\n")
    # if not vehicle.armed:
    #     vehicle.launch(10)
    # vehicle.travel([51.1415097, -4.2534511, 30], 15.0)