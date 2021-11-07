import io
import socket
import struct
from flask import Flask,render_template,Response
import cv2

from picamera import PiCamera
from datetime import datetime
import os
import time
from unit_id import unit_details

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
def stream_video():

    app=Flask(__name__)
    camera=PiCamera()

    def generate_frames():
        while True:
                
            ## read the camera frame
            success,frame=camera.read()
            if not success:
                break
            else:
                ret,buffer=cv2.imencode('.jpg',frame)
                frame=buffer.tobytes()

            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/video')
    def video():
        return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

    app.run(host='0.0.0.0', debug=True, threaded=True)

def stream_video_worksButNotToBrowser():
    client_socket = socket.socket()

    client_socket.connect(('192.168.1.79', 8081))  # ADD IP HERE

    # Make a file-like object out of the connection
    connection = client_socket.makefile('wb')
    try:
        camera = PiCamera()
        camera.vflip = True
        camera.resolution = (500, 480)
        # Start a preview and let the camera warm up for 2 seconds
        camera.start_preview()
        time.sleep(2)

        # Note the start time and construct a stream to hold image data
        # temporarily (we could write it directly to connection but in this
        # case we want to find out the size of each capture first to keep
        # our protocol simple)
        start = time.time()
        stream = io.BytesIO()
        for foo in camera.capture_continuous(stream, 'jpeg'):
            # Write the length of the capture to the stream and flush to
            # ensure it actually gets sent
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            # Rewind the stream and send the image data over the wire
            stream.seek(0)
            connection.write(stream.read())
            # If we've been capturing for more than 30 seconds, quit
            if time.time() - start > 60:
                break
            # Reset the stream for the next capture
            stream.seek(0)
            stream.truncate()
        # Write a length of zero to the stream to signal we're done
        connection.write(struct.pack('<L', 0))
    finally:
        connection.close()
        client_socket.close()
def stop_stream():
    pass



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







