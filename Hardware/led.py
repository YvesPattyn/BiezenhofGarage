import RPi.GPIO as GPIO
from time import sleep

class led:
    name = ""
    gpiopin = 0

    def __init__(self,GpioPin,Name):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GpioPin,GPIO.OUT)
        self.gpiopin = GpioPin
        self.name = Name

    def on(self):
        print("led: %s turned on." % self.name)
        GPIO.output(self.gpiopin, GPIO.HIGH)

    def off(self):
        print("led: %s turned off." % self.name)
        GPIO.output(self.gpiopin, GPIO.LOW)

    def pulse(self, duration=0.2):
        print("led: %s was pulsed." % self.name)
        GPIO.output(self.gpiopin, GPIO.HIGH)
        sleep(duration)
        GPIO.output(self.gpiopin, GPIO.LOW)