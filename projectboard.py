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
            self.log("ProjectBoard: Door switch init<br />")
            self.magnet = magnetswitch(13,"Linker Deur ")

            self.log("ProjectBoard:relay init<br />")
            self.relay = relay(26,"Sturing Garage Deur<br />")

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

    def relay_on(self):
        return self.relay.on()

    def relay_off(self):
        return self.relay.off()

    def getrelaystatus(self):
        return self.relay.getstatus()
       
