"""
Unique file for each unit
"""

import socket, random

unit_details = {
    "unit_name": socket.gethostname().upper(),
    "unit_id": hash(socket.gethostname()),
    "type": "prototype",
    "description": "Test unit for development",
    "hub_address": "192.168.1.79", # MEDEND NETWORK
    # "hub_address": "127.0.0.1", # LOCAL TESTING
    "video_port": 8081
}