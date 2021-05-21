from picamera import PiCamera
from datetime import datetime
import os
import socket
import time

label = "[" + socket.gethostname() + "]"
name = socket.gethostname()
send_channel = 7501 # same as status channel which hub is listening on. make a third channel if necessary/possible

SEPARATOR = "<SEPARATOR>"

# Take a picture
def capt_img(hub_addr):
    print(f"{label} Capture image")
    img_name = datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + str(name)
    camera = PiCamera()
    camera.resolution = (1024, 768)
    camera.start_preview()
    time.sleep(2) # apparently camera has to "warm up"
    camera.capture(img_name)
    print(f"{label} Image saved as {img_name}")
    send_file(hub_addr, img_name)
    
    
# Send a file to the hub
def send_file(hub_addr, file):
    s = socket.socket()
    print(f"{label} Connecting to hub...")
    s.connect((hub_addr, send_channel))
    filesize = os.path.getsize(file)

    print(f"{label} Sending file: {file}")
    s.send(f"<FILE_TRANSFER>{SEPARATOR}{file}{SEPARATOR}{filesize}")
    print(f"{label} {file} sent to hub")
    s.close()

