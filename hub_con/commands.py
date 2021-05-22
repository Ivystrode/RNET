"""
hub_main and bot will both link here
This is where they can access commands to send to the unit/s
"""

import socket

import dbcontrol

SEPARATOR = "<SEPARATOR>"
command_channel = 7502

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
    print("[HUB - COMMANDS] CPU Command")
    s = socket.socket()
    s.connect((unit_addr, command_channel))
    s.send(f"<CPU_COMD>{SEPARATOR}{command}".encode())
    print(f"[HUB - COMMANDS] CPU command '{command}' sent to {unit_addr}")
    s.close()
    
def send_file(unit_addr, command_channel, filetype, vid_length):
    print("[HUB - COMMANDS] File send command")
    s = socket.socket()
    s.connect((unit_addr, command_channel))
    s.send(f"<SEND_FILE>{SEPARATOR}{filetype}{SEPARATOR}{vid_length}".encode())
    print(f"[HUB - COMMANDS] {filetype.upper()} command sent to {unit_addr}")
    s.close()