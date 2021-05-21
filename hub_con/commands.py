"""
hub_main and bot will both link here
This is where they can access commands to send to the unit/s
"""

import socket

import dbcontrol

SEPARATOR = "<SEPARATOR>"

def get_unit_name(requested_name):
    pass

def servo_move(unit_addr, command_channel, axis, position):
    """Sends custom or centre move commands to one or all servos"""
    
    print("[HUB - COMMANDS] Servo command")
    s = socket.socket()
    s.connect((unit_addr, command_channel))
    s.send(f"<SERVO_MOVE>{SEPARATOR}{axis}{SEPARATOR}{position}".encode())
    print(f"[HUB - COMMANDS] Servo position {position} command sent to {unit_addr}")
    s.close()
    
def cpu_comd(unit_addr, command_channel, command):
    print("[HUB - COMMANDS] CPU Command")
    s = socket.socket()
    s.connect((unit_addr, command_channel))
    s.send(f"<CPU_COMD>{SEPARATOR}{command}".encode())
    print(f"[HUB - COMMANDS] CPU command '{command}' sent to {unit_addr}")
    s.close()
