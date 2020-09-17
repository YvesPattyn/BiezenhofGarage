import logging
import RPi.GPIO as GPIO
from time import sleep

class relay:
    name = ""
    gpiopin = 0

    def __init__(self,GpioPin,Name):
        logging.info("Initialise Relay %s on GpioPin %i" % (Name, GpioPin))
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GpioPin,GPIO.OUT)
        self.gpiopin = GpioPin
        self.name = Name

    def on(self):
        logging.info("Relay: %s turned on." % self.name)
        GPIO.output(self.gpiopin, GPIO.HIGH)

    def off(self):
        logging.info("Relay: %s turned off." % self.name)
        GPIO.output(self.gpiopin, GPIO.LOW)

    def pulse(self, duration=1.25):
        logging.info("Relay: %s was pulsed." % self.name)
        GPIO.output(self.gpiopin, GPIO.HIGH)
        sleep(duration)
        GPIO.output(self.gpiopin, GPIO.LOW)
