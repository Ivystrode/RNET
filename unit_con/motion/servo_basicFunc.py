import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

pwm=GPIO.PWM(12,50)
pwm.start(2.5)

pwm.ChangeDutyCycle(1.5) # FURTHEST RIGHT
sleep(1)
pwm.ChangeDutyCycle(7.1) # CENTRE
sleep(1)
pwm.ChangeDutyCycle(12.6) # FURTHEST LEFT
sleep(1)


def rotate(posn):
	# print(f"Rotating to {posn}")
	pwm.ChangeDutyCycle(int(posn))
	
rotate(1.5)
sleep(0.5)
rotate(12.6)
sleep(0.5)
rotate(7.1)
sleep(1)

# pwm.stop()
# GPIO.cleanup()

#test
