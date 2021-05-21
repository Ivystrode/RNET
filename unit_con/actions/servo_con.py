import RPi.GPIO as GPIO
from time import sleep
import socket

# SERVO 1 (ROTATE SERVO)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

rotate_servo=GPIO.PWM(12,50)
rotate_servo.start(2.5)

print(f"[{socket.gethostname().upper()}] Testing rotate_servo servo")
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

print(f"[{socket.gethostname().upper()}] Testing elevate_servo servo")
elevate_servo.ChangeDutyCycle(1.5) # FURTHEST RIGHT
sleep(1)
elevate_servo.ChangeDutyCycle(7.1) # CENTRE
sleep(1)
elevate_servo.ChangeDutyCycle(12.6) # FURTHEST LEFT
sleep(1)



def rotate(posn, axis):
    print("servocon rotate")
	if axis == "rotate":
		rotate_servo.ChangeDutyCycle(float(posn))
	elif axis == "elevate":
		elevate_servo.ChangeDutyCycle(float(posn))
	else:
		print(f"[{socket.gethostname().upper()} - Servo Control] Error")

def centre_both():
    print("servocon cenboth")
    rotate_servo.ChangeDutyCycle(7.1)
    elevate_servo.ChangeDutyCycle(7.1)
    
def centre_rotate():
    print("servocon cenR")
    rotate_servo.ChangeDutyCycle(7.1)
    
def centre_elevate():
    print("servocon cenE")
    elevate_servo.ChangeDutyCycle(7.1)
     
	
rotate(1.5, "rotate")
sleep(0.5)
rotate(12.6, "rotate")
sleep(0.5)
rotate(7.1, "rotate")
sleep(1)

rotate(1.5, "elevate")
sleep(0.5)
rotate(12.6, "elevate")
sleep(0.5)
rotate(7.1, "elevate")
sleep(1)

# pwm.stop()
# GPIO.cleanup()

#test
