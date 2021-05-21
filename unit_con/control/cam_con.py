from picamera import PiCamera
from datetime import datetime
import os
import socket
import time

label = "[" + socket.gethostname().upper() + "]"
name = socket.gethostname()
file_channel = 7503 # same as status channel which hub is listening on. make a third channel if necessary/possible

SEPARATOR = "<SEPARATOR>"

# Take a picture
def capt_img(hub_addr):
    print(f"{label} Capture image")
    img_name = datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + str(name) + ".jpg"
    camera = PiCamera()
    camera.resolution = (1024, 768)
    camera.start_preview()
    time.sleep(2) # apparently camera has to "warm up"
    camera.capture(img_name)
    time.sleep(0.5)
    camera.close()
    print(f"{label} Image saved as {img_name}")
    send_file(hub_addr, img_name)
    
    
# Send a file to the hub
def send_file(hub_addr, file):
    s = socket.socket()
    print(f"{label} Connecting to hub...")
    s.connect((hub_addr, file_channel))
    filesize = os.path.getsize(file)

    print(f"{label} Sending file: {file}")
    s.send(f"{file}{SEPARATOR}{filesize}".encode())
    print(f"{label} {file} sent to hub")
    s.close()

