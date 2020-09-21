import logging
from time import sleep
from Hardware.led import led
from Hardware.magnetswitch import magnetswitch
from Hardware.relay import relay

class ProjectBoard:

    def __init__(self,Name):
        logging.info("Initialisation of projectBoard Name %s" % Name)
        self.name = Name
        try:
            self.magnet = magnetswitch(17,"Garagedeur")
            self.relay = relay(27,"Sturing Garage Deur")
            self.ledgreen =led ( 4, "LED green")
            self.ledred =led ( 22, "LED red")
        except Exception as e:
            logging.error("There was an exception at setting up the projectboard.")
            logging.error(str(e))

    def getdoorstatus(self):
            status = self.magnet.getstatus()
            return status

    def sendpulse(self):
        return self.relay.pulse()
    
    def green_on(self):
        self.ledgreen.on()
        
    def green_off(self):
        self.ledgreen.off()
        
    def red_on(self):
        self.ledred.on()
        
    def red_off(self):
        self.ledgred.off()
        
    def blinkgreen(self):
        self.ledgreen.pulse()
        
    def blinkred(self, times = 1):
        if (times == 1):
            self.ledred.pulse(0.5)
        else:
            for x in range(1, times):
                self.ledred.pulse(0.1)
                sleep(0.1)
                
    def relay_on(self):
        return self.relay.on()

    def relay_off(self):
        return self.relay.off()

    def getrelaystatus(self):
        status = self.relay.getstatus()
        return status
       
