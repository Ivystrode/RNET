# import required modules
from flask import Flask, render_template, Response 
import picamera 
import cv2

app = Flask(__name__, template_folder='/home/pi/Code/rnet/rnet_testing/unit_con/control/templates') 
vc = picamera.PiCamera()
@app.route('/') 
def index(): 
   """Video streaming .""" 
   print("index")
   return render_template("index.html") 
def gen(): 
   """Video streaming generator function.""" 
   print("gen")
   while True: 
       rval, frame = vc.read() 
       cv2.imwrite('pic.jpg', frame) 
       yield (b'--frame\r\n' 
              b'Content-Type: image/jpeg\r\n\r\n' + open('pic.jpg', 'rb').read() + b'\r\n') 
@app.route('/video_feed') 
def video_feed(): 
   """Video streaming route. Put this in the src attribute of an img tag.""" 
   print("feed")
   return Response(gen(vc), 
                   mimetype='multipart/x-mixed-replace; boundary=frame') 

def run():
    print("whoo")
    app.run(host='0.0.0.0', port=5555, debug=True, threaded=True)
