import cv2

from picamera import PiCamera
from datetime import datetime
import os
import socket
import time

from tqdm import tqdm

label = "[" + socket.gethostname().upper() + "]"
name = socket.gethostname()
file_channel = 7503 # same as status channel which hub is listening on. make a third channel if necessary/possible (i think it was necessary)

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024

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

# ==========end==========

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
    send_photo(hub_addr, img_name, f"Requested image taken at {datetime.now().strftime('%H:%M:%S')}")
    
def im_recog():
    while True:
        ret, frame = stream.read()

        ClassIndex, confidence, bbox = model.detect(frame, confThreshold=0.55)

        if len(ClassIndex) != 0:
            for ClassInd, conf, boxes in zip(ClassIndex.flatten(), confidence.flatten(), bbox):
                if ClassInd <= 80:
                    if labels[ClassInd-1] == "person" or labels[ClassInd-1] == "car":
                        cv2.rectangle(frame, boxes, (0,255,0), 2)
                        
                        # cv2.rectangle(frame,(boxes[0]-1, boxes[1]-30),(boxes[2]+boxes[0], boxes[1]),(0,255,0), -1)
                        cv2.putText(frame, f"{labels[ClassInd-1].capitalize()}: {round(float(conf*100), 1)}%",(boxes[0], boxes[1]-10), font, fontScale=font_scale, color=(0,255,0), thickness=2)
                        
                        print(f"{labels[ClassInd-1]} detected, dimensions: {boxes}, confidence: {round(float(conf*100), 1)}%")
                    
        cv2.imshow("Video detection", frame)

        if cv2.waitKey(5) & 0xFF == ord("c"):
            break

    stream.release()
    cv2.destroyAllWindows()





# Send a file to the hub
def send_photo(hub_addr, file, file_description):
    s = socket.socket()
    print(f"{label} Connecting to hub...")
    s.connect((hub_addr, file_channel))
    filesize = os.path.getsize(file)

    print(f"{label} Sending file: {file}")
    s.send(f"{file}{SEPARATOR}{filesize}{SEPARATOR}{file_description}".encode())
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

