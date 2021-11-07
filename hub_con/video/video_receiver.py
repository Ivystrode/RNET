from imutils import build_montages
from datetime import datetime
import numpy as np
import imagezmq
import argparse
import imutils
import cv2

config_file = "unit_con/control/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
frozen_model="unit_con/control/frozen_inference_graph.pb"
labels = []
with open("unit_con/control/Labels", "r") as f:
    labels = [line.strip() for line in f.readlines()]
confidence_level = 50
montageW = 250
montageH = 250
mW = 300
mH = 300

imageHub = imagezmq.ImageHub()

WATCH_FOR = set(['person','car','dog'])
object_count = {obj: 0 for obj in WATCH_FOR}
frameDict = {}

model = cv2.dnn_DetectionModel(frozen_model, config_file)
model.setInputSize(320,320)
model.setInputScale(1.0/127.5)
model.setInputMean((127.5,127.5,127.5))
model.setInputSwapRB(True)

def receive_stream():
    while True:
        # receive and ack
        (client_name, frame) = imageHub.recv_image()
        imageHub.send_reply(b'OK')
        
        frame = imutils.resize(frame, width=400)
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

        model.setInput(blob)
        detections = model.forward()
        
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence > confidence_level:
                idx = int(detections[0,0,i,1])

                if labels[idx] in WATCH_FOR:
                    object_count[labels[idx]] += 1
                    
                    box = detections[0,0,i,3:7] * np.array([w,h,w,h])
                    (startX,startY,endX,endY) = box.astype("int")

                    cv2.rectangle(frame,(startX, startY),(endX, endY), (255,0,0), 2)
                    cv2.putText(frame, client_name, (10,25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)

                    montages = build_montages(frameDict.values(), (w,h), (mW, mH))
                    
                    for (i, montage) in enumerate(montages):
                        cv2.imshow(f"{client_name} video stream")

                    
            
