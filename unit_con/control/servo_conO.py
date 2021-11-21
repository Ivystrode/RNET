import RPi.GPIO as GPIO
from time import sleep
import socket

# SERVO 1 (ROTATE SERVO)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

elev_fl = 12.6
elev_ce = 6.5
elev_fr = 1.5

rot_fl = 12.6
rot_ce = 7.1
rot_fr = 1.5

elevate_servo=GPIO.PWM(12,50)
elevate_servo.start(2.5)

print(f"[{socket.gethostname().upper()}] Testing elevate servo")
elevate_servo.ChangeDutyCycle(1.5) # FURTHEST RIGHT
sleep(1)
elevate_servo.ChangeDutyCycle(7.1) # CENTRE
sleep(1)
elevate_servo.ChangeDutyCycle(12.6) # FURTHEST LEFT
sleep(1)


# SERVO 2 (ELEVATE SERVO)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

rotate_servo=GPIO.PWM(11,50)
rotate_servo.start(2.5)

print(f"[{socket.gethostname().upper()}] Testing rotate servo")
rotate_servo.ChangeDutyCycle(1.5) # FURTHEST RIGHT
sleep(1)
rotate_servo.ChangeDutyCycle(7.1) # CENTRE
sleep(1)
rotate_servo.ChangeDutyCycle(12.6) # FURTHEST LEFT
sleep(1)

autorotate = False


def rotate(posn, axis):
    
	if axis == "rotate":
		elevate_servo.ChangeDutyCycle(float(posn))
	elif axis == "elevate":
		rotate_servo.ChangeDutyCycle(float(posn))
	else:
		print(f"[{socket.gethostname().upper()} - Servo Control] Error")

def centre_both():
    elevate_servo.ChangeDutyCycle(rot_ce)
    rotate_servo.ChangeDutyCycle(elev_ce)
    
def centre_rotate():
    elevate_servo.ChangeDutyCycle(rot_ce)
    
def centre_elevate():
    rotate_servo.ChangeDutyCycle(elev_ce)
    
def autorotate():
    # autorotate = False
    print(f"autorotate: {autorotate}")
     

# pwm.stop()
# GPIO.cleanup()

#test
