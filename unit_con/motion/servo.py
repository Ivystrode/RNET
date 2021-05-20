import RPi.GPIO as GPIO
from time import sleep

# SERVO 1 (ROTATE SERVO)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

rotator=GPIO.PWM(12,50)
rotator.start(2.5)

# SERVO 2 (ELEVATE SERVO)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

pwm=GPIO.PWM(11,50)
pwm.start(2.5)

rotator.ChangeDutyCycle(1.5) # FURTHEST RIGHT
sleep(1)
rotator.ChangeDutyCycle(7.1) # CENTRE
sleep(1)
rotator.ChangeDutyCycle(12.6) # FURTHEST LEFT
sleep(1)

# elevator.ChangeDutyCycle(1.5) # FURTHEST RIGHT
# sleep(1)
# elevator.ChangeDutyCycle(7.1) # CENTRE
# sleep(1)
# elevator.ChangeDutyCycle(12.6) # FURTHEST LEFT
# sleep(1)


def rotate(posn, axis):
	servo = axis
	# print(f"Rotating to {posn}")
	servo.ChangeDutyCycle(float(posn))
	
rotate(1.5, rotator)
sleep(0.5)
rotate(12.6, rotator)
sleep(0.5)
rotate(7.1, rotator)
sleep(1)

rotate(1.5, elevator)
sleep(0.5)
rotate(12.6, elevator)
sleep(0.5)
rotate(7.1, elevator)
sleep(1)

# pwm.stop()
# GPIO.cleanup()

#test
