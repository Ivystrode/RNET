"""
Unique file for each unit
"""

import socket

unit_details = {
    "unit_name": socket.gethostname().upper(),
    "unit_id": "01",
    "type": "prototype",
    "description": "Test unit for development",
    "hub_address": "192.168.1.79",
    "video_port": "8081"
}