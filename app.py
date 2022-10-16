#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, request

# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera import Camera

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)


@app.route('/', methods = ['POST','GET'])
def index():
    """Video streaming home page."""
    if request.method=="POST":
        print("Printing value : ",request.form.get('value'))
        button_pressed = int(request.form.get('value'))
        # print("form data : ",request.form)
        # print("button_pressed :",button_pressed)
        if button_pressed ==1:
            print("Moving right")

        elif button_pressed==2:
            print("Moving left")

        elif button_pressed==3:
            print("Moving bwd ")

        elif button_pressed==4:
            print("Moving fwd")

        elif button_pressed==0:
            print("Moving stop")

    else:
        print("not a post method")
    return render_template('index.html')

def gen(camera):
    """Video streaming generator function."""
    yield b'--frame\r\n'
    while True:
        frame = camera.get_frame()
        yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
