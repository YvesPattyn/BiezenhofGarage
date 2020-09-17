import logging
import RPi.GPIO as GPIO

class magnetswitch:
    gpiopin = 0
    name = ""

    def __init__(self,GpioPin,Name):
        logging.info("Initialise Magnetic Switch %s on GpioPin %i" % (Name, GpioPin) )
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GpioPin,GPIO.IN)
        self.gpiopin = GpioPin
        self.name = Name

    def getstatus(self):
        status = GPIO.input(self.gpiopin)
        logging.info("Magnetic Switch status=%i" % status)
        return status
