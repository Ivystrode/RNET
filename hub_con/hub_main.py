from datetime import datetime
import json
import ntpath
import socket
import threading
import time
from tqdm import tqdm

import commands
import dbcontrol
from hub_bot import bot

class Hub():
    
    def __init__(self, SERVER_HOST):
        
        self.SERVER_HOST = SERVER_HOST
        self.STATUS_PORT = 7501
        self.COMMAND_PORT = 7502
        self.FILE_PORT = 7503
        self.BUFFER_SIZE = 1024
        self.SEPARATOR = "<SEPARATOR>"
        
        self.active_units = {} # units that have reported active to the hub (key is unit address, value is time of last statrep)
        self.lost_connection_units = {} # units that have missed a statrep
        
        self.initialise()
    
    def initialise(self):
        # receive status updates from units and update list of active units
        threading.Thread(target=self.status_channel).start()
        # check active status/check for lost connection
        threading.Thread(target=self.track_active_units).start()
        # port to receive files on
        threading.Thread(target=self.file_receiver).start()
        # threading.Thread(target=self.command_channel).start()
        
        
    def status_channel(self):
        """
        This loop will receive and process signals from units
        """
    
        while True:
            s = socket.socket()
            s.bind((self.SERVER_HOST, self.STATUS_PORT))
            s.listen(5)
            print("[HUB] Listening for connections")
            
            try:
                unit_socket, unit_address = s.accept()
                print(f"[HUB] Connection from {unit_address}")
                    
                received = unit_socket.recv(self.BUFFER_SIZE).decode()
                
                cleaned_received = received.split(self.SEPARATOR)
                
                if cleaned_received[0] == "<STATREP>":
                    print(f"[HUB] Message received: {cleaned_received}")
                    sending_unit_name = cleaned_received[1]
                    sending_unit_status = cleaned_received[2]
                    
                    try:
                        # if connection just recovered, inform user
                        unit_status = dbcontrol.check_unit_status(unit_address[0])
                        if unit_status == "Disconnected":
                            print(f"[HUB] Re-established connection to {sending_unit_name} ({unit_address[0]})")
                        
                        # update unit status
                        dbcontrol.update_unit(unit_address[0], cleaned_received[2], str(datetime.now().strftime("%Y%m%d%H%M")))
                        
                    except Exception as e:
                        if "UNIQUE constrained failed" in e:
                            print(f"[HUB] Unit already activated")
                        else:
                            print(f"[HUB] Database error: {e}")
                    # self.track_active_units(unit_address[0])
                
                    
                elif cleaned_received[0] == "<UNIT_ACTIVATED>":
                    print(f"[HUB] Message received: {cleaned_received}")
                    try:
                        dbcontrol.insert(cleaned_received[1], cleaned_received[2], unit_address[0], cleaned_received[3], "Idle", str(datetime.now().strftime("%Y%m%d%H%M")))
                    except Exception as e:
                        print(f"[HUB] Database error: {e}")

                else:
                    pass
                
            except Exception as e:
                print(f"[HUB] Connection error:\n{e}")
                
  
                
            unit_socket.close()
            s.close()
            time.sleep(0.5)
            
    def track_active_units(self):
        while True:
            known_units = dbcontrol.get_all_units()
            timenow = int(datetime.now().strftime("%Y%m%d%H%M"))
            
            for unit in known_units:
                
                if int(unit[5]) - timenow < -1:
                    self.lost_connection_units[unit[1]] = unit[5] # if it's missed a statrep, report connection loss
                    dbcontrol.update_unit(unit[2], "Disconnected", unit[5])
                    
                else:
                    if unit[1] in self.lost_connection_units.keys(): # if it has since made a statrep, report connection regained
                        self.lost_connection_units.pop(unit[1])
                        print(f"[HUB] Connection recovered to {unit[1]}")
                    
            # print(f"[HUB] Active units: {self.active_units}")
            
            if len(self.lost_connection_units) > 0:
                print(f"[HUB] WARNING! Connection Lost to: {self.lost_connection_units}")
            else:
                print("[HUB] All active units online")
            time.sleep(60)
            
    def file_receiver(self):
        file_socket = socket.socket()
        file_socket.bind((self.SERVER_HOST, self.FILE_PORT))
        file_socket.listen(5)
        
        while True:
        
            try:
                unit_socket, unit_address = file_socket.accept()
                unit_name = dbcontrol.get_unit_name(unit_address[0])
                print(f"[HUB] Incoming file from {unit_name}")
                
                try:
                    received = unit_socket.recv(self.BUFFER_SIZE).decode()
                except:
                    received = unit_socket.recv(self.BUFFER_SIZE).decode("iso-8859-1")
                
                if unit_name is not None:
                    
                    print(f"[HUB] Receiving file from {unit_name}")
                    # filedata = received.split(self.SEPARATOR)
                    # file = filedata[1]
                    # filesize = int(filedata[2])
                    file, filesize = received.split(self.SEPARATOR)
                    filesize = int(filesize)
                    filename = ntpath.basename(file)
                    
                    progress = tqdm(range(filesize), f"[HUB] Progress {filename}", unit="B", unit_scale=True, unit_divisor=1024)
                    with open(filename, "wb") as f: 
                        for _ in progress:
                            bytes_read = unit_socket.recv(self.BUFFER_SIZE)
                            if not bytes_read:

                                break
                            f.write(bytes_read)
                            progress.update(len(bytes_read))
                            
                else:
                    print("[HUB] File send attempt from unknown sender, file not accepted")
            except Exception as e:
                print(f"[HUB] {e}")
        
                
    def unit_message(self, name, status):
        print("[HUB]  Message received:")
        print(f"[HUB]  {name.upper()} status: {status}")
        
main_hub = Hub("0.0.0.0")