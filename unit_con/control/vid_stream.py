from flask import Flask, render_template, Response, request
import time
import picamera
import os

app = Flask(__name__)
#app = Flask(__name__, template_folder='/var/www/html/templates')

@app.route('/', methods=['GET', 'POST'])
def move():
    result = ""
    if request.method == 'POST':
        
        return render_template('index.html', res_str=result)
                        
    return render_template('index.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(picamera.PiCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

app.run(host='0.0.0.0', debug=True, threaded=True)