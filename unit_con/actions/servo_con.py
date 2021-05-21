import RPi.GPIO as GPIO
from time import sleep
import socket

# SERVO 1 (ROTATE SERVO)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

rotate_servo=GPIO.PWM(12,50)
rotate_servo.start(2.5)

print(f"[{socket.gethostname().upper()}] Testing rotate servo")
rotate_servo.ChangeDutyCycle(1.5) # FURTHEST RIGHT
sleep(1)
rotate_servo.ChangeDutyCycle(7.1) # CENTRE
sleep(1)
rotate_servo.ChangeDutyCycle(12.6) # FURTHEST LEFT
sleep(1)


# SERVO 2 (ELEVATE SERVO)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

elevate_servo=GPIO.PWM(11,50)
elevate_servo.start(2.5)

print(f"[{socket.gethostname().upper()}] Testing elevate servo")
elevate_servo.ChangeDutyCycle(1.5) # FURTHEST RIGHT
sleep(1)
elevate_servo.ChangeDutyCycle(7.1) # CENTRE
sleep(1)
elevate_servo.ChangeDutyCycle(12.6) # FURTHEST LEFT
sleep(1)



def rotate(posn, axis):
    
	if axis == "rotate":
		rotate_servo.ChangeDutyCycle(float(posn))
	elif axis == "elevate":
		elevate_servo.ChangeDutyCycle(float(posn))
	else:
		print(f"[{socket.gethostname().upper()} - Servo Control] Error")

def centre_both():
    rotate_servo.ChangeDutyCycle(7.1)
    elevate_servo.ChangeDutyCycle(7.1)
    
def centre_rotate():
    rotate_servo.ChangeDutyCycle(7.1)
    
def centre_elevate():
    elevate_servo.ChangeDutyCycle(7.1)
     

# pwm.stop()
# GPIO.cleanup()

#test
