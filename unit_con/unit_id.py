"""
Unique file for each unit
ID is based on a bash of the hostname/unit name

THESE NEED TO BE UPDATED TO BE CLASS ATTRIBUTES NOW

"""

import socket, hashlib

hasher = hashlib.sha1()
encoded_id = socket.gethostname().lower().encode()
hasher.update(encoded_id)

unit_details = {
    "unit_name": socket.gethostname().upper(),
    "unit_id": str(hasher.hexdigest()),
    "type": "prototype",
    "description": "Test unit for development",
    "hub_address": "192.168.1.79", # MEDEND NETWORK
    # "hub_address": "127.0.0.1", # LOCAL TESTING
    "video_port": 8081
}