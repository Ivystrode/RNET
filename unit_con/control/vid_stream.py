# import required modules
from flask import Flask, render_template, Response 
import picamera 
import cv2

app = Flask(__name__) 
vc = picamera.PiCamera()
@app.route('/') 
def index(): 
   """Video streaming .""" 
   print("index")
   return render_template("<p>{{ url_for('video_feed') }}<p>") 
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
   return Response(gen(), 
                   mimetype='multipart/x-mixed-replace; boundary=frame') 

def run():
    print("whoo")
    app.run(host='192.168.1.222', port=8081, debug=True, threaded=True)
