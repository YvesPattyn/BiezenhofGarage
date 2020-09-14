from Hardware.led import led
from Hardware.magnetswitch import magnetswitch
from Hardware.relay import relay

class ProjectBoard:

    def log(self,message):
        #print(message)
        pass

    def __init__(self,Name):
        self.log("ProjectBoard Name %s <br />" % Name)
        self.name = Name
        try:
            self.log("ProjectBoard: Door switch init")
            self.magnet = magnetswitch(20,"Garagedeur")

            self.log("ProjectBoard:relay ini")
            self.relay = relay(26,"Sturing Garage Deur")
            self.ledgreen =led ( 4, "LED green")
            self.ledred =led ( 17, "LED red")
        except Exception as e:
            self.log("There was an exception at setting up the projectboard.<br />")
            self.log(str(e))

    def getdoorstatus(self):
            status = self.magnet.getstatus()
            self.log("getdoorstatus : %i <br />" % status)
            return status

    def sendpulse(self):
        self.log("sendpulse <br />")
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
        return self.relay.getstatus()
       
