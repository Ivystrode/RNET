import io
import socket
import struct
import subprocess
import cv2
import os
import time
import threading
import numpy as np
from datetime import datetime

from picamera import PiCamera
from picamera.array import PiRGBArray
from datetime import datetime
from unit_id import unit_details

from tqdm import tqdm

label = "[" + socket.gethostname().upper() + "]"
name = socket.gethostname()
file_channel = 7503 # same as status channel which hub is listening on. make a third channel if necessary/possible (i think it was necessary)

object_detection_active = False
detection_duration = 30

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024

# ==========COMMAND SUBROUTER==========
def command_subrouter(command):
    global detection_duration
    global object_detection_active
    print("CAM_CON - COMMAND RECEIVED")
    print(command)
    if command[1] == "stream":
        print("starting vid stream service")
        start_stream()
        print("streaming active")
    elif command[1] == "stopstream":
        print("stopping video transmission")
        stop_stream()
        print("stream stopped")
    elif command[1] == "image_detection":
        print("toggle image detection")
        if not object_detection_active:
            print("its active")
            # stop_stream()
            # time.sleep(2)
            object_detection_active = True
            detection_duration = int(command[2])
            detection_thread.start()
            count_thread.start()
        else:
            print("detection already running - stopping it now")
            det_stop()
    else:
        print(f"unknown command: {command[1]}")

# ==========IMAGE DETECTION SETUP==========
camera_active = False


config_file = "unit_con/control/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
frozen_model="unit_con/control/frozen_inference_graph.pb"
labels = []
with open("unit_con/control/Labels", "r") as f:
    labels = [line.strip() for line in f.readlines()]

model = cv2.dnn_DetectionModel(frozen_model, config_file)
model.setInputSize(320,320)
model.setInputScale(1.0/127.5)
model.setInputMean((127.5,127.5,127.5))
model.setInputSwapRB(True)

# stream = cv2.VideoCapture(0) do not activate until im recog is on other camera is used up
# stream.set(cv2.CAP_PROP_FPS, 30)

font_scale = 2
font = cv2.FONT_HERSHEY_PLAIN

# ==========Basic image capture & send to hub==========

# Take a picture
def capt_img(hub_addr):
    print(f"{label} Capture image")
    img_name = datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + str(name) + ".jpg"
    camera = PiCamera()
    camera.resolution = (1024, 768)
    camera.vflip = True
    camera.hflip = True
    camera.start_preview()
    time.sleep(2) # apparently camera has to "warm up"
    camera.capture(img_name)
    time.sleep(0.5)
    camera.close()
    print(f"{label} Image saved as {img_name}")
    send_photo(hub_addr, img_name, f"Camera shot")
    
# Send a file to the hub
def send_photo(hub_addr, file, file_description):
    s = socket.socket()
    print(f"{label} Connecting to hub...")
    s.connect((hub_addr, file_channel))
    filesize = os.path.getsize(file)
    file_type = "photo"

    print(f"{label} Sending file: {file}")
    s.send(f"{file}{SEPARATOR}{filesize}{SEPARATOR}{file_description}{SEPARATOR}{file_type}".encode())
    try:
        progress = tqdm(range(filesize), f"{label} Sending {file}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(file, "rb") as f:
            for _ in progress:
                try:
                    bytes_read = f.read(BUFFER_SIZE)
                    
                    if not bytes_read:
                        break
                    
                    s.sendall(bytes_read)
                    progress.update(len(bytes_read))
                except Exception as e:
                    print(f"{label} FILE SEND ERROR: {e}")
                    break
    except Exception as e:
        print(f"{label} FILE SEND ERROR - outside - {e}")
    print(f"{label} {file} sent to hub")
    s.close()
    

# ==========Live video streaming==========
def start_stream():
    """
    These two functions work but using motion isn't ideal
    """
    subprocess.run(['sudo','service','motion','start'])
    print("Video transmitting")

def stop_stream():
    subprocess.run(['sudo','service','motion','stop'])
    print("Video transmission stopped")

def stream_video_direct():
    """
    This streams direct to the hub - not the interface
    Use this to run server side recognition models
    (At some point want this showing on the interface)
    """
    
    
    client_socket = socket.socket()

    client_socket.connect((unit_details['hub_address'], unit_details['video_port'])) 

    connection = client_socket.makefile('wb')
    
    try:
        camera = PiCamera()
        camera.vflip = True
        camera.resolution = (500, 480)
        camera.start_preview()
        time.sleep(2)
        start = time.time()
        stream = io.BytesIO()
        
        for _ in camera.capture_continuous(stream, 'jpeg'):
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            stream.seek(0)
            connection.write(stream.read())
            
            if time.time() - start > 60:
                break
            
            stream.seek(0)
            stream.truncate()
            
        connection.write(struct.pack('<L', 0))
        
    finally:
        connection.close()
        client_socket.close()
        



# ==========Motion detection==========
class SingleMotionDetector:
    def __init__(self, accumWeight=0.5):
        self.accumWeight = accumWeight # the bigger t his is the less the bg will be factored in; the lower it is the MORE the bg will be factored in
        # at 0.5 it weighs back and foreground evenly, play with it to adjust if necessary
        
    def update(self, image):
        # take an input frame and compute weighted average
        if self.bg is None:
            self.bg = image.copy().astype("float")
            return
        
        # update bg model by accuming the weighted av
        cv2.accumulateWeighted(image, self.bg, self.accumWeight)
        
    def detect(self, image, tVal=25):
        """
        compute the absolute diff between bg and image
        """
        # tVal/threshold value to mark a pixel as moved/moving
        delta = cv2.absdiff(self.bg.astype("uint8"), image)
        thresh = cv2.threshold(delta, tVal, 255, cv2.THRESH_BINARY)[1]
        
        # erode/deliate to remove tiny blobs
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)
        
        # contours to extract motion regions
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        (minX, minY) = (np.inf, np.inf)
        (maxX, maxY) = (-np.inf, -np.inf)
        
        # if no contours found - no motion was detected
        if len(cnts) == 0:
            return None
        
        # otherwise loop over them and get the coordinates the motion took palce at
        for c in cnts:
            # get the boundary box
            (x,y,w,h) = cv2.boundingRect(c)
            (minX, minY) = (min(minX, x), min(minY, y))
            (maxX, maxY) = (max(maxX, x), max(maxY, y))
            
        # return thresholded image & bounding box
        return (thresh, (minX, minY, maxX, maxY))




# ==========Object recognition==========
def im_recog():
    """
    Run the model on the rpi's camera, if it detects a person or a car it takes a still and sends it to the users
    Later on this function will take parameters allowing users to choose which model to use or what object to detect/look for
    """
    global object_detection_active
    stop_stream()
    time.sleep(4)
    
    detection = False
    counts_before_detect_again = 0
    
    config_file = "unit_con/control/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
    frozen_model="unit_con/control/frozen_inference_graph.pb"
    labels = []
    with open("unit_con/control/Labels", "r") as f:
        labels = [line.strip() for line in f.readlines()]

    model = cv2.dnn_DetectionModel(frozen_model, config_file)
    model.setInputSize(320,320)
    model.setInputScale(1.0/127.5)
    model.setInputMean((127.5,127.5,127.5))
    model.setInputSwapRB(True)
    
    camera = PiCamera()
    camera.resolution = (1024, 768)
    camera.vflip = True
    camera.hflip = True
    camera.framerate = 32
    raw_capture = PiRGBArray(camera, size=(1024, 768))
    time.sleep(1)
        
    print("detecting active")
    while True:
        if object_detection_active:
            for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
                
                image = frame.array

                ClassIndex, confidence, bbox = model.detect(image, confThreshold=0.55)

                if len(ClassIndex) != 0:
                    for ClassInd, conf, boxes in zip(ClassIndex.flatten(), confidence.flatten(), bbox):
                        if ClassInd <= 80:
                            if labels[ClassInd-1] == "person" or labels[ClassInd-1] == "car":
                                # these aren't working in this implementation
                                cv2.rectangle(image, boxes, (0,255,0), 2)
                                cv2.putText(image, f"{labels[ClassInd-1].capitalize()}: {round(float(conf*100), 1)}%",(boxes[0], boxes[1]-10), font, fontScale=font_scale, color=(0,255,0), thickness=2)

                                if not detection:
                                    cv2.imwrite(f'{labels[ClassInd-1].capitalize()} detection_{datetime.now().strftime("%H%M%S")}.jpg', image)
                                    detection = True
                                    print(f"{labels[ClassInd-1]} detected, dimensions: {boxes}, confidence: {round(float(conf*100), 1)}%")
                                    send_photo(unit_details['hub_address'], f'{labels[ClassInd-1].capitalize()} detection_{datetime.now().strftime("%H%M%S")}.jpg', f"{labels[ClassInd-1].capitalize()} detected: {round(float(conf*100), 1)}% confidence")
                                
                if detection:
                    counts_before_detect_again += 1
                    if counts_before_detect_again > 500: # this is about a minute or so? we don't want to do this TOO often...
                        detection = False
                        counts_before_detect_again = 0
                        
                    # monitor present only
                    # cv2.imshow("Video detection", frame)

                # only relevant if testing unit with a monitor/keyboard connected...
                if cv2.waitKey(5) & 0xFF == ord("c"):
                    object_detection_active = False
                    break
                
                raw_capture.truncate(0)
                
        else:
            break
        
    print("end of detection")
    # stream.release()
    camera.close()
    cv2.destroyAllWindows()
    
def det_timer(_duration):
    """
    Stops the object recognition after the determined duration
    """
    global object_detection_active
    time.sleep(_duration)
    object_detection_active = False
    print("Detection running status:")
    print(detection_thread.is_alive())
    time.sleep(2)
    print(detection_thread.is_alive())
    
def det_stop():
    """
    Stops object detection on order
    """
    global object_detection_active
    object_detection_active = False
    print("Detection stopped")
    print("Detection running status:")
    print(detection_thread.is_alive())
    time.sleep(2)
    print(detection_thread.is_alive())
    

detection_thread = threading.Thread(target=im_recog, daemon=True)
count_thread = threading.Thread(target=det_timer, kwargs={'_duration':detection_duration})


