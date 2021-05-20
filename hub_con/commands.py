"""
hub_main and bot will both link here
This is where they can access commands to send to the unit/s
"""

import socket

import dbcontrol

SEPARATOR = "<SEPARATOR>"

def get_unit_name(requested_name):
    pass

def servo_test(unit_addr, command_channel, axis, position):
    print("[HUB - COMMANDS] Servo command")
    s = socket.socket()
    s.connect((unit_addr, command_channel))
    s.send(f"<SERVO_MOVE>{SEPARATOR}{axis}{SEPARATOR}{position}".encode())
    print(f"[HUB - COMMANDS] Servo position {position} command sent to {unit_addr}")
    s.close()