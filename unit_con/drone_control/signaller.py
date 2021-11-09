"""
Handles Flight Controller messaging to the hub
"""
import socket
import unit_id

unit_details = unit_id.unit_details

SEPARATOR = "<SEPARATOR>"

def message(HUB_ADDRESS, PORT, message):
    
    s=socket.socket()
    
    print(f"[FLIGHT CONTROLLER] Connecting to hub...")
    s.connect((HUB_ADDRESS, PORT))
    print(f"[FLIGHT CONTROLLER] Connected to hub at {HUB_ADDRESS}")
    
    message = f"<TELEM>{SEPARATOR}{unit_details['unit_name'].upper()}{SEPARATOR}{message}"
    
    s.send(message.encode())
    
    print(f"[FLIGHT CONTROLLER] Message to hub: {message}\n")
    
    s.close()