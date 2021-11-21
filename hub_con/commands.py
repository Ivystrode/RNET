"""
hub_main and bot will both link here
This is where they can access commands to send to the unit/s
This could be refactored to be significantly less DRY but I'll waste my time with that kind of stuff later
"""

import socket, threading
from hub_con.video import video_receiver

# import dbcontrol
from hub_con import dbcontrol

SEPARATOR = "<SEPARATOR>"
command_channel = 7502

def interface_command(unit, command):
    unitaddr = dbcontrol.get_unit_address(unit)
    if command == "WIFI_SCAN":
        wifi_comd(unitaddr, command_channel, command, 5)
    elif command == "CAMERA_SHOT":
        send_file(unitaddr, command_channel, 'image', 'N/A')


def get_unit_status(name, addr):
    print(f"[HUB - COMMANDS] Check status of {name} ({addr})")
    try:
        s = socket.socket()
        s.connect((addr, command_channel))
        s.send(f"<SEND_STATREP>".encode())
        print(f"[HUB - COMMANDS] STATREP request sent to {name}: {addr}")
        s.close()
        return dbcontrol.get_unit_status(name)
    except:
        return "no_connection"
        print(f"[HUB - COMMANDS] Failed to connect to {name}: {addr}")

def servo_move(unit_addr, command_channel, axis, position):
    """Sends custom or centre move commands to one or all servos"""

    print("[HUB - COMMANDS] Servo command")
    s = socket.socket()
    s.connect((unit_addr, command_channel))
    s.send(f"<SERVO_MOVE>{SEPARATOR}{axis}{SEPARATOR}{position}".encode())
    print(f"[HUB - COMMANDS] Servo {axis.upper()} command sent to {unit_addr}")
    s.close()
    
def cpu_comd(unit_addr, command_channel, command):
    """Issue commands to the on board computer such as reboot etc"""
    
    print("[HUB - COMMANDS] CPU Command")
    s = socket.socket()
    s.connect((unit_addr, command_channel))
    s.send(f"<CPU_COMD>{SEPARATOR}{command}".encode())
    print(f"[HUB - COMMANDS] CPU command '{command}' sent to {unit_addr}")
    s.close()
    
def send_file(unit_addr, command_channel, filetype, vid_length):
    """Command unit to send file (such as picture) to the hub"""
    
    print("[HUB - COMMANDS] File send command")
    s = socket.socket()
    s.connect((unit_addr, command_channel))
    s.send(f"<SEND_FILE>{SEPARATOR}{filetype}{SEPARATOR}{vid_length}".encode())
    print(f"[HUB - COMMANDS] {filetype.upper()} command sent to {unit_addr}")
    s.close()
    
def receive_file(unit_name, filename, filetype):
    """
    On receipt of a file from a unit, decide what to do with it
    if return is True, the bot sends it to the/a user
    """
    pass
    
def wifi_comd(unit_addr, command_channel, command, time):
    """Currently issue monitor mode commands to the unit, later will also attack wifi networks"""
    
    print("[HUB - COMMANDS] Wifi command")
    s = socket.socket()
    s.connect((unit_addr, command_channel))
    s.send(f"<WIFI>{SEPARATOR}{command}{SEPARATOR}{time}".encode())
    print(f"[HUB - COMMANDS] Wifi {command} command sent to {unit_addr}")
    s.close()
    
def vid_comd(unit_addr, command_channel, command, time):
    """Tell unit to begin streaming video, detecting motion, or detecting specific objects"""
    
    print("[HUB - COMMANDS] Video command")
    s = socket.socket()
    s.connect((unit_addr, command_channel))
    s.send(f"<VIDEO>{SEPARATOR}{command}{SEPARATOR}{time}".encode())
    print(f"[HUB - COMMANDS] Video {command} command sent to {unit_addr}")
    s.close()
    
def fc_comd(unit_addr, command_channel, command):
    """Send a command to the unit that will be routed through pymavlink to the FC"""
    
    print(f"[HUB - COMMANDS] Flight Controller command: {command}")
    s = socket.socket()
    s.connect((unit_addr, command_channel))
    s.send(f"<FC_COMD>{SEPARATOR}{command}".encode())
    print(f"[HUB - COMMANDS] Flight Controller {command} command sent to {unit_addr}")
    s.close()  