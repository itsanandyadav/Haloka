#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, request

# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera_pi import Camera

import RPi.GPIO as GPIO
in1=37
in2=35
in3=33
in4=31
GPIO.setwarnings(False)			#disable warnings
GPIO.setmode(GPIO.BOARD)		#set pin numbering system

GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)

pwm1=GPIO.PWM(in1,1000)
pwm2=GPIO.PWM(in2,1000)
pwm3=GPIO.PWM(in3,1000)
pwm4=GPIO.PWM(in4,1000)

pwm1.start(0)
pwm2.start(0)
pwm3.start(0)
pwm4.start(0)

duty=20


# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)


@app.route('/', methods = ['POST','GET'])
def index():
    """Video streaming home page."""
    if request.method=="POST":
        button_pressed = int(request.form.get('value'))
        print("button_pressed :",button_pressed)
        if button_pressed ==1:
            print("Moving RIGHT")
            pwm1.ChangeDutyCycle(duty)
            pwm2.ChangeDutyCycle(0)
            pwm3.ChangeDutyCycle(0)
            pwm4.ChangeDutyCycle(0)

        elif button_pressed==2:
            print("Moving LEFT")
            pwm1.ChangeDutyCycle(0)
            pwm2.ChangeDutyCycle(0)
            pwm3.ChangeDutyCycle(duty)
            pwm4.ChangeDutyCycle(0)

        elif button_pressed==3:
            print("Moving BWD ")
            pwm1.ChangeDutyCycle(0)
            pwm2.ChangeDutyCycle(duty)
            pwm3.ChangeDutyCycle(0)
            pwm4.ChangeDutyCycle(duty)

        elif button_pressed==4:
            print("Moving FWD")
            pwm1.ChangeDutyCycle(duty)
            pwm2.ChangeDutyCycle(0)
            pwm3.ChangeDutyCycle(duty)
            pwm4.ChangeDutyCycle(0)

        elif button_pressed==0:
            print("Stop Moving")
            pwm1.ChangeDutyCycle(0)
            pwm2.ChangeDutyCycle(0)
            pwm3.ChangeDutyCycle(0)
            pwm4.ChangeDutyCycle(0)

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
