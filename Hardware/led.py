import logging
import RPi.GPIO as GPIO
from time import sleep

class led:
    name = ""
    gpiopin = 0

    def __init__(self,GpioPin,Name):
        logging.info("Initialised Led %s on GpioPin %i." % (Name, GpioPin))
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GpioPin,GPIO.OUT)
        self.gpiopin = GpioPin
        self.name = Name

    def on(self):
        logging.info("Led: %s turned on." % self.name)
        GPIO.output(self.gpiopin, GPIO.HIGH)

    def off(self):
        logging.info("led: %s turned off." % self.name)
        GPIO.output(self.gpiopin, GPIO.LOW)

    def pulse(self, duration=0.2):
        logging.info("led: %s was pulsed." % self.name)
        GPIO.output(self.gpiopin, GPIO.HIGH)
        sleep(duration)
        GPIO.output(self.gpiopin, GPIO.LOW)