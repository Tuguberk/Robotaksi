import RPi.GPIO as GPIO
import time

class servo:
    def __init__(self,pin):
        self.pin = pin
        self.pwm = GPIO.PWM(servo, 50)

    def write(self,derece):
        try:
            dutyCycle = angle / 18. + 3.
            self.pwm.ChangeDutyCycle(dutyCycle)
            sleep(0.3)
            self.pwm.stop()
        except:
            GPIO.cleanup()
