"""
Handles Flight Controller messaging to the hub
Either make it a separate Class or integrate it into the FlightController class
"""
import socket
import unit_id

unit_details = unit_id.unit_details

SEPARATOR = "<SEPARATOR>"

def message(HUB_ADDRESS, PORT, message, message_type="<TELEM>", activity="N/A"):
    """
    Message format:
    1 - Message type (usually TELEM unless emergency/error that user needs to be aware of)
    2 - Unit name
    3 - Message
    4 - Activity for hub to add to record - if no activity this should be N/A
    """
    
    s=socket.socket()
    
    print(f"[{unit_details['unit_name']}] FC SIGNALLER: Connecting to hub...")
    s.connect((HUB_ADDRESS, PORT))
    print(f"[{unit_details['unit_name']}] FC SIGNALLER: Connected to hub at {HUB_ADDRESS}")
    
    message = f"{message_type}{SEPARATOR}{unit_details['unit_name'].upper()}{SEPARATOR}{message}{SEPARATOR}{activity}"
    
    
    
    s.send(message.encode())
    
    print(f"[{unit_details['unit_name']}] FC SIGNALLER: Message sent to hub: {message}\n")
    
    s.close()