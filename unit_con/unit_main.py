"""
This is the central node of the individual unit. This is the "brain" that will communicate between the remote hub, and local functions of the unit.
Obviously this will eventually need to be done over a VPN...and sockets I guess

In fact in the networked version this can be done with sockets communicating directly to the hostname/IP address of the machine rather than
sending out a CC1 asking "name" to respond. Why call everyone to ask for one person?
"""

import json
import socket
import time
import threading

import commands
# from actions import servo
import unit_dbcontrol
import unit_id

class Unit():
    
    def __init__(self, HUB_ADDRESS):
        

        self.HUB_ADDRESS = HUB_ADDRESS
        self.STATUS_PORT = 7501
        self.COMMAND_PORT = 7502
        self.FILE_PORT = 7503
        self.UNIT_ADDRESS = "0.0.0.0"
        self.BUFFER_SIZE = 1024
        
        # to make sure connection isn't doubled up
        self.socket_open = False
        
        # used to split fragments of messages sent to hub
        self.SEPARATOR = "<SEPARATOR>"
        
        # status variable is used to inform hub of status of this unit
        self.status = unit_dbcontrol.get_own_status()
        self.autorotate = False
        
        self.unit_details = unit_id.unit_details
        
        self.label = "[" + self.unit_details['unit_name'].upper() + "]"
        
        print(f"{self.label} initialised")
        
        self.initialise()
        
    def initialise(self):
        """
        Start the different threads to send to/receive from the hub
        """
        
        # keep hub updated with status
        threading.Thread(target=self.report_in).start()
        
        # listen for command signals from hub
        threading.Thread(target=self.command_listener).start()
        
        unit_dbcontrol.update_status("Idle")
        

    def report_in(self):
        """
        Upon activation, the first thing the unit should do is report to the hub that it is active so that commands can be sent.
        Eventually THIS WILL REQUIRE VPN ACTIVATION.
        This then runs every 60 seconds and sends the status from the unit db to the hub
        """
        
        # Report to the hub what this unit is (ie static or rover and name)
        unit_overview = f"_{self.unit_details['unit_id']}_{self.unit_details['unit_name']}_{self.unit_details['type']}"
        s = socket.socket()
        s.connect((self.HUB_ADDRESS, self.STATUS_PORT))
        activation_msg = "<UNIT_ACTIVATED>" + unit_overview.replace("_", self.SEPARATOR)
        s.send(activation_msg.encode())
        s.close()
        print(f"{self.label} Activation report sent to Hub.")
        time.sleep(0.5)
        
        # make regular status reports
        while True:
            time.sleep(60)
            self.statrep()
            
    def command_listener(self):
        """"
        Runs constantly to listen for commands from the hub
        """
        while True:
            s = socket.socket()
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # make socket re-usable...
            s.bind((self.UNIT_ADDRESS, 7502))
            s.listen(5)
            print(f"{self.label} {self.unit_details['unit_name']} listening for commands")
            
            try:
                hub_socket, address = s.accept()
                print(f"{self.label} Signal received from {address[0]}")
                
                received = hub_socket.recv(self.BUFFER_SIZE).decode()
                cleaned_receive = received.split(self.SEPARATOR)
                
                print(f"{self.label} Signal from hub: {cleaned_receive}")
                
                if cleaned_receive[0] == "<SEND_STATREP>":
                    self.statrep()
                else:                
                    commands.command_router(cleaned_receive, self.HUB_ADDRESS)
                    unit_dbcontrol.update_status(str(cleaned_receive[1]))
  
            except Exception as e:
                print(f"{self.label} Connection error: {e}")
            
            hub_socket.close()
            s.close()
            time.sleep(0.5)
        
    def statrep(self):
        print(f"{self.label} STATUS: {self.status}")
        
        s=socket.socket()
        
        print(f"{self.label} Connecting to hub...")
        s.connect((self.HUB_ADDRESS, self.STATUS_PORT))
        print(f"{self.label} Connected to hub at {self.HUB_ADDRESS}")
        
        message = f"<STATREP>{self.SEPARATOR}{self.unit_details['unit_name'].upper()}{self.SEPARATOR}{self.status}"
        
        s.send(message.encode())
        
        print(f"{self.label} Status update to hub: {self.status}\n")
        
        s.close()

    def get_name(self, requested_name):
        """
        Simple function to test hub communicating with units as individuals.
        If the hub sends a message to a specific unit (in this case specified by unit name) then only that unit responds.
        I can use this to send orders to specific units later.
        Why store the unit details in a JSON? I don't bloody know it just sounded right.
        """
        
        if requested_name == self.unit_details['unit_name']:
            # msg = f"{self.unit_details['unit_name']}. Unit type: {self.unit_details['type']}"
            # return msg
            
            s=socket.socket()
            self.socket_open = True
            
            print("{self.label} Connecting to hub...")
            s.connect((self.HUB_ADDRESS, self.STATUS_PORT))
            print(f"{self.label} Connected to hub at {self.HUB_ADDRESS}")
            s.send(f"<MESSAGE>{self.SEPARATOR}{self.unit_details['unit_name'].upper()}{self.SEPARATOR}reporting in as ordered".encode())
            
            s.close()
            self.socket_open = False
            
        else:
            print(f"{self.label} Hub pinged for {requested_name}. I'm {self.unit_details['unit_name']}, that's not me.")
        
        
# Decided against making this a function, just instantiate the Unit class
# activate()


# unit = Unit("192.168.1.64")

# Try this, if doesn't work, use the above
unit=socket.gethostname()
unit = Unit(unit_id.unit_details['hub_address'])
print(unit)