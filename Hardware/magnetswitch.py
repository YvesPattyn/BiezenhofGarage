import RPi.GPIO as GPIO

class magnetswitch:
    gpiopin = 0
    name = ""

    def __init__(self,GpioPin,Name):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GpioPin,GPIO.IN)
        self.gpiopin = GpioPin
        self.name = Name

    def getstatus(self):
        return GPIO.input(self.gpiopin)
