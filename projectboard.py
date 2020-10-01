import logging
from Hardware.led import led
from Hardware.magnetswitch import magnetswitch
from Hardware.relay import relay


class ProjectBoard:
    ''' This ProjectBoard contains a Relay, a magnetswitch and two leds '''
    def __init__(self,Name):
        logging.info("Initialisation of projectBoard Name %s" % Name)
        self.name = Name
        try:
            self.magnet = magnetswitch(20,"Garagedeur")
            self.relay = relay(26,"Sturing Garage Deur")
            self.ledgreen =led ( 4, "LED green")
            self.ledred =led ( 17, "LED red")
        except Exception as e:
            logging.error("There was an exception at setting up the projectboard.")
            logging.error(str(e))

    def getdoorstatus(self):
            status = self.magnet.getstatus()
            return status

    def sendpulse(self):
        return self.relay.pulse()

    def blinkgreen(self):
        self.ledgreen.pulse()
        
    def blinkred(self):
        self.ledred.pulse()
        
    def relay_on(self):
        return self.relay.on()

    def relay_off(self):
        return self.relay.off()

    def getrelaystatus(self):
        status = self.relay.getstatus()
        return status
       
