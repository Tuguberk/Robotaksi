import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class servo:
    def __init__(self,pin):
        GPIO.setup(pin, GPIO.OUT)
        self.pwm = GPIO.PWM(pin, 100)

    def write(self,derece):
        try:
            self.pwm.start(5)
            self.pwm.ChangeDutyCycle(float(derece) / 10.0 + 2.5)
            sleep(0.3)
            self.pwm.stop()
        except:
            GPIO.cleanup()
servo_kapı = servo(27)
servo_kapı.write(10)

"""
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
def setServoAngle(servo, angle):
	pwm = GPIO.PWM(servo, 50)
	pwm.start(8)
	dutyCycle = angle / 18. + 3.
	pwm.ChangeDutyCycle(dutyCycle)
	sleep(0.3)
	pwm.stop()
if __name__ == '__main__':
	import sys
	servo = int(sys.argv[1])
	GPIO.setup(servo, GPIO.OUT)
	setServoAngle(servo, int(sys.argv[2]))
	GPIO.cleanup()"""
