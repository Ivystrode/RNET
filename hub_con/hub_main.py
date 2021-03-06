from datetime import datetime
import ntpath
import shutil
import socket
import threading
import time
from tqdm import tqdm
from decouple import config

import sys
sys.path.append("/home/main/Documents/File_Root/Main/Code/Projects/rnet/rnet/")

from units.models import UnitPhoto
from .models import Control_Hub
from .views import save_file, record_activity

from hub_con import commands
from hub_con import dbcontrol

from hub_con.hub_bot.bot import HubBot

from interface import data

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
        
        self.bot = HubBot(config('tbot_key'))
        self.bot.activate_hub_bot()
        self.initialise()
        
        
        dbcontrol.connect()
    
    def initialise(self):
        # receive status updates from units and update list of active units
        threading.Thread(target=self.status_channel).start()
        # check active status/check for lost connection
        threading.Thread(target=self.track_active_units).start()
        # port to receive files on
        threading.Thread(target=self.file_receiver).start()
        # threading.Thread(target=self.command_channel).start()
        print("[HUB] Hub activated")
        
        
    def status_channel(self):
        """
        This loop will receive and process signals from units
        """
    
        while True:
            s = socket.socket()
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # make socket re-usable...
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
                        dbcontrol.update_unit(unit_address[0], cleaned_received[2], str(datetime.now().strftime("%Y%m%d%H%M")), cleaned_received[3], cleaned_received[4])
                        
                    except Exception as e:
                        if "UNIQUE constraint failed" in e:
                            print(f"[HUB] Unit already activated")
                        else:
                            print(f"[HUB] Database error: {e}")
                    # self.track_active_units(unit_address[0])
                
                    
                elif cleaned_received[0] == "<UNIT_ACTIVATED>":
                    print(f"[HUB] Message received: {cleaned_received}")
                        
                    try:
                        print("try to add new unit...")
                        dbcontrol.insert(cleaned_received[1], cleaned_received[2], unit_address[0], cleaned_received[3], "Activated", str(datetime.now().strftime("%Y%m%d%H%M")), cleaned_received[4], cleaned_received[5])
                        print(f"[HUB] {cleaned_received[2]} added to database")
                        record_activity(cleaned_received[2].lower(), "Unit activated")
                    except Exception as e:
                        print(f"{e} --- ok try to update the unit now...")
                        try:
                            print("trying to update...")
                            time.sleep(2)
                            dbcontrol.update_unit(unit_address[0], cleaned_received[2], str(datetime.now().strftime("%Y%m%d%H%M")), cleaned_received[4], cleaned_received[5])
                            print(f"[HUB] {cleaned_received[2]} re-activated")
                        except Exception as e:
                            print(f"[HUB] Database error: {e}")
                else: # if TELEM ? NO - should be OK as long as we follow the same message format/protocol as defined in signaller.py
                    print(f"[HUB] Message received: {cleaned_received}")
                    if cleaned_received[3] != "N/A":
                        record_activity(cleaned_received[3])
                    self.bot.send_message(cleaned_received[2])

                
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
                # print(unit)
                
                if int(unit[5]) - timenow < -1:
                    # if unit[1] not in self.lost_connection_units:
                        # self.bot.send_message(f"Lost connection to {unit[1]}")
                    self.lost_connection_units[unit[1]] = unit[5] # if it's missed a statrep, report connection loss
                    dbcontrol.update_unit(unit[2], "Disconnected", unit[5], unit[6], unit[7])
                    print(f"[HUB] Lost connection to {unit[1]}")
                    
                else:
                    if unit[1] in self.lost_connection_units.keys(): # if it has since made a statrep, report connection regained
                        self.lost_connection_units.pop(unit[1])
                        print(f"[HUB] Connection recovered to {unit[1]}")
                        self.bot.send_message(f"Connection to {unit[1]} recovered")
                        record_activity(unit[1], "Connection recovered")
                    
            # print(f"[HUB] Active units: {self.active_units}")
            
            if len(self.lost_connection_units) > 0:
                print(f"[HUB] WARNING! Connection Lost to: {self.lost_connection_units}")
                unitstring = [key for key in self.lost_connection_units.keys()]
                self.bot.send_message(f"Lost connection to: {', '.join(unitstring)}")
            else:
                print("[HUB] All active units online")
            time.sleep(60)
            
    def file_receiver(self):
        
        while True:
            file_socket = socket.socket()
            file_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # make socket re-usable...
            file_socket.bind((self.SERVER_HOST, self.FILE_PORT))
            file_socket.listen(5) # should this go in the while loop...?
        
            try:
                unit_socket, unit_address = file_socket.accept() # did i close this??
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
                    file, filesize, file_description, file_type = received.split(self.SEPARATOR)
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
                            
                    # if file_description[0:5] != "FIREQ": # if this is a file the unit decided to send of its own accord
                    try:
                        print(f"[HUB] Unsolicited file, sending to bot")
                        self.bot.send_unrequested_file(unit_name, filename, file_description)
                        print(f"[HUB] File sent by bot")
                        
                        #Ideally I'd like to save to a subdir in media/
                        #named after the unit, but for now this doesn't work
                        # if not os.path.exists(f"media/{unit_name}"):
                        #     os.mkdir(f"media/{unit_name}")
                        # shutil.move(filename, f'media/{unit_name}/')
                        # so I just do this
                        if file_description == "Wifi scan":
                            data.sort(filename)
                        shutil.move(filename, f'media/') # changed from move - to overwrite if already exists? changed back to move, we have unique names for ALL photos now
                        print(f"[HUB] {filename} moved to files directory")
                        
                        # save as unitphoto object to link to unit in django
                        # new_unit_photo = UnitPhoto.objects.create(caption=file_description, photo=filename)

                        print("[HUB] Saving file...")
                        save_file(unit_name, filename, file_description, file_type)
                        record_activity(unit_name, file_description)
                        print("[HUB] Saved")
                        
                    except Exception as e:
                        print(f"[HUB] Unable to send file: {e}")
                            
                    # else: # if this is a file requested by the user
                    #     print(f"[HUB] Bot file request - file thread ignoring file")
                    file_socket.close()
                            
                else:
                    print("[HUB] File send attempt from unknown sender, file not accepted")
            except Exception as e:
                print(f"[HUB] {e}")
        
                
    def unit_message(self, name, status):
        print("[HUB]  Message received:")
        print(f"[HUB]  {name.upper()} status: {status}")

if __name__ == '__main__':
    main_hub = Hub("0.0.0.0")
    # bot.activate_hub_bot()