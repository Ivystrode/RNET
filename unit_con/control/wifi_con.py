"""
This file will control the wifi band passive and active measures, like the DDO files
"""

from datetime import datetime
import os
import socket
import subprocess
import threading
import time
from tqdm import tqdm

label = "[" + socket.gethostname().upper() + "]"
scanning = False

hub_address = ""
file_channel = 7503

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024

def wifi_control(command, hub_addr):
    global hub_address
    hub_address = hub_addr
    # hub_addr = hub_address dont change this!!
    
    scan_time = command[2]
    if command[1].lower() == "scan":
        activate_monitor_mode(scan_time)
    elif command[1].lower() == "stop_scan":
        stop_scan()
    else:
        print(f"{label} Incorrect wifi control option received")
        

def activate_monitor_mode(scan_time):
    global scanning
    subprocess.Popen(f"sudo airmon-ng start wlan1", shell=True)
    print(f"{label} Wifi monitor mode active")
    scanning = True
    time.sleep(5)
    threading.Thread(target=scan).start()
    if scan_time != "continuous":
        time.sleep(int(scan_time))
    scanning = False

def stop_scan():
    global scanning
    scanning=False
    print(f"{label} Terminating wifi scan...")

def scan():
    global scanning
    scanning_activated = False
    
    while True:
        if scanning:
            if not scanning_activated:
                filename = f"{datetime.now().strftime('%Y%m%d-%H%M')}_{socket.gethostname()}_wifi_scan"
                wifi_scanner = subprocess.Popen(f"sudo airodump-ng -w {filename} --output-format csv wlan1mon", shell=True, stdout=subprocess.PIPE)
                # wifi_scanner.sta
                scanning_activated = True
                print(f"{label} Wifi scanner active")
                # time.sleep(10)
                # wifi_scanner.terminate()
            else:
                pass
            
        if not scanning:
            wifi_scanner.terminate()
            subprocess.Popen("sudo airmon-ng stop wlan1mon", shell=True)
            print(f"{label} Wifi scanner deactivated")
            send_report(hub_address, filename)
            break

def send_report(hub_addr, file):
    file = file + "-01.csv"
    s = socket.socket()
    print(f"{label} Connecting to hub...")
    s.connect((hub_addr, file_channel))
    filesize = os.path.getsize(file)
    file_description = f"wifi_scan_report {file}"

    print(f"{label} Sending scan report: {file}")
    s.send(f"{file}{SEPARATOR}{filesize}{SEPARATOR}{file_description}".encode())
    try:
        progress = tqdm(range(filesize), f"{label} Sending {file}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(file, "rb") as f:
            for _ in progress:
                try:
                    bytes_read = f.read(BUFFER_SIZE)
                    
                    if not bytes_read:
                        break
                    
                    s.sendall(bytes_read)
                    progress.update(len(bytes_read))
                except Exception as e:
                    print(f"{label} FILE SEND ERROR: {e}")
                    break
    except Exception as e:
        print(f"{label} FILE SEND ERROR - outside - {e}")
    print(f"{label} {file} sent to hub")
    s.close()
# Testing only
# activate_monitor_mode()
